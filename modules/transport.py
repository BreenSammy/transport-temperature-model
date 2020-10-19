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
from modules.route import routeDecoder, stopDecoder

matplotlib.use('Agg')

class Transport:
    def __init__(self, path, transporttype, start, initial_temperature, cargo, route):
        self.path = path
        self.type = transporttype
        self.start = start
        self.initial_temperature = initial_temperature
        self.cargo = cargo
        self.route = route

        self._jsonpath = os.path.join(self.path, 'transport.json')
        self._weatherdatapath = os.path.join(self.path, 'weatherdata.csv')
        self._postprocesspath = os.path.join(self.path, 'postProcessing') 
        self._plotspath = os.path.join(self.path, 'plots')

        if not os.path.exists(self._postprocesspath):
            os.makedirs(self._postprocesspath)
        if not os.path.exists(self._plotspath):
            os.makedirs(self._plotspath)
        
        if os.path.exists(self._weatherdatapath):
            self.weatherdata = pd.read_csv(self._weatherdatapath, parse_dates = ['Date'])
            start = self.weatherdata['Date'].iloc[0]
        else:
            self.weatherdata = self.get_weatherdata()
        # Reload weatherdata, if start time is not the same or 
        # traveltime differs by more than 10 minutes     
        if self.start != start or abs(self.route.traveltime() - self.traveltime()) > 0.05*self.traveltime():
            self.weatherdata = self.get_weatherdata()

        # Write start of weatherdata back to transport
        self.start = self.weatherdata['Date'].iloc[0]

        self.plot_waypoints()
    
    def traveltime(self):
        traveltime = self.weatherdata['Date'].iloc[-1] - self.weatherdata['Date'].iloc[0] 
        return traveltime.total_seconds()

    def plot_waypoints(self, tiles = 'cartodb_positron'):
        """Plot waypoints on OSM map and save as interactive html"""
        xy = self.weatherdata[['Lon', 'Lat']].values
        # Plot the path as red dots connected by a blue line
        plt.plot(xy[:,0], xy[:,1], 'r.')
        plt.plot(xy[:,0], xy[:,1], 'b')

        filename = os.path.join(self._plotspath, 'route.html')
        mplleaflet.save_html(fileobj=filename, tiles = tiles)
        
    def get_weatherdata(self):
        """Get weatherdata for all waypoints along the route"""
        print('Gathering weatherdata for all waypoints')
        weatherdata = self.route.waypoints(self.start)
        datetimes = weatherdata.Date.tolist()
        lat = weatherdata.Lat.values
        lon = weatherdata.Lon.values
        # Read temperature from NOAA server and interpolate missing values
        weatherdata['T'] = weather.waypoints_temperature(datetimes, lat, lon)
        weatherdata['T'] = weatherdata['T'].interpolate()
        
        weatherdata.to_csv(self._weatherdatapath, encoding='utf-8', index=False)

        return weatherdata
    
    def to_json(self, filename):
        """Saves transport object data as json file"""
        with open(filename, 'w') as outfile:
            json.dump(self, outfile, cls = TransportEncoder, indent = 4)
    
    def save(self):
        """Save transport as json and weatherdata as csv"""   
        if not os.path.exists(self.path):
            os.makedirs(self.path)

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
            if hasattr(transport.route, 'stops'):
                for stop in transport.route.stops:
                    stop = stop.to_dict()
                    stops.append(stop)

            # Return dictionary for json file
            return {
                "type": transport.type,
                "start": transport.start.strftime("%s %s" % (
                    self.DATE_FORMAT, self.TIME_FORMAT
                )),
                "temperature": transport.initial_temperature,
                "route": transport.route.to_dict(),
                "stops": stops,
                "cargo": [item.to_dict() for item in transport.cargo]           
            }

class TransportDecoder(JSONDecoder):
    """
    JSONDecoder for Transport object. Handles deserialisation of datetime.datetime objects.
    See also: https://gist.github.com/setaou/ff98e82a9ce68f4c2b8637406b4620d1
    """
    # This an elementary date checker, rather than  ISO date checker.
    datetime_regex = re.compile(r'(\d{4}[-/]\d{2}[-/]\d{2})')
    # Duration checker
    duration_regex = re.compile(r'(\d{0,9}[:/]\d{1,2}[:/]\d{1,2})')
    # Timezone checker
    timezone_regex = re.compile(r'(?:[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])')

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
        elif cls.timezone_regex.match(s):
            return (parse_timezone(s), end)
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

def parse_timezone(timezone_str):
    """Parse a timezone format like +04:30 and return fitting timedelta"""
    hours = int(timezone_str[1:3])
    minutes = int(timezone_str[4:6])
    sign = timezone_str[0]
    if sign == '+':
        return timedelta(hours = hours, minutes = minutes)
    else:
         return timedelta(hours = -hours, minutes = -minutes)

def from_json(filepath):
    """Create Transport instance from json file"""   
    with open(filepath) as json_file:
        json_dict = json.load(json_file, cls=TransportDecoder)
    path = os.path.dirname(filepath)
    # Read all parameters from the dict
    transporttype = json_dict['type']
    start = json_dict['start']
    initial_temperature = json_dict['temperature']
    # Create cargo instances
    cargo = [cargoDecoder(item) for item in json_dict['cargo']]
    # Create route, first check if from file, else use FTM routing
    route = routeDecoder(json_dict['route'], path, stops = json_dict['stops'])   
    # Create stop instances
    if 'stops' in json_dict:
        stops = [stopDecoder(stop) for stop in json_dict['stops']]
    else:
        stops = []
    # Create route, first check if from file, else use FTM routing
    route = routeDecoder(json_dict['route'], path, stops = stops)
    # Return the transport instance
    return Transport(path, transporttype, start, initial_temperature, cargo, route)