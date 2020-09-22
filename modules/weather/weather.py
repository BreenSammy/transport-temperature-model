import calendar
import copy
from datetime import date, datetime, timedelta 
import ftplib
import os
import time

import geopy.distance
import numpy as np
import pandas as pd 
from scipy import spatial

class Station:
    """
    Class to represent a weather station of NOAA ISD database. 
    Handles FTP connection to NOAA server and downloads ISD weather data.
    ISD:  https://www.ncdc.noaa.gov/isd
    Data: https://www.ncei.noaa.gov/pub/data/noaa/
    """
    def __init__(self, input_date, lat, lon):
        self.date = input_date
        self.lat_query = lat
        self.lon_query = lon

        isd_history = os.path.abspath('isd-history.csv')
        isd_inventory = os.path.abspath('isd-inventory.csv')

        # Download isd-history.txt (List of all weather stations), if not downloaded or older than one month
        if not os.path.exists(isd_history): 
            self._download('isd-history.csv', isd_history) 
        # Check age of file with UNIX timestamp
        elif (time.time() - os.path.getmtime(isd_history)) > 2592000: 
            self._download('isd-history.csv', isd_history) 
        # Same for isd-inventory.txt (Gives information about amount of measurements at station)
        if not os.path.exists(isd_inventory): 
            self._download('isd-inventory.csv', isd_inventory) 
        # Check age of file with UNIX timestamp
        elif (time.time() - os.path.getmtime(isd_inventory)) > 2592000: 
            self._download('isd-invenotry.csv', isd_inventory) 

        # Save them as dataframe for easy acess
        self.isd_history = pd.read_csv(isd_history, dtype={'USAF': str, 'WBAN': str})
        self.isd_inventory = pd.read_csv(isd_inventory, dtype={'USAF': str, 'WBAN': str})
        # Remove all stations without location
        self.isd_history = self.isd_history[self.isd_history.LAT.notnull()]

        self._find(self.date, self.lat_query, self.lon_query)
        self._download_weatherdata()

    def _connect(self):
        """Conncect to NOAA server with ftp connection. Retry to establish connection if it."""
        retry = True
        while (retry):
            try:
                self._ftp = ftplib.FTP('ftp.ncei.noaa.gov')
                self._ftp.login()
                self._ftp.cwd('pub/data/noaa')
                retry = False

            except EOFError as e:
                print(e)
                print("Connection to NOAA server failed. Retrying to connect.")
                retry = True

            except OSError as e:
                print(e)
                print("Connection to NOAA server failed. Retrying to connect.")
                retry = True

    def _download(self, source_file: str, target_file: str):
        """Downlaod a file from the ftp server and save it in the target file"""
        try:
            self._connect()
            fh = open(target_file, 'wb+')
            self._ftp.retrbinary('RETR ' + source_file, fh.write)

        except ftplib.all_errors as e:
            print('FTP error:', e) 

            if os.path.isfile(target_file):
                os.remove(target_file)

    def _find(self, input_date: date, lat: float, lon: float):
        """Finds nearest station by lat and lon, that has data for specified date"""
        # Remove all stations which have no records at the desired date
        date_int = int(input_date.strftime('%Y%m%d'))
        possible_stations = copy.deepcopy(self.isd_history)
        possible_stations = possible_stations[possible_stations.BEGIN < date_int]
        possible_stations = possible_stations[possible_stations.END > date_int]

        while True:
            coordinates = possible_stations[['LAT', 'LON']].values

            # Search for closest station
            tree = spatial.KDTree(coordinates)
            index_next_station = tree.query([(lat,lon)])[1][0]

            # Get dataframe entry of closest station
            station = possible_stations[possible_stations.LAT == coordinates[index_next_station][0]]
            station = possible_stations[possible_stations.LON == coordinates[index_next_station][1]]

            # Get data inventory of closest station
            inventory = self.isd_inventory.loc[
                (self.isd_inventory['USAF'] == station['USAF'].values[0]) &
                (self.isd_inventory['YEAR'] == input_date.year)
                ]
            
            # Abbreviation of desired month to search pandas dataframe
            month = str.upper(calendar.month_abbr[input_date.month])
            # Amount of days in the desired month, used to check for full dataset
            days_in_month = calendar.monthrange(input_date.year, input_date.month)[1]

            # Check if the dataset of the station has hourly data for that month
            if inventory[month].values[0]/days_in_month > 24:
                break
            else: 
                # Remove the current station from possible stations and search again
                index = possible_stations.loc[possible_stations['USAF'] == station['USAF'].values[0]].index.item()
                possible_stations = possible_stations.drop([index])

        self.USAF = station['USAF'].values[0]
        self.WBAN = station['WBAN'].values[0]
        self.lat = station['LAT'].values[0]
        self.lon = station['LON'].values[0]

        coords_station = np.array([self.lat, self.lon])
        coords_query = np.array([self.lat_query, self.lon_query])
        self.distance = geopy.distance.distance(coords_station, coords_query).km
        print(self.distance)

    def _download_weatherdata(self):
        """Downloads weather data for the station"""

        datapath = os.path.abspath('weatherdata')
        
        if not os.path.exists(datapath):
            os.makedirs(datapath)

        self.filename = self.USAF + '-' + self.WBAN + '-' + str(self.date.year) + '.gz'
        self.filepath = os.path.join(datapath, self.filename)
        
        if not os.path.exists(self.filepath):
            ftp_filepath = 'isd-lite/' + str(self.date.year) + '/' + self.filename
            self._download(ftp_filepath, self.filepath)

    def reload(self):
        """
        Reload the station. Current station is removed and new nearest station is searched.
        Used when current station has no useable data.
        """
        # Drop current station from isd_history
        index = self.isd_history.loc[self.isd_history['USAF'] == self.USAF].index.item()
        self.isd_history = self.isd_history.drop([index])
        # Find new next station and download weather data
        self._find(self.date, self.lat_query, self.lon_query)
        self._download_weatherdata()

