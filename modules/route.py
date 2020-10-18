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
    def __init__(self, start_coordinates, end_coordinates):
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

    def waypoints(self, start, stops = []):
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

    def _routing(self, start_coordinates, end_coordinates):
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

class FileRoute:
    def __init__(self, filename: str, trimstart, trimend, timezone):
        self.filename = filename
        self.trimstart = trimstart
        self.trimend = trimend
        self.timezone = timezone

        if filename.endswith('.csv'):
            self.dataframe = self.dataframe_from_csv(filename)
        elif filename.endswith('.gpx'):
            # Cache the coordinates in csv format for faster access
            csvpath = os.path.splitext(filename)[0] + '.csv'
            if os.path.exists(csvpath):
                self.dataframe = self.dataframe_from_csv(csvpath)
            else:
                self.dataframe = gps.dataframe(filename)
                self.dataframe.to_csv(csvpath, encoding='utf-8', index=False)
        else:
            raise ValueError('Supported file formats for routes are gpx or csv')

    def dataframe_from_csv(self, csvpath):
        return pd.read_csv(
                csvpath, usecols=[0, 1, 2], names=['Date', 'Lat', 'Lon'], header = 1, parse_dates = ['Date']
                )

    def waypoints(self, start = None, stops = []):
        """Get dataframe with hourly waypoints along route

            Args:
                start: Use custom start datetime for waypoints
                
            Returns:
                waypoints: DataFrame with hourly dates and coordinates of route 
        """
        waypoints = self._create_waypoints()
        
        # Convert the timestamps to UTC
        waypoints['Date'] = waypoints['Date'] - self.timezone

        if start != None:
            add_seconds(waypoints)
            seconds_list = waypoints.seconds.tolist()
            new_dates = [start + timedelta(seconds = seconds) for seconds in seconds_list]
            waypoints['Date'] = new_dates
            waypoints = waypoints.drop(columns = ['seconds'])

        return waypoints

    def _create_waypoints(self):

        waypoints_list = []

        start = self.dataframe['Date'].iloc[0]
        end = self.dataframe['Date'].iloc[-1]

        # Trim timedeltas from start and end, if position data has to be trimmed
        start = start + self.trimstart
        end = end - self.trimend
        self.dataframe = self.dataframe[self.dataframe.Date.between(start, end)]
        self.dataframe.index = range(len(self.dataframe))

        waypoints_list.append(self.dataframe.head(1))
        waypoints_list[0].at[0,'Lon'] = normalize_longitude(waypoints_list[0].at[0,'Lon'])
            
        timestamp = start
        i = 1
        while (end - timestamp) > timedelta(hours = 1):
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
                        'Lon': normalize_longitude(current_coordinates[1] + (j+1)*step[1])
                    }
                    df = pd.DataFrame(df_dict, index = [0])
                    waypoints_list.append(df)

                waypoints_list.append(self.dataframe.loc[[i], :])
                waypoints_list[-1].at[i,'Lon'] = normalize_longitude(waypoints_list[-1].at[i,'Lon'])
                timestamp = self.dataframe['Date'].iloc[i]

            i += 1

        waypoints = pd.concat(waypoints_list)
        waypoints.index = range(len(waypoints))
        return waypoints

    def to_dict(self):
        return {
            'filename': os.path.basename(self.filename),
            'timezone': timezone_to_string(self.timezone),
            'trimstart': duration_to_string(self.trimstart),
            'trimend': duration_to_string(self.trimend)
        }          

class Stop:
    """Class to represent a stop during transport."""
    def __init__(self, duration, lat, lon):
        self.duration = duration
        self.lat = lat
        self.lon = lon

    def coordinates(self):
        return np.array([self.lat, self.lon])

    def to_dict(self):
        """Return dict of Stop instance, serializes duration"""
        return {
            'duration': duration_to_string(self.duration),
            'lat': self.lat,
            'lon': self.lon
        }

def stopDecoder(obj):
    return Stop(obj['duration'], obj['lat'], obj['lon'])

def duration_to_string(duration):
    """Convert timedelta object to string in format H:M:S, e.g. 03:20:30"""
    days = duration.days
    seconds = duration.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    hours = hours + days*24
    duration = '{:02}:{:02}:{:02}'.format(hours, minutes, seconds)
    return duration

def timezone_to_string(timezone):
    """Convert a timedelta respresenting a timezone offset to a string, e.g. +09:30"""
    seconds_timezone = timezone.total_seconds()
    sign = np.sign(seconds_timezone)
    if sign == -1:
        sign = '-'
    else:
        sign = '+'
    seconds_timezone = abs(seconds_timezone)
    hours, minutes = divmod(seconds_timezone, 3600)
    timezone = sign + '{:02}:{:02}'.format(int(hours), int(minutes))
    return timezone

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
        # Add 360 degrees to negative longitude to compensate for -180 + 180 crossoover
        if np.sign(coordinates_start[1]) == -1:
            coordinates_start[1] += 360
        else:
            coordinates_end[1] += 360

    direction_lat = coordinates_end[0] - coordinates_start[0]
    direction_lon = coordinates_end[1] - coordinates_start[1]

    return np.array([direction_lat, direction_lon])

def normalize_longitude(longitude):
    """Convert coordinates with absolute values over 180°:

            >>> normalize_longitude(-182)
            178
            >>> normalize_longitude(182)
            -178
    """
    if abs(longitude) > 180:
        return longitude - 360 * np.sign(longitude)
    else:
        return longitude

def add_seconds(dataframe):
    """Add a column with total passed seconds to dataframe with ['Date'] column"""
    start = dataframe['Date'].iloc[0]
    length = len(dataframe.index)
    seconds = np.zeros(length)

    for i in range(length):
        passed_timedelta = dataframe['Date'].iloc[i] - start
        seconds[i] = passed_timedelta.total_seconds()

    dataframe.insert(1, 'seconds', seconds, True) 