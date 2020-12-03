import calendar
import copy
from datetime import date, datetime, timedelta 
import ftplib
import os
import shutil
import time
import warnings

from bs4 import BeautifulSoup
import geopy.distance
import netCDF4 as nc
import numpy as np
import pandas as pd 
import requests
from scipy import spatial

WEATHERDATAPATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'weatherdata'
    )

if not os.path.exists(WEATHERDATAPATH):
            os.makedirs(WEATHERDATAPATH)

#NOAA database saves temperature readings with scaling factor
T_SCALINGFACTOR = 0.1

def hour_rounder(t):
    """ Rounds to nearest hour by adding a timedelta hour if minute >= 30 """
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +timedelta(hours=t.minute//30))

class ISD:
    """Downloads weatherdata from ISD Lite database"""
    URL = 'https://www.ncei.noaa.gov/pub/data/noaa/isd-lite/'
    ISD_HISTORY_URL = 'https://www.ncei.noaa.gov/pub/data/noaa/isd-history.csv'
    ISD_INVENTORY_URL = 'https://www.ncei.noaa.gov/pub/data/noaa/isd-inventory.csv'
    def __init__(self):
        filedirectory = os.path.dirname(os.path.abspath(__file__))
        isd_history_path = os.path.join(filedirectory, 'isd-history.csv')
        isd_inventory_path = os.path.join(filedirectory, 'isd-inventory.csv')

        # Download isd history and inventory for station finding
        if not os.path.exists(isd_history_path) or (time.time() - os.path.getmtime(isd_history_path)) > 2592000:  
            self._download(self.ISD_HISTORY_URL, isd_history_path) 
        if not os.path.exists(isd_inventory_path) or (time.time() - os.path.getmtime(isd_inventory_path)) > 2592000:
            self._download(self.ISD_INVENTORY_URL, isd_inventory_path) 

        self.isd_history = pd.read_csv(isd_history_path, dtype={'USAF': str, 'WBAN': str})
        self.isd_inventory = pd.read_csv(isd_inventory_path, dtype={'USAF': str, 'WBAN': str})
        # Remove stations that do not have a location
        self.isd_history = self.isd_history[self.isd_history.LAT.notnull()]
        self.reset_possible_stations()

    def reset_possible_stations(self):
        """Possibile stations are used for finding closest station with weatherdata"""
        self.possible_stations = copy.deepcopy(self.isd_history)

    def _download(self, fileurl: str, targetpath: str):
        if not os.path.exists(targetpath):
            print('Downloading file from: \n' + fileurl)
            r = requests.get(fileurl, allow_redirects=True)
            with open(targetpath, 'wb') as outfile:
                outfile.write(r.content)
            print('Download finished')

    def find_station(self, input_date, lat: float, lon: float):
        """Finds nearest station by lat and lon that has data for specified date"""
        # Remove all stations which have no records at the desired date
        date_int = int(input_date.strftime('%Y%m%d'))
        self.possible_stations = self.possible_stations[self.possible_stations.BEGIN < date_int]
        self.possible_stations = self.possible_stations[self.possible_stations.END > date_int]

        if self.possible_stations.empty:
            raise ValueError('No station available for query datetime')

        while True:
            coordinates = self.possible_stations[['LAT', 'LON']].values

            # Search for closest station
            tree = spatial.cKDTree(coordinates)
            index_next_station = tree.query([(lat,lon)])[1][0]

            # Get dataframe entry of closest station
            station = self.possible_stations[
                (self.possible_stations.LAT == coordinates[index_next_station][0]) & 
                (self.possible_stations.LON == coordinates[index_next_station][1])
                ]

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
            if not inventory.empty:
                if inventory[month].values[0]/days_in_month >= 24:
                    break
                
            # Remove the current station from possible stations and search again
            index = self.possible_stations.loc[
                (self.possible_stations['USAF'] == station['USAF'].values[0]) & 
                (self.possible_stations['WBAN'] == station['WBAN'].values[0])
                ].index.item()

            self.possible_stations = self.possible_stations.drop([index])

        return station

    def temperature(self, input_date, lat: float, lon: float, output_station = False, ftp = False):
        # Round to the next full hour, because database has data for full hours
        input_date = hour_rounder(input_date)
        # Sometimes the station has no data for the datetime, thus the loop
        retry = True
        while retry:
            station = self.find_station(input_date, lat, lon)
            # Calculate distance from query location to the station
            coords_station = np.array([station['LAT'].iloc[0], station['LON'].iloc[0]])
            coords_query = np.array([lat, lon])
            distance = geopy.distance.distance(coords_station, coords_query).km

            if distance > 300:            
                print(
                    '{0}: Distance from {1}, {2} to closest weatherstation is {3} km. No data at query location available'.format(
                        input_date, round(lat, 3), round(lon, 3), round(distance, 2))
                        )
                temperature = float('nan')
                self.possible_stations = self.possible_stations.drop([station.index[0]])
                break
            
            col_names = ['Year', 'Month', 'Day', 'Hour', 'T']
            filename = '{0}-{1}-{2}.gz'.format(station['USAF'].iloc[0], station['WBAN'].iloc[0], input_date.year)

            # Download files with ftp connection
            if ftp:
                filepath = self._download_weatherdata_ftp(filename, input_date.year)
            # Else use https url
            else:
                # e.g .../2019/010020-99999-2019.gz
                filepath = self.URL + str(input_date.year) + '/' + filename

            df = pd.read_csv(
                    filepath, parse_dates={'Date': ['Year', 'Month', 'Day', 'Hour']}, 
                    compression='gzip', quotechar='"', delim_whitespace=True, usecols=[0,1,2,3,4], names=col_names
                    )

            df = df[df.Date.between(input_date, input_date)]

            # If the dataframe is empty or temperature value is faulty, station has no data for datetime and is removed from isd_history
            if df.empty or (df['T'].values[0] == -9999):
                self.possible_stations = self.possible_stations.drop([station.index[0]])
                retry = True
            else:
                temperature = df['T'].values[0] * T_SCALINGFACTOR  
                retry = False

        self.reset_possible_stations()

        if output_station:
            return temperature, station
        else:
            return temperature

    def _connect_ftp(self):
        """Conncect to NOAA server with ftp connection. Retry to establish connection if it fails."""
        retry = True
        while (retry):
            try:
                ftp = ftplib.FTP('ftp.ncei.noaa.gov')
                ftp.login()
                ftp.cwd('pub/data/noaa')
                retry = False

            except EOFError as e:
                print(e)
                print("Connection to NOAA server failed. Retrying to connect.")
                retry = True

            except OSError as e:
                print(e)
                print("Connection to NOAA server failed. Retrying to connect.")
                retry = True

        return ftp

    def _download_ftp(self, source_file: str, target_file: str):
        """Downlaod a file from the ftp server and save it in the target file"""
        try:
            ftp = self._connect_ftp()
            with open(target_file, 'wb+') as fh:
                ftp.retrbinary('RETR ' + source_file, fh.write)

        except ftplib.all_errors as e:
            print('FTP error:', e) 

            if os.path.isfile(target_file):
                os.remove(target_file)

    def _download_weatherdata_ftp(self, filename, year):
        """Downloads weather data for the station"""

        filepath = os.path.join(WEATHERDATAPATH, filename)
        
        if not os.path.exists(filepath):
            ftp_filepath = 'isd-lite/' + str(year) + '/' + filename
            self._download_ftp(ftp_filepath, filepath)

        return filepath

class NOAAFile(object):
    """Base class for access to NOAA server"""
    def __init__(self, input_date):   
        self.date = input_date

    def _find_file(self, url, datestring, extension):
        """Find url for data file for input_date"""

        page = requests.get(url).text
        soup = BeautifulSoup(page, 'html.parser')
        available_files = [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(extension)]

        return next((s for s in available_files if datestring in s), None) 

    def _download(self, fileurl: str, targetpath: str):
            r = requests.get(fileurl, allow_redirects=True)
            with open(targetpath, 'wb') as outfile:
                outfile.write(r.content)

class ICOADSFile(NOAAFile):
    """
    Class to handle files from NOAA International Comprehensive Ocean-Atmosphere Data Set.
    See also: https://icoads.noaa.gov/index.shtml
    """
    def __init__(self, input_date, download = True):

        super(ICOADSFile, self).__init__(input_date)
        url = 'https://www.ncei.noaa.gov/data/international-comprehensive-ocean-atmosphere/v3/archive/enhanced-trim/'
        datestring = 'd' + input_date.strftime('%Y%m')
        fileurl = self._find_file(url, datestring, 'gz')
        filename = 'ICOADS_' + self.date.strftime('%Y%m') + '.dat.gz'
        targetpath = os.path.join(WEATHERDATAPATH, filename)

        if download:
            self._download(fileurl, targetpath)
            readfile = targetpath
        else: 
            readfile = fileurl

        self.dataframe = self._read(readfile)

    def _read(self, ICOADSfile):

        # character lengths of columns and scaling factors for values, see IMMA_format.pdf in doc
        COL_LENGTHS = {
            'YR': range(0, 4), 'MO': range(4, 6), 'DY': range(6, 8), 'HR': range(8, 12),
            'Lat': range(12,17), 'Lon': range(17, 23), 'T': range(69, 73)
            }
        
        SCALINGFACTORS = {
            'T': T_SCALINGFACTOR,
            'Lat': 0.01,
            'Lon': 0.01,
            'HR': 36 # 0.01* 3600 to transform into seconds
        }

        dateparse = lambda x: datetime.strptime(x, '%Y %m %d')

        df = pd.read_fwf(
            ICOADSfile, parse_dates={'date': ['YR', 'MO', 'DY']}, date_parser=dateparse,
            colspecs=[(min(x), max(x)+1) for x in COL_LENGTHS.values()],
            header=None, names=COL_LENGTHS.keys()
            )

        # drop all readings without temperature readings
        df = df[df['T'].notna()]

        for key in SCALINGFACTORS:
            df[key] = df[key] * SCALINGFACTORS[key]

        # add time to date
        df['HR'] = pd.to_timedelta(df['HR'], 's')  
        df['date'] = df['date'] + df['HR']
        df = df.drop(columns = ['HR'])

        return df

    def temperature(self, input_datetime, lat, lon):

            # df = copy.deepcopy(self.dataframe)
            df = self.dataframe

            df = df[df.date.between(
                input_datetime - timedelta(hours = 3),
                input_datetime + timedelta(hours = 3)
                )]

            coordinates = df[['Lat', 'Lon']].values

            # Search for closest reading
            tree = spatial.KDTree(coordinates)
            index = tree.query([(lat,lon)])[1][0]

            distance = geopy.distance.distance([lat, lon], coordinates[index]).km
 
            return df.iloc[index]['T'], distance

class OISSTFile(NOAAFile):
    """
    Class to handle files from NOAA sea surface temperature optimum interpolation database. 
    Daily files in netCDF format are availabe.
    
    See also:
    https://www.ncdc.noaa.gov/oisst
    https://towardsdatascience.com/read-netcdf-data-with-python-901f7ff61648
    https://iescoders.com/reading-netcdf4-data-in-python/
    """
    def __init__(self, input_date):
        super(OISSTFile, self).__init__(input_date)
         
        url = 'https://www.ncei.noaa.gov/data/sea-surface-temperature-optimum-interpolation/v2.1/access/avhrr/{}'

        folderstring = input_date.strftime('%Y%m')
        datestring = input_date.strftime('%Y%m%d')

        fileurl = self._find_file(url.format(folderstring), datestring, 'nc')
        filename = os.path.basename(fileurl)
        targetpath = os.path.join(WEATHERDATAPATH, filename)

        self._download(fileurl, targetpath)
        
        self.dataset = nc.Dataset(targetpath)

    def sea_surface_temperature(self, lat, lon):
        """
        Read sea surface temperature from netCDF file. sst is variable of dimensions time, zlev, lat and lon.
        Documentation from dataset:

        time(time)
            long_name: Center time of the day
            units: days since 1978-01-01 12:00:00
            unlimited dimensions: time
            current shape = (1,)

        zlev(zlev)
            long_name: Sea surface height
            units: meters
            positive: down
            actual_range: 0, 0

        lat(lat)
            long_name: Latitude
            units: degrees_north
            grids: Uniform grid from -89.875 to 89.875 by 0.25
            current shape = (720)

        lon(lon)
            long_name: Longitude
            units: degrees_east
            grids: Uniform grid from 0.125 to 359.875 by 0.25
            current shape = (1440)

        sst(time, zlev, lat, lon)
            long_name: Daily sea surface temperature
            units: Celsius
            current shape = (1, 1, 720, 1440)
    """
        # Transform longitude format
        lon = degrees_decimal_to_east(lon)

        # Data points lie on a grid with 0.25° spacing, therfore closest datapoint location has to be found
        GRIDSIZE = 0.25

        latdivmod = divmod(lat, GRIDSIZE)
        londivmod = divmod(lon, GRIDSIZE)

        lat_sst = latdivmod[0] * GRIDSIZE + round(latdivmod[1]) + GRIDSIZE / 2
        lon_sst = londivmod[0] * GRIDSIZE + round(londivmod[1]) + GRIDSIZE / 2

        dataset_lon = self.dataset['lon'][:]
        dataset_lat = self.dataset['lat'][:]

        index_lon = np.where(np.isclose(dataset_lon, lon_sst))[0]
        index_lat = np.where(np.isclose(dataset_lat, lat_sst))[0]

        temperature = self.dataset['sst'][0,0, index_lat, index_lon][0][0]
        distance = geopy.distance.distance([lat, lon], [lat_sst, lon_sst]).km

        return temperature, distance

def temperature(input_datetime: datetime, lat: float, lon: float, use_ICOADS = False):
    """Find temperature for datetime and location."""

    OISST = OISSTFile(input_datetime)
    sst, _ = OISST.sea_surface_temperature(lat, lon)
    coordinates_onsea = onsea(lat, lon)

    isd = ISD()

    if not use_ICOADS and coordinates_onsea:
        temperature = sst
    elif use_ICOADS and coordinates_onsea:
        ICOADS = ICOADSFile(input_datetime)
        temperature, _ = ICOADS.temperature(input_datetime, lat, lon) 
    else:
        temperature = isd.temperature(input_datetime, lat, lon)

    clear()

    return temperature

def waypoints_temperature(datetimes, lat, lon):
    """ Get temperature for a series of waypoints"""
    
    length = lat.size
    temperatures = np.empty(length)
    temperatures[:] = np.nan

    isd = ISD()
    OISST = OISSTFile(datetimes[0])
    day = datetimes[0].day

    for i in range(length):
        # Read new OISST file if day switches
        if day != datetimes[i].day:
            day = datetimes[i].day
            OISST = OISSTFile(datetimes[i])

        sst, _ =  OISST.sea_surface_temperature(lat[i], lon[i])
        isd_temperature = isd.temperature(datetimes[i], lat[i], lon[i], ftp = True)

        if not np.isnan(isd_temperature):
            temperatures[i] = isd_temperature
        elif isinstance(sst, np.float32):
            temperatures[i] = sst

        if not np.isnan(temperatures[i]):
            print(
                "Found temperature data for {0} at {1}, {2}: {3}".format(
                    datetimes[i], round(lat[i], 3), round(lon[i], 3), round(temperatures[i], 1)
                    ))
        else:
            print(
                "Did not find temperature data for {0} at {1}, {2}: {3}".format(
                    datetimes[i], round(lat[i], 3), round(lon[i], 3), round(temperatures[i], 1)
                    ))

    clear()

    return np.around(temperatures, 2)

def degrees_decimal_to_east(lon):
    """
    Transform longitude in decimal format to degrees east.
    Example:
    Longitude: 122.61458° W
    decimal format:
    -122.61458
    degrees east:
    237.38542 
    """
    if lon < 0:
        lon = 360 - abs(lon)

    return lon

def onsea(lat, lon):
    """
    Check if coordinates are on sea by reading value from OISST. 
    If no value is available that means coordinates are on land.
    Uses file from day before yesterday to definetly get file.
    """
    day_before_yesterday = date.today() - timedelta(days = 2) 
    sst, _ = OISSTFile(day_before_yesterday).sea_surface_temperature(lat, lon)

    if isinstance(sst, np.float32):
        return True
    else:
        return False

def clear():
    """Delete all downloaded weatherdata"""
    shutil.rmtree(WEATHERDATAPATH)