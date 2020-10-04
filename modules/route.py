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
from modules.weather import onsea

class FTMRoute:
    def __init__(self, start_coordinates, end_coordinates, stops = None):
        route = self._routing(start_coordinates, end_coordinates)

        self.distance = route['distance']
        self.duration = route['duration']
        self.coordinates = route['geometry']['coordinates']
  
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

    def _routing(self, start_coordinates, end_coordinates, stops = None):
        """
        Use FTM routing service. Needs connection to LRZ.
        See also: https://wiki.tum.de/display/smartemobilitaet/Routing
        """

        lat = []
        lon = []

        lat.append(start_coordinates[0])
        lat.append(end_coordinates[0])

        lon.append(start_coordinates[1])
        lon.append(end_coordinates[1])

        lon = quote(str(lon), safe='')
        lat = quote(str(lat), safe='')

        url = "http://gis.ftm.mw.tum.de/route?lat={0}&lon={1}"
        try:
            contents = urllib.request.urlopen(url.format(lat, lon)).read()
            route = json.loads(contents)
        except:
            raise Exception('No connection to FTM routing service: Connect to LRZ VPN and try again')

        return route['routes'][0]

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
        }

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
            self.dataframe = pd.read_csv(
                csvpath, usecols=[0, 1, 2], names=['Date', 'Lat', 'Lon'], header = 1, parse_dates = ['Date']
                )
        elif filename.endswith('.gpx'):
            self.dataframe = gps.dataframe(filename)
            self.dataframe.to_csv(csvpath, encoding='utf-8', index=False)

        # Transform all timestamps to UTC timezzone and drop +0:00 timezone identifier
        self.dataframe['Date'] = pd.to_datetime(self.dataframe['Date'], utc=True)
        self.dataframe['Date'] = self.dataframe['Date'].dt.tz_localize(None)
    
    def to_dict(self):
        return {
            'type': 'gpx',
            'filename': os.path.basename(self.filename)
        }

    def waypoints(self, start, end):
        """Get a dataframe with date and location for every hour."""
        waypoints_list = []
        
        # Finding dataframe entry closest to start date and adding it
        start_index = self.dataframe['Date'].sub(start).abs().idxmin()
        waypoints_list.append(self.dataframe.iloc[[start_index]])

        time = start + timedelta(hours = 1)

        # Add timestamps for every hour, if next timesamp is longer than one hour, take next
        while time < end:
            waypoints = self.dataframe[self.dataframe.Date.between(time, end)]
            waypoints_list.append(waypoints.head(1))
            time = waypoints['Date'].iloc[0] + timedelta(hours = 1)

        # Finding dataframe entry closest to end date and adding it
        end_index = self.dataframe['Date'].sub(end).abs().idxmin()
        waypoints_list.append(self.dataframe.iloc[[end_index]])

        waypoints = pd.concat(waypoints_list)

        waypoints.index = range(len(waypoints))
        
        return waypoints

class CSVRoute:
    def __init__(self, filename: str):
        self.filename = filename

        self.dataframe = pd.read_csv(
                filename, usecols=[0, 1, 2], names=['Date', 'Lat', 'Lon'], header = 1, parse_dates = ['Date']
                )

        self.start = self.dataframe['Date'].iloc[0]
        self.end = self.dataframe['Date'].iloc[-1]

    def waypoints(self, start = None):
        """Get dataframe with hourly waypoints along route

            Args:
                start: Use custom start datetime for waypoints
                
            Returns:
                waypoints: DataFrame with hourly dates and coordinates of route 
        """
      
        filename = os.path.splitext(self.filename)[0] + '_waypoints.csv'
        if os.path.exists(filename):
            waypoints = pd.read_csv(filename, parse_dates = ['Date'])
        else:
            waypoints = self._create_waypoints()

        # Save waypoints for faster access
        waypoints.to_csv(filename, encoding='utf-8', index=False)

        if start != None:
            add_seconds(waypoints)
            seconds_list = waypoints.seconds.tolist()
            new_dates = [start + timedelta(seconds = seconds) for seconds in seconds_list]
            waypoints['Date'] = new_dates
            waypoints = waypoints.drop(columns = ['seconds'])

        return waypoints

    def _create_waypoints(self):
        waypoints_list = []

        waypoints_list.append(self.dataframe.head(1))
        timestamp = self.start
        i = 1
        while (self.end - timestamp) > timedelta(hours = 1):
            nexttimestamp = self.dataframe.loc[i, 'Date']

            timedelta_nextpoint = nexttimestamp - timestamp

            # Loop over dataframe until latesttime is reached
            if timedelta_nextpoint > timedelta(hours = 1): 
                # Create a vector between next two points, curvature of earth is neglected due to short distances
                current_coordinates = self.dataframe.loc[i - 1, ['Lat', 'Lon']].values
                next_coordinates = self.dataframe.loc[i, ['Lat', 'Lon']].values
                direction = direction_crossover(current_coordinates, next_coordinates)

                # Create waypoints for every hour along the direction
                number_points = floor(timedelta_nextpoint / timedelta(hours = 1))
                step = direction/number_points
                timestep = timedelta_nextpoint / number_points
                timestep.microsecond = 0

                for j in range(number_points-1):
                    df_dict = {
                        'Date':  (timestamp + (j + 1)*timestep).replace(microsecond = 0, nanosecond = 0),
                        'Lat': current_coordinates[0] + (j + 1)*step[0],
                        'Lon': current_coordinates[1] + (j+1)*step[1]
                    }
                    df = pd.DataFrame(df_dict, index = [0])
                    waypoints_list.append(df)

                waypoints_list.append(self.dataframe.loc[[i], :])
                timestamp = self.dataframe['Date'].iloc[i]
            i += 1

        waypoints = pd.concat(waypoints_list)
        waypoints.index = range(len(waypoints))
        return waypoints

    def to_dict(self):
        return {
            'type': 'csv',
            'filename': os.path.basename(self.filename)
        }          

def check_onsea(dataframe):
    """Check for all coordinates in dataframe, whether they are on the sea or not"""
    coordinates = dataframe[['Lat', 'Lon']].values

    result = [onsea(coordinates[i][0], coordinates[i][1]) for i in range(coordinates.shape[0])]

    return result

def check_crossover(longitude_start, longitude_end):
    """Check if -180 to +180 crossover appears between two coordinates"""
    if np.sign(longitude_start) == np.sign(longitude_end):
        return False
    elif (abs(longitude_start) + abs(longitude_end)) > 180:
        return True

def direction_crossover(coordinates_start, coordinates_end):
    """Calculate the vector between two coordinates. Handles edge case of -180 to +180 crossover"""

    if check_crossover(coordinates_start[1], coordinates_end[1]):
        if np.sign(coordinates_start[1]) == -1:
            coordinates_start[1] += 360
        else:
            coordinates_end[1] += 360

    direction_lat = coordinates_end[0] - coordinates_start[0]
    direction_lon = coordinates_end[1] - coordinates_start[1]

    return np.array([direction_lat, direction_lon])

def add_seconds(dataframe):
    """Add a column with total passed seconds to dataframe with ['Date'] column"""
    start = dataframe['Date'].iloc[0]
    length = len(dataframe.index)
    seconds = np.zeros(length)

    for i in range(length):
        passed_timedelta = dataframe['Date'].iloc[i] - start
        seconds[i] = passed_timedelta.total_seconds()

    dataframe.insert(1, 'seconds', seconds, True) 