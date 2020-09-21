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
        # Travel speed in km/h
        speed = 80

        # Initialize variables
        coordinates = np.zeros([floor(self.distance/speed), 2])
        counter = 0
        distance = 0.0

        for i in range(len(self.coordinates_full) - 1):
            coords_1 = self.coordinates_full[i]
            coords_2 = self.coordinates_full[i+1]
            distance = distance + geopy.distance.distance(coords_1, coords_2).km

            # Save coordinates after one hour of traveltime
            if distance > speed * 1:
                coordinates[counter, :] = coords_2
                counter = counter + 1
                distance = 0

        return coordinates

    def get_dataframe(self):
        """Create a dataframe with time and location of route"""
        rows_list = [{'Date': self.start, 'Lat': self.coordinates_full[0][0], 'Lon': self.coordinates_full[0][1]}]

        date = self.start
        for i in range(len(self.coordinates)):
            date = date + timedelta(hours = 1)
            row = {'Date': date, 'Lat': self.coordinates[i][0], 'Lon': self.coordinates[i][1]}
            rows_list.append(row)
        
        df = pd.DataFrame(rows_list)

        return df