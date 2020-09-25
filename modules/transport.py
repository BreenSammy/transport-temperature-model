import copy
from dateutil.parser import parse
from datetime import date, datetime 
import json
from json import JSONEncoder, JSONDecoder
import os
import re

import numpy as np
import pandas as pd

from modules.cargo import cargoDecoder
import modules.weather.weather as weather
from modules.route import Route, RouteGPX, stopDecoder


class Transport:
    def __init__(self, name, transporttype, start, end, cargo, route_filename, stops = None, reread_temperature = True):
        if route_filename.endswith('.gpx'):
            route_path = os.path.join('transports', name, route_filename)
            self.route = RouteGPX(start, end, route_path)
            self.route.filename = route_filename
        else:
            self.route = Route(start, end, route_filename, stops = stops)
        self.name = name
        self.type = transporttype
        self.start = start
        self.end = end
        self.cargo = cargo

        self._folder = os.path.join('transports', self.name)
        self._jsonpath = os.path.join(self._folder, self.name + '.json')
        self._weatherdatapath = os.path.join(self._folder, 'weatherdata.csv')
        
        if reread_temperature:
            self.weatherdata = self.get_weatherdata()
        elif os.path.exists(self._weatherdatapath):
            self.weatherdata = pd.read_csv( self._weatherdatapath, parse_dates = ['Date'])
        else:
            self.weatherdata = self.get_weatherdata()

        
    def get_temperature(self):
        length = len(self.route.dataframe.index)
        temperature = np.zeros([length, 1])
        lat = self.route.dataframe[['Lat']].values
        lon = self.route.dataframe[['Lon']].values
        for i in range(length):
            current_datetime = self.route.dataframe['Date'].values[i]
            current_datetime = pd.Timestamp(current_datetime)
            current_datetime = current_datetime.to_pydatetime()
            temperature[i] = weather.temperature(current_datetime, lat[i][0], lon[i][0])
        return temperature

    def get_weatherdata(self):
        temperature = self.get_temperature()
        dataframe = copy.deepcopy(self.route.dataframe)
        dataframe['T'] = temperature
        return dataframe

    def save_weatherdata(self, filename):
        """Saves transport dataframe as .csv file"""
        self.weatherdata.to_csv(filename, encoding='utf-8', index=False)
    
    def to_json(self, filename):
        """Saves transport object data as json file"""
        with open(filename, 'w') as outfile:
            json.dump(self, outfile, cls = TransportEncoder, indent = 4,)
    
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
            stops = [stop.to_dict() for stop in transport.route.stops]
            # Transform datetime instances to string
            for stop in stops:
                stop["Start"] = stop["Start"].strftime("%s %s" % (
                        self.DATE_FORMAT, self.TIME_FORMAT
                    ))
                stop["End"] = stop["End"].strftime("%s %s" % (
                        self.DATE_FORMAT, self.TIME_FORMAT
                    ))
            # Return dictionary for json file
            return {
                "Name": transport.name,
                "Type": transport.type,
                "Start": transport.start.strftime("%s %s" % (
                    self.DATE_FORMAT, self.TIME_FORMAT
                )),
                "End": transport.end.strftime("%s %s" % (
                    self.DATE_FORMAT, self.TIME_FORMAT
                )),
                "Route": {
                    "Filename": transport.route.filename,
                    "Stops":  stops
                },
                "Cargo": [item.to_dict() for item in transport.cargo]           
            }

class TransportDecoder(JSONDecoder):
    """
    JSONDecoder for Transport object. Handles deserialisation of datetime.datetime objects.
    See also: https://gist.github.com/setaou/ff98e82a9ce68f4c2b8637406b4620d1
    """
     #This an elementary date checker, rather than  ISO date checker.
    datetime_regex = re.compile(r'(\d{4}[-/]\d{2}[-/]\d{2})')

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
        else:
            return (s, end)

def load(filename):
    """Return dict from json file"""
    return json.load(filename, cls=TransportDecoder)

def from_json(filename, reread_temperature = True):
    """Create Transport instance from json file"""
    json_dict = load(filename)
    # Read all parameters from the dict
    name = json_dict['Name']
    transporttype = json_dict['Type']
    start = json_dict['Start']
    end = json_dict['End']
    # Create cargo instances
    cargo = [cargoDecoder(item) for item in json_dict['Cargo']]
    route_filename = json_dict['Route']['Filename']
    # Create stop instances
    stops = [stopDecoder(stop) for stop in json_dict['Route']['Stops']]
    # Return the transport instance
    return Transport(
        name, transporttype, start, end, cargo, route_filename, 
        stops = stops, reread_temperature = reread_temperature
        )

