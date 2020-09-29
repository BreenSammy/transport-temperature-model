from copy import deepcopy
from dateutil.parser import parse as dateutilparser
from datetime import datetime, timedelta 
import json
from math import sqrt, floor
import os
import urllib.request
from urllib.parse import quote

import geopy.distance
import numpy as np
import pandas as pd

import modules.gps as gps

class FTMRoute:
    def __init__(self, start_coordinates, end_coordinates, stops = None):
        route = self._routing(start_coordinates, end_coordinates)

        self.distance = route['distance']
        self.duration = route['duration']
        self.coordinates = route['geometry']['coordinates']
  
    def _routing(self, start_coordinates, end_coordinates, stops = None):
        """
        Use FTM routing service for finding route. Needs connection to LRZ.
        See also: https://wiki.tum.de/display/smartemobilitaet/Routing"""

        lat = []
        lon = []

        lat.append(start_coordinates[0])
        lat.append(end_coordinates[0])

        lon.append(start_coordinates[1])
        lon.append(end_coordinates[1])

        lon = quote(str(lon), safe='')
        lat = quote(str(lat), safe='')

        url = "http://gis.ftm.mw.tum.de/route?lat={0}&lon={1}"
        contents = urllib.request.urlopen(url.format(lat, lon)).read()
        route = json.loads(contents)

        return route['routes'][0]

    def start(self):
        """Get the coordinates of start of route"""
        coords_start = deepcopy(self.coordinates[0])
        # URL returns coordinates in [Lon, Lat], convention is [Lat, Lon]
        coords_start.reverse()
        return coords_start
    
    def end(self):
        """Get the coordinates of end of route"""
        coords_end = deepcopy(self.coordinates[-1])
        # URL returns coordinates in [Lon, Lat], convention is [Lat, Lon]
        coords_end.reverse()
        return coords_end

    def waypoints(self, start, stops):
        """Get a dataframe with date and location for hourly waypoints along route"""

        date = start
        coords_start = self.start()
        
        waypoints_list = []
        waypoints_list.append(
            {'Date': start, 'Lat': coords_start[0], 'Lon': coords_start[1]}
        )

        # Add waypoints between stops
        for stop in stops:
            waypoints_list, date, passed_time = self._add_hourly_waypoints(
                waypoints_list, date, coords_start, stop.coordinates()
                )

            # Add hourly waypoints at location of stop
            start_stop = date + timedelta(seconds = round(passed_time))
            end_stop = start_stop + stop.duration

            while (end_stop - date) > timedelta(hours = 1):
                date = date + timedelta(seconds = round(passed_time))
                waypoints_list.append({'Date': date, 'Lat': stop.lat, 'Lon': stop.lon})
                passed_time = 3600
                
            waypoints_list.append({'Date': end_stop, 'Lat': stop.lat, 'Lon': stop.lon})
            
            # Next start are coordinates of stop
            coords_start = stop.coordinates()
            # Next date to start with is date of end of stop
            date = end_stop

        # Add waypoints for rest of route
        coords_end = self.end()
        waypoints_list, date, passed_time = self._add_hourly_waypoints(waypoints_list, date, coords_start, coords_end)

        # Add waypoint for end of route
        end = date + timedelta(seconds = round(passed_time))
        waypoints_list.append(
            {'Date': end, 'Lat': coords_end[0], 'Lon': coords_end[1]}
            )

        return pd.DataFrame(waypoints_list)

    def _add_hourly_waypoints(self, waypoints_list, date, start_coordinates, end_coordinates):
        """Add hourly waypoints of a route to a list"""
        
        route = self._routing(start_coordinates, end_coordinates)
        duration = route['legs'][0]['annotation']['duration']

        passed_time = 0
        i = 0
        for i in range(len(duration)):
            passed_time = duration[i] + passed_time
            i = i + 1
            if passed_time > 3600:
                    date = date + timedelta(seconds = round(passed_time))
                    waypoints_list.append(
                        {
                        'Date': date, 
                        'Lat': route['geometry']['coordinates'][i][1], 
                        'Lon': route['geometry']['coordinates'][i][0]
                        }
                    )
                    passed_time = 0

        return waypoints_list, date, passed_time

    def to_dict(self):
        return {
            "type": "FTM",
            "start_coordinates": self.start(),
            "end_coordinates": self.end(),
        },

    def saveJSON(self, filename):
        with open(filename, 'w') as json_file:
            json.dump(self, json_file, default=lambda o: o.__dict__, indent = 4 )

class GPXRoute:
    """Class for routes created from gpx file with timestamps"""
    def __init__(self, filename):
        self.filename = filename
        # Reading point data from .gpx file takes long, so caching the read data in .csv file 
        csvpath = os.path.splitext(filename)[0] + '.csv'
        if os.path.exists(csvpath):
            self.dataframe_full = pd.read_csv(
                csvpath, usecols=[0, 1, 2], names=['Date', 'Lat', 'Lon'], header = 1, parse_dates = ['Date']
                )
        elif filename.endswith('.gpx'):
            self.dataframe_full = gps.dataframe(filename)
            self.dataframe_full.to_csv(csvpath, encoding='utf-8', index=False)

        # Transform all timestamps to UTC timezzone and drop +0:00 timezone identifier
        self.dataframe_full['Date'] = pd.to_datetime(self.dataframe_full['Date'], utc=True)
        self.dataframe_full['Date'] = self.dataframe_full['Date'].dt.tz_localize(None)
    
    def to_dict(self):
        return {
            'type': 'gpx' 
        }

    def waypoints(self, start, end):
        """Get a dataframe with date and location for every hour."""
        waypoints_list = []
        
        # Finding dataframe entry closest to start date and adding it
        start_index = self.dataframe_full['Date'].sub(start).abs().idxmin()
        waypoints_list.append(self.dataframe_full.iloc[[start_index]])

        time = start + timedelta(hours = 1)

        # Add timestamps for every hour, if next timesamp is longer than one hour, take next
        while time < end:
            waypoints = self.dataframe_full[self.dataframe_full.Date.between(time, end)]
            waypoints_list.append(waypoints.head(1))
            time = waypoints['Date'].iloc[0] + timedelta(hours = 1)

        # Finding dataframe entry closest to end date and adding it
        end_index = self.dataframe_full['Date'].sub(end).abs().idxmin()
        waypoints_list.append(self.dataframe_full.iloc[[end_index]])

        waypoints = pd.concat(waypoints_list)

        waypoints.index = range(len(waypoints))
        
        return waypoints

