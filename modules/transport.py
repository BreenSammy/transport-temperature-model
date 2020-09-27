import copy
from dateutil.parser import parse
from datetime import date, datetime, timedelta 
import json
from json import JSONEncoder, JSONDecoder
import os
import re

import numpy as np
import pandas as pd

from modules.cargo import cargoDecoder
import modules.weather.weather as weather
from modules.route import Route, RouteGPX, FTMRoute


class Transport:
    def __init__(self, name, transporttype, start, end, cargo, route, stops = None, reread_temperature = True):
        # if route_filename.endswith('.gpx'):
        #     self.route = RouteGPX(start, end, route_filename)
        self.name = name
        self.type = transporttype
        self.start = start
        self.end = end
        self.cargo = cargo
        self.route = route
        self.stops = stops

        self._folder = os.path.join('transports', self.name)
        self._jsonpath = os.path.join(self._folder, self.name + '.json')
        self._weatherdatapath = os.path.join(self._folder, 'weatherdata.csv')
        
        if reread_temperature:
            self.weatherdata = self.get_weatherdata()
        elif os.path.exists(self._weatherdatapath):
            self.weatherdata = pd.read_csv( self._weatherdatapath, parse_dates = ['Date'])
        else:
            self.weatherdata = self.get_weatherdata()
    
    def get_weatherdata(self):
        weatherdata = self.route.waypoints(self.start, self.stops)
        length = len(weatherdata.index)
        temperature = np.zeros([length, 1])
        lat = weatherdata[['Lat']].values
        lon = weatherdata[['Lon']].values

        for i in range(length):
            current_datetime = weatherdata['Date'].iloc[i]
            current_datetime = pd.Timestamp(current_datetime)
            current_datetime = current_datetime.to_pydatetime()
            temperature[i] = weather.temperature(current_datetime, lat[i][0], lon[i][0])

        weatherdata['T'] = temperature
        return weatherdata

    def save_weatherdata(self, filename):
        """Saves transport dataframe as .csv file"""
        self.weatherdata.to_csv(filename, encoding='utf-8', index=False)
    
    def to_json(self, filename):
        """Saves transport object data as json file"""
        with open(filename, 'w') as outfile:
            json.dump(self, outfile, cls = TransportEncoder, indent = 4)
    
    def save(self):
        """Save transport as json and weatherdata as csv"""   
        if not os.path.exists(self._folder):
            os.makedirs(self._folder)

        self.to_json(self._jsonpath)
        self.save_weatherdata(self._weatherdatapath)

class TransportEncoder(JSONEncoder):
    """
    JSONEncoder for Transport object. 
    Mainly handles serialisation of datetime.datetime objects.
    See also: https://gist.github.com/simonw/7000493
    """
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"
    def default(self, transport):

        if isinstance(transport, Transport):
            # Transform stop instances in list into dicts
            stops = [stop.to_dict() for stop in transport.stops]
            # Transform datetime instances to string
            for stop in stops:
                days = stop["duration"].days
                seconds = stop["duration"].seconds
                hours, remainder = divmod(seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                hours = hours + days*24
                stop["duration"] = '{0}:{1}:{2}'.format(hours, minutes, seconds)
                # stop["duration"] = stop["duration"].strftime("%s" % (
                #         self.TIME_FORMAT
                #     ))
            # Return dictionary for json file
            return {
                "name": transport.name,
                "type": transport.type,
                "start": transport.start.strftime("%s %s" % (
                    self.DATE_FORMAT, self.TIME_FORMAT
                )),
                "end": transport.end.strftime("%s %s" % (
                    self.DATE_FORMAT, self.TIME_FORMAT
                )),
                "route": {
                    "start_coordinates": transport.route.start(),
                    "end_coordinates": transport.route.end(),
                },
                "cargo": [item.to_dict() for item in transport.cargo]           
            }

class TransportDecoder(JSONDecoder):
    """
    JSONDecoder for Transport object. Handles deserialisation of datetime.datetime objects.
    See also: https://gist.github.com/setaou/ff98e82a9ce68f4c2b8637406b4620d1
    """
     #This an elementary date checker, rather than  ISO date checker.
    datetime_regex = re.compile(r'(\d{4}[-/]\d{2}[-/]\d{2})')
    #Duration checker
    duration_regex = re.compile(r'(\d{0,9}[:/]\d{2}[:/]\d{2})')

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, *args, **kwargs)
        self.parse_string = TransportDecoder.new_scanstring
        # Use the python version as the C version does not use the new parse_string
        self.scan_once = json.scanner.py_make_scanner(self) 


    @classmethod
    def new_scanstring(cls, s, end, strict=True):
        """Handles deserialisation of datetime.datetime objects."""
        (s, end) = json.decoder.scanstring(s, end, strict)
        if cls.datetime_regex.match(s):
            return (parse(s), end)
        elif cls.duration_regex.match(s):
            return (parse_duration(s), end)
        else:
            return (s, end)

def parse_duration(duration_str):
    """
    Method to parse a duration in format hours:minutes:seconds as datetime.timedelta instance
    See also: https://stackoverflow.com/questions/4628122/how-to-construct-a-timedelta-object-from-a-simple-string
    """
    duration_regex = re.compile(r'((?P<hours>\d+?):)?((?P<minutes>\d+?):)?((?P<seconds>\d+?))?')
    parts = duration_regex.match(duration_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in parts.items():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)

class Stop:
    """Class to represent a stop during transport."""
    def __init__(self, duration, lat, lon):
        self.duration = duration
        self.lat = lat
        self.lon = lon

    def coordinates(self):
        return np.array([self.lat, self.lon])

    def to_dict(self):
        return {
            'duration': self.duration,
            'lat': self.lat,
            'lon': self.lon
        }

def stopDecoder(obj):
    return Stop(obj['duration'], obj['lat'], obj['lon'])

def from_json(filename, reread_temperature = True):
    """Create Transport instance from json file"""
    json_dict = json.load(filename, cls=TransportDecoder)
    # Read all parameters from the dict
    name = json_dict['name']
    transporttype = json_dict['type']
    start = json_dict['start']
    end = json_dict['end']
    # Create cargo instances
    cargo = [cargoDecoder(item) for item in json_dict['cargo']]
    route_start = json_dict['route']['start_coordinates']
    route_end = json_dict['route']['end_coordinates']
    route = FTMRoute(route_start, route_end)
    # Create stop instances
    stops = [stopDecoder(stop) for stop in json_dict['stops']]
    # Return the transport instance
    return Transport(
        name, transporttype, start, end, cargo, route, 
        stops = stops, reread_temperature = reread_temperature
        )

