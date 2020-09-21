import os
from datetime import datetime, timedelta 
from math import sqrt, floor
import geopy.distance

import numpy as np
import pandas as pd

class Route:
    """Class to represent location and time of a route. """
    def __init__(self, start: datetime, end: datetime, filename: str, stops = None):
        self.start = start
        self.end = end
        self.traveltime = end - start
        self.stops = stops
        self.read(filename)
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
        df = pd.read_csv(filename, usecols=[0,1], names=['Lon', 'Lat'])
        self.coordinates_full =  df[['Lat', 'Lon']].values

    def coordinates_hourly(self):
        """Calculate the coordinates of the route for every hour"""
        # Calculate the distance from start to all stops 
        coordinates_stops = self.stops[['Lat', 'Lon']].values
        amount_stops = len(coordinates_stops[:,0])
        distance_stops = np.zeros([amount_stops, 1])
        for i in range(amount_stops):
            distance_stops[i] = geopy.distance.distance(self.coordinates_full[0,:], coordinates_stops[i]).km


        speed = np.zeros([amount_stops + 1, 1])
        stops_start = self.stops[['Start']].values

        stops_end = self.stops[['End']].values

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
            
            if stop_counter < len(self.stops.index):
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
        """Create a dataframe with time and location of route"""
        rows_list = [{'Date': self.start, 'Lat': self.coordinates_full[0][0], 'Lon': self.coordinates_full[0][1]}]
        stops_counter = 0
        date = self.start
        for i in range(len(self.coordinates)):
            # Add stops to the dataframe
            stop_added = False
            if stops_counter < len(self.stops.index):
                coords_stop = self.stops[['Lat', 'Lon']].values[stops_counter]
                if np.array_equal(self.coordinates[i,:], coords_stop):
                    # Get start time of stop and transform it to datetime object
                    stop_start = self.stops[['Start']].values[stops_counter][0]
                    stop_start = pd.Timestamp(stop_start)
                    stop_start = stop_start.to_pydatetime()
                    # Same for end time of stop
                    stop_end = self.stops[['End']].values[stops_counter][0]
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
        
        df = pd.DataFrame(rows_list)
        return df