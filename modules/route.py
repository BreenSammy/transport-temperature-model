from dateutil.parser import parse as dateutilparser
from datetime import datetime, timedelta 
from math import sqrt, floor
import os

import geopy.distance
import numpy as np
import pandas as pd

import modules.gps as gps

class Route:
    """Class to represent location and time of a route. """
    def __init__(self, start: datetime, end: datetime, filename: str, stops = None):
        self.start = start
        self.end = end
        self.filename = filename
        self.stops = stops
        self.traveltime = end - start
        self._df_stops = pd.DataFrame([item.to_dict() for item in stops])
        self.coordinates_full = self.read(filename)
        self.coordinates_start = self.coordinates_full[0]
        self.coordinates_end = self.coordinates_full[-1]
        self.distance = self.calc_distance()
        self.coordinates = self.coordinates_hourly()
        self.dataframe = self.get_dataframe()

    def calc_distance(self):
        """Calculate the total distance of the route"""
        distance = 0.0
        for i in range(len(self.coordinates_full) - 1):
            coords_1 = self.coordinates_full[i]
            coords_2 = self.coordinates_full[i+1]
            distance = distance + geopy.distance.distance(coords_1, coords_2).km

        return distance

    def read(self, filename: str):
        """Read coordinates from a .csv file"""
        routepath = os.path.join('routes', filename)
        df = pd.read_csv(routepath, usecols=[0,1], names=['Lon', 'Lat'])
        return df[['Lat', 'Lon']].values

    def coordinates_hourly(self):
        """Calculate the coordinates of the route for every hour"""
        # Calculate the distance from start to all _df_stops 
        coordinates_stops = self._df_stops[['Lat', 'Lon']].values
        amount_stops = len(coordinates_stops[:,0])
        distance_stops = np.zeros([amount_stops, 1])
        for i in range(amount_stops):
            distance_stops[i] = geopy.distance.distance(self.coordinates_full[0,:], coordinates_stops[i]).km


        speed = np.zeros([amount_stops + 1, 1])
        stops_start = self._df_stops[['Start']].values

        stops_end = self._df_stops[['End']].values

        stop_start = stops_start[0][0]
        stop_start = pd.Timestamp(stop_start)
        stop_start = stop_start.to_pydatetime()

        td = stop_start - self.start
        td = td / timedelta(hours = 1)
        speed[0] = distance_stops[0] / td

        for i in range(amount_stops-1):
            distance_between_stops = distance_stops[i+1] - distance_stops[i]

            stop_start = stops_start[i+1][0]
            stop_start = pd.Timestamp(stop_start)
            stop_start = stop_start.to_pydatetime()
            stop_end = stops_end[i][0]
            stop_end = pd.Timestamp(stop_end)
            stop_end = stop_end.to_pydatetime()

            td = stop_start - stop_end
            td = td / timedelta(hours = 1)
            speed[i+1] = distance_between_stops[0] / td

        stop_end = stops_end[-1][0]
        stop_end = pd.Timestamp(stop_end)
        stop_end = stop_end.to_pydatetime()

        td = self.end - stop_end
        td = td / timedelta(hours = 1)
        speed[-1] = (self.distance - distance_stops[-1]) / td

        average_speed = np.average(speed)

        # Initialize variables for next loop
        coordinates = np.zeros([floor(self.distance/average_speed) + amount_stops, 2])
        counter = 0
        stop_counter = 0
        distance = 0.0 # Traveld distance between saved coordinates
        total_distance = 0.0 # Total traveld distance

        for i in range(len(self.coordinates_full) - 1):
            coords_1 = self.coordinates_full[i]
            coords_2 = self.coordinates_full[i+1]

            distance_1_to_2 = geopy.distance.distance(coords_1, coords_2).km
            distance = distance + distance_1_to_2
            total_distance = total_distance + distance_1_to_2
            
            if stop_counter < len(self._df_stops.index):
                if total_distance > distance_stops[stop_counter]:
                    coordinates[counter,:] = coordinates_stops[stop_counter]
                    stop_counter = stop_counter + 1
                    counter = counter + 1
                    distance = 0

            # Save coordinates after one hour of traveltime
            if distance > speed[stop_counter] * 1:
                coordinates[counter, :] = coords_2
                counter = counter + 1
                distance = 0

        # Remove all rows with zero entries from array
        coordinates = coordinates[~np.all(coordinates == 0, axis=1)]

        return coordinates

    def get_dataframe(self):
        """Create a dataframe with time and location of route for every hour"""
        rows_list = []
        rows_list.append(
            {'Date': self.start, 'Lat': self.coordinates_full[0][0], 'Lon': self.coordinates_full[0][1]}
        )
        stops_counter = 0
        date = self.start
        for i in range(len(self.coordinates)):
            # Add _df_stops to the dataframe
            stop_added = False
            if stops_counter < len(self._df_stops.index):
                coords_stop = self._df_stops[['Lat', 'Lon']].values[stops_counter]
                if np.array_equal(self.coordinates[i,:], coords_stop):
                    # Get start time of stop and transform it to datetime object
                    stop_start = self._df_stops[['Start']].values[stops_counter][0]
                    stop_start = pd.Timestamp(stop_start)
                    stop_start = stop_start.to_pydatetime()
                    # Same for end time of stop
                    stop_end = self._df_stops[['End']].values[stops_counter][0]
                    stop_end = pd.Timestamp(stop_end)
                    stop_end = stop_end.to_pydatetime()

                    # Add row for start of stop
                    row_stop_start = {'Date': stop_start, 'Lat': coords_stop[0], 'Lon': coords_stop[1]}
                    rows_list.append(row_stop_start)

                    # Add row for every full hour of stop
                    time = stop_start + timedelta(hours = 1)
                    while time < stop_end:
                        row = {'Date': time, 'Lat': coords_stop[0], 'Lon': coords_stop[1]}
                        rows_list.append(row)
                        time = time + timedelta(hours = 1)
                            
                    # Add row for end of stop
                    row_stop_end = {'Date': stop_end, 'Lat': coords_stop[0], 'Lon': coords_stop[1]}
                    rows_list.append(row_stop_end)

                    stops_counter = stops_counter + 1
                    date = stop_end
                    stop_added = True
            # If current coordinates are not a stop add them with a timedelta of one hour
            if stop_added == False:
                date = date + timedelta(hours = 1)
                row = {'Date': date, 'Lat': self.coordinates[i][0], 'Lon': self.coordinates[i][1]}
                rows_list.append(row)
        # Add row for end
        last_row = {'Date': self.end, 'Lat': self.coordinates_full[-1][0], 'Lon': self.coordinates_full[-1][1]}
        rows_list.append(last_row)

        df = pd.DataFrame(rows_list)
        return df

