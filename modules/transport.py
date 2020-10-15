import copy
from dateutil.parser import parse
from datetime import date, datetime, timedelta 
import json
from json import JSONEncoder, JSONDecoder
import os
import re

import matplotlib
import matplotlib.pyplot as plt
import mplleaflet
import numpy as np
import pandas as pd

from modules.cargo import cargoDecoder
import modules.weather as weather
from modules.route import GPXRoute, FTMRoute, CSVRoute

matplotlib.use('Agg')

ROUTESPATH = os.path.abspath('routes')

class Transport:
    def __init__(self, name, transporttype, start, end, cargo, route, stops = []):
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
        
        if os.path.exists(self._weatherdatapath):
            self.weatherdata = pd.read_csv(self._weatherdatapath, parse_dates = ['Date'])
            start = self.weatherdata['Date'].iloc[0]
            end = self.weatherdata['Date'].iloc[-1]
        else:
            self.weatherdata = self.get_weatherdata()

        if self.start != start or self.end != end:
            self.weatherdata = self.get_weatherdata()

        # Write start and end of weatherdata back to transport
        self.start = self.weatherdata['Date'].iloc[0]
        self.end = self.weatherdata['Date'].iloc[-1]

    def plot_waypoints(self, tiles = 'cartodb_positron'):
        xy = self.weatherdata[['Lon', 'Lat']].values
        # Plot the path as red dots connected by a blue line
        plt.plot(xy[:,0], xy[:,1], 'r.')
        plt.plot(xy[:,0], xy[:,1], 'b')

        filename = os.path.join(self._folder, 'route.html')
        mplleaflet.save_html(fileobj=filename, tiles = tiles)
        
    def get_weatherdata(self):
        if isinstance(self.route, FTMRoute):
            weatherdata = self.route.waypoints(self.start, self.stops)
        elif isinstance(self.route, GPXRoute):
            weatherdata = self.route.waypoints(self.start, self.end)
        elif isinstance(self.route, CSVRoute):
            weatherdata = self.route.waypoints(self.start)

        datetimes = weatherdata.Date.tolist()
        lat = weatherdata.Lat.values
        lon = weatherdata.Lon.values

        weatherdata['T'] = weather.waypoints_temperature(datetimes, lat, lon)
        weatherdata['T'] = weatherdata['T'].interpolate()

        # sections = weatherdata.groupby(['sea'])

        # for _, section in sections:
        #     print(section)
        #     datetimes = section.Date.tolist()
        #     lat = section.Lat.values
        #     lon = section.Lon.values
        #     onsea = section['sea'].iloc[0]
        #     if onsea:
        #         section['T'] = weather.temperature_onsea(datetimes, lat, lon)
        #     else:
        #         section['T'] = weather.temperature_onland(datetimes, lat, lon)

        # sections_onsea = weatherdata[weatherdata['sea'] == True].groupby((weatherdata['sea'] == False).cumsum())
        # sections_onsea_keys = [key for key, _ in sections_onsea]
        # sections_onland = weatherdata[weatherdata['sea'] == False].groupby((weatherdata['sea'] == True).cumsum())
        # sections_onland_keys = [key for key, _ in sections_onland]

        # for _, section in sections_onland:
        #     print(section)

        # print(sections_onsea_keys)
        # print(sections_onsea.get_group(sections_onsea_keys[0]))
        # print(sections_onland_keys)
        # print(sections_onland.get_group(sections_onland_keys[0]))
        # # print(df[1])
        # i = 0
        # while i < length:
        #     df = weatherdata.loc[weatherdata['Lat'] ==  weatherdata.loc[i, 'Lat']]
        #     datetimes = df.Date.tolist()
        #     lat = df.Lat.values[0]
        #     lon = df.Lon.values[0]
        #     read_temperature = weather.temperature_range(datetimes, lat, lon)
        #     j = i + read_temperature.size
        #     temperature[i:j] = read_temperature
        #     i = j

        # weatherdata['T'] = temperature

        weatherdata.to_csv(self._weatherdatapath, encoding='utf-8', index=False)

        return weatherdata
    
    def to_json(self, filename):
        """Saves transport object data as json file"""
        with open(filename, 'w') as outfile:
            json.dump(self, outfile, cls = TransportEncoder, indent = 4)
    
    def save(self):
        """Save transport as json and weatherdata as csv"""   
        if not os.path.exists(self._folder):
            os.makedirs(self._folder)

        self.to_json(self._jsonpath)
        self.weatherdata.to_csv(self._weatherdatapath, encoding='utf-8', index=False)

class TransportEncoder(JSONEncoder):
    """
    JSONEncoder for Transport object. 
    Handles serialisation of datetime.datetime objects.
    See also: https://gist.github.com/simonw/7000493
    """
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"
    def default(self, transport):

        if isinstance(transport, Transport):
            # Serialize stops
            stops = []
            for stop in transport.stops:
                stop = stop.to_dict_serial()
                stops.append(stop)

            # Return dictionary for json file
            return {
                "type": transport.type,
                "start": transport.start.strftime("%s %s" % (
                    self.DATE_FORMAT, self.TIME_FORMAT
                )),
                "end": transport.end.strftime("%s %s" % (
                    self.DATE_FORMAT, self.TIME_FORMAT
                )),
                "route": transport.route.to_dict(),
                "stops": stops,
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
    duration_regex = re.compile(r'(\d{0,9}[:/]\d{1,2}[:/]\d{1,2})')

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
    
    def to_dict_serial(self):
        """Serialize timedelta object duration"""
        days = self.duration.days
        seconds = self.duration.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        hours = hours + days*24
        duration = '{0}:{1}:{2}'.format(hours, minutes, seconds)
        return {
            'duration': duration,
            'lat': self.lat,
            'lon': self.lon
        }

def stopDecoder(obj):
    return Stop(obj['duration'], obj['lat'], obj['lon'])

def from_json(filename):
    """Create Transport instance from json file"""   
    with open(filename) as json_file:
        json_dict = json.load(json_file, cls=TransportDecoder)
    name = os.path.splitext(os.path.basename(filename))[0]
    # Read all parameters from the dict
    transporttype = json_dict['type']
    start = json_dict['start']
    end = json_dict['end']
    # Create cargo instances
    cargo = [cargoDecoder(item) for item in json_dict['cargo']]

    if json_dict['route']['type'].lower() == 'gpx':
        routepath = os.path.join(ROUTESPATH, json_dict['route']['filename'])
        route = GPXRoute(routepath)
    elif json_dict['route']['type'].lower() == 'csv':
        routepath = os.path.join(ROUTESPATH, json_dict['route']['filename'])
        route = CSVRoute(routepath)
    elif json_dict['route']['type'].upper() == 'FTM':
        route_start = json_dict['route']['start_coordinates']
        route_end = json_dict['route']['end_coordinates']
        route = FTMRoute(route_start, route_end)
    else:
        raise Exception('Route type is not supported, try FTM or gpx')
        
    # Create stop instances
    if 'stops' in json_dict:
        stops = [stopDecoder(stop) for stop in json_dict['stops']]
    else:
        stops = []
    # Return the transport instance
    return Transport(name, transporttype, start, end, cargo, route, stops = stops)