def temperature(input_datetime: datetime, lat: float, lon: float):
    """Find temperature for datetime and location. Datetimes are rounded to nearest full hour."""

    # Round to the next full hour, because database has data for full hours
    input_datetime = hour_rounder(input_datetime)

    date = input_datetime.date()
    station = Station(date, lat, lon)

    # Sometimes the station has no data for the datetime, thus the loop
    retry = True
    while retry:
        col_names = ['Year', 'Month', 'Day', 'Hour', 'T']

        df = pd.read_csv(station.filepath, compression='gzip', quotechar='"', delim_whitespace=True, usecols=[0,1,2,3,4], names=col_names)

        df["Date"] = df["Year"].astype(str) + '-' + df["Month"].astype(str) + '-' + df["Day"].astype(str) + ' ' + df["Hour"].astype(str)  + ':00:00'

        del df['Year']
        del df['Month'] 
        del df['Day'] 
        del df['Hour']

        df.Date=pd.to_datetime(df.Date)

        df = df[df.Date.between(input_datetime, input_datetime)]

        # If the dataframe is empty, station has no data for datetime and is removed from isd_history
        if df.empty:
            # Remove the current station from possible stations and search again
            station.reload()
            retry = True
        else:
            temperature = df['T'].values[0] / 10  
            retry = False

    return temperature

def temperature_range(start: datetime, end: datetime, lat: float, lon: float):
    """Find temperature for a time range at stationary location"""

    station = Station(start, lat, lon)
    col_names = ['Year', 'Month', 'Day', 'Hour', 'T']

    df = pd.read_csv(station.filepath, compression='gzip', quotechar='"', delim_whitespace=True, usecols=[0,1,2,3,4], names=col_names)

    df["Date"] = df["Year"].astype(str) + '-' + df["Month"].astype(str) + '-' + df["Day"].astype(str) + ' ' + df["Hour"].astype(str)  + ':00:00'

    del df['Year']
    del df['Month'] 
    del df['Day'] 
    del df['Hour']

    df.Date=pd.to_datetime(df.Date)

    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

    df = df[df.Date.between(start, end)]

    df.index = range(len(df.index))

    # Apply scaling factor to temperature
    df['T'] = df['T'] / 10  

    return df

def data(start: datetime, end: datetime, lat: float ,lon: float):
    """Returns dataframe with needed data from station data."""

    station = Station(start, lat, lon)
    cols = ['Year', 'Month', 'Day', 'Hour', 'T', 'Sky_coverage']

    # Read NOAA file for the station as pandas dataframe
    df = pd.read_csv(station.filepath, compression='gzip', quotechar='"', delim_whitespace=True, usecols=[0,1,2,3,4,10], names=cols)

    df['Lat'] = lat
    df['Lon'] = lon

    # Create new column for date so date can be saved as datetime object
    df["Date"] = df["Year"].astype(str) + '-' + df["Month"].astype(str) + '-' + df["Day"].astype(str) + ' ' + df["Hour"].astype(str)  + ':00:00'
    del df['Year']
    del df['Month'] 
    del df['Day'] 
    del df['Hour']
    df.Date=pd.to_datetime(df.Date)

    # Rearrange columns so date and coordinates are first
    cols = ['Date', 'Lat', 'Lon', 'T', 'Sky_coverage']
    df = df[cols]

    # Select rows between dates
    df = df[df.Date.between(start, end)]
    # Reindex 
    df.index = range(len(df.index))
    # Apply scaling factor to temperature
    df['T'] = df['T'] / 10 

    return df

def hour_rounder(t):
    """ Rounds to nearest hour by adding a timedelta hour if minute >= 30 """
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +timedelta(hours=t.minute//30))