class RouteGPX:
    """Class for routes created from gpx file with timestamps"""
    def __init__(self, start, end, filename):
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

        self.start = start
        self.end = end

        self.stops = []

        self.dataframe = self.get_dataframe()

    def get_dataframe(self):
        """Get a dataframe with date and location for every hour."""
        df_list = []
        
        # Finding dataframe entry closest to start date and adding it
        start_index = self.dataframe_full['Date'].sub(self.start).abs().idxmin()
        df_list.append(self.dataframe_full.iloc[[start_index]])

        time = self.start + timedelta(hours = 1)

        # Add timestamps for every hour, if next timesamp is longer than one hour, take next
        while time < self.end:
            df = self.dataframe_full[self.dataframe_full.Date.between(time, self.end)]
            df_list.append(df.head(1))
            time = df['Date'].iloc[0] + timedelta(hours = 1)

        # Finding dataframe entry closest to end date and adding it
        end_index = self.dataframe_full['Date'].sub(self.end).abs().idxmin()
        df_list.append(self.dataframe_full.iloc[[end_index]])

        df = pd.concat(df_list)

        df.index = range(len(df))
        
        return df

class Stop:
    """Class to represent a stop on the route."""
    def __init__(self, start, end, lat, lon):
        self.start = start
        self.end = end
        self.lat = lat
        self.lon = lon

    def to_dict(self):
        return {
            'Start': self.start,
            'End': self.end,
            'Lat': self.lat,
            'Lon': self.lon
        }

def stopDecoder(obj):
    return Stop(obj['Start'], obj['End'], obj['Lat'], obj['Lon'])