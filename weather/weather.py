import os
import ftplib
from datetime import date, datetime 
import calendar
import time
import copy
import gzip

import numpy as np
import pandas as pd 
from scipy import spatial

class Weather:
    """Class to handle FTP connection to NOAA server and download weather data"""
    def __init__(self):
        retry = True
        # Try to connect to NOAA, sometimes connection fails
        while (retry):
            try:
                self.ftp = ftplib.FTP('ftp.ncei.noaa.gov')
                self.ftp.login()
                self.ftp.cwd('pub/data/noaa')
                isd_history = os.path.abspath('isd-history.csv')
                isd_inventory = os.path.abspath('isd-inventory.csv')

                # Download isd-history.txt (List of all weather stations), if not downloaded or older than one month
                if not os.path.exists(isd_history): 
                    self.download('isd-history.csv', isd_history) 
                # Check age of file with UNIX timestamp
                elif (time.time() - os.path.getmtime(isd_history)) > 2592000: 
                    self.download('isd-history.csv', isd_history) 

                if not os.path.exists(isd_inventory): 
                    self.download('isd-inventory.csv', isd_inventory) 
                # Check age of file with UNIX timestamp
                elif (time.time() - os.path.getmtime(isd_inventory)) > 2592000: 
                    self.download('isd-invenotry.csv', isd_inventory) 

                self.isd_history = pd.read_csv(isd_history, dtype={'USAF': str})
                self.isd_inventory = pd.read_csv(isd_inventory, dtype={'USAF': str})
                # Remove all stations without location
                self.isd_history = self.isd_history[self.isd_history.LAT.notnull()]

                retry = False

            except EOFError as e:
                print(e)
                print("Retrying...")
                retry = True

            except OSError as e:
                print(e)
                print("Retrying...")
                retry = True

    def download(self, source_file, target_file):
        """Downlaod a file from the ftp server and save it in the target file"""
        try:
            fh = open(target_file, 'wb+')
            self.ftp.retrbinary('RETR ' + source_file, fh.write)

        except ftplib.all_errors as e:
            print('FTP error:', e) 

            if os.path.isfile(target_file):
                os.remove(target_file)

    def find_station(self, date, lat, lon):
        """Finds nearest station by lat and lon, that has data for specified date"""

        # Remove all stations which have no records at the desired date
        date_int = int(date.strftime('%Y%m%d'))
        possible_stations = copy.deepcopy(self.isd_history)
        possible_stations = possible_stations[possible_stations.BEGIN < date_int]
        possible_stations = possible_stations[possible_stations.END > date_int]

        while True:
            coordinates = possible_stations[['LAT', 'LON']].values

            # Search for closest station
            tree = spatial.KDTree(coordinates)
            index_next_station = tree.query([(lat,lon)])[1][0]
            #range_next_station = tree.query([(lat,lon)])[0][0]

            # Get dataframe entry of closest station
            station = possible_stations[possible_stations.LAT == coordinates[index_next_station][0]]
            station = possible_stations[possible_stations.LON == coordinates[index_next_station][1]]

            # Get data inventory of closest station
            inventory = self.isd_inventory.loc[
                (self.isd_inventory['USAF'] == station['USAF'].values[0]) &
                (self.isd_inventory['YEAR'] == date.year)
                ]
            
            # Abbreviation of desired month to search pandas dataframe
            month = str.upper(calendar.month_abbr[date.month])
            # Amount of days in the desired month, used to check for full dataset
            days_in_month = calendar.monthrange(date.year, date.month)[1]

            # Check if the dataset of the station has hourly data for that month
            if inventory[month].values[0]/days_in_month > 24:
                break
            else: 
                # Remove the current station from possible stations and search again
                index = possible_stations.loc[possible_stations['USAF'] == station['USAF'].values[0]].index.item()
                possible_stations = possible_stations.drop([index])

        return station

    def download_weather_data(self, date, lat, lon):
        """Downloads weather data for the nearest station"""

        data_path = os.path.abspath('data')

        if not os.path.exists(data_path):
            os.makedirs(data_path)
        
        station = self.find_station(date, lat, lon)
        file_name = station['USAF'].values[0] + '-' + str(station['WBAN'].values[0]) + '-' + str(date.year) + '.gz'
        file_path = os.path.join(data_path, file_name)
        
        if not os.path.exists(file_path):
            self.ftp.cwd('isd-lite/' + str(date.year))
            self.download(file_name, file_path)
        else:
            print("File already downloaded")

        return file_path

w = Weather()

def temperature(datetime, lat, lon):
    """Find temperature for datetime and location"""
    date = datetime.date()
    file_path = w.download_weather_data(date, lat, lon)
    col_names = ['Year', 'Month', 'Day', 'Hour', 'T']

    df = pd.read_csv(file_path, compression='gzip', quotechar='"', delim_whitespace=True, usecols=[0,1,2,3,4], names=col_names)

    temperature = df.loc[
            (df['Year'] == datetime.year) &
            (df['Month'] == datetime.month) &
            (df['Day'] == datetime.day) &
            (df['Hour'] == datetime.hour)
            ]['T'].values[0] / 10 

    return temperature

def temperature_range(start, end, lat, lon):
    """Find temperature for a time range at stationary location"""
    date = start.date()
    file_path = w.download_weather_data(date, lat, lon)
    col_names = ['Year', 'Month', 'Day', 'Hour', 'T']

    df = pd.read_csv(file_path, compression='gzip', quotechar='"', delim_whitespace=True, usecols=[0,1,2,3,4], names=col_names)

    temperature = df.loc[
            (df['Year'] >= start.year) &
            (df['Month'] >= start.month) &
            (df['Day'] >= start.day) &
            (df['Hour'] >= start.hour) &
            (df['Year'] <= end.year) &
            (df['Month'] <= end.month) &
            (df['Day'] <= end.day) &
            (df['Hour'] <= end.hour)
            ]

    #temperature.reindex()

    return temperature




# datetime = datetime(2018, 3, 2, 5)

# print(datetime)

# weather = Weather()

# date = datetime.date()

# temperature = Weather.temperature(datetime, 44, 12)

# print(temperature)


