import os
import ftplib
from datetime import date 
import time
import copy

import numpy as np
import pandas as pd 
from scipy import spatial

class Weather:
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
                    self.download('isd-invenotry.csv', isd_invenotry) 

                self.isd_history = pd.read_csv(isd_history)
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

        # remove all stations which have no records at the desired date
        date = int(date.strftime('%Y%m%d'))
        possible_stations = copy.deepcopy(self.isd_history)
        possible_stations = possible_stations[possible_stations.BEGIN < date]
        possible_stations = possible_stations[possible_stations.END > date]


        coordinates = possible_stations[['LAT', 'LON']].values

        tree = spatial.KDTree(coordinates)
        result = tree.query([(lat,lon)])[1][0]

        possible_stations = possible_stations[possible_stations.LAT == coordinates[result][0]]
        station = possible_stations[possible_stations.LON == coordinates[result][1]]

        return station

    def download_weather_data(self, date, lat, lon):

        data_path = os.path.abspath('data')

        if not os.path.exists(data_path):
            os.makedirs(data_path)
        
        self.ftp.cwd('isd-lite/' + str(date.year))
        
        station = self.find_station(date, lat, lon)
        file_name = station['USAF'].values[0] + '-' + str(station['WBAN'].values[0]) + '-' + str(date.year) + '.gz'

        self.download(file_name, os.path.join(data_path, file_name))


date = date(2018, 3, 2)    

weather = Weather()

weather.download_weather_data(date, 44, 12)