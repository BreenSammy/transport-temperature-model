import calendar
import copy
from datetime import date, datetime, timedelta 
import ftplib
import os
import time
import warnings

from bs4 import BeautifulSoup
import geopy.distance
import netCDF4 as nc
import numpy as np
import pandas as pd 
import requests
from scipy import spatial

WEATHERDATAPATH = os.path.abspath('weatherdata')

if not os.path.exists(WEATHERDATAPATH):
            os.makedirs(WEATHERDATAPATH)

#NOAA database saves temperature readings with scaling factor
T_SCALINGFACTOR = 0.1

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
        
        isd_history = os.path.abspath('weatherdata/isd-history.csv')
        isd_inventory = os.path.abspath('weatherdata/isd-inventory.csv')

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
        """Conncect to NOAA server with ftp connection. Retry to establish connection if it fails."""
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
        """Finds nearest station by lat and lon that has data for specified date"""
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

    def _download_weatherdata(self):
        """Downloads weather data for the station"""

        self.filename = self.USAF + '-' + self.WBAN + '-' + str(self.date.year) + '.gz'
        self.filepath = os.path.join(WEATHERDATAPATH, self.filename)
        
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

        if not os.path.exists(targetpath):
            print('Downloading file from: \n' + fileurl)
            r = requests.get(fileurl, allow_redirects=True)
            with open(targetpath, 'wb') as outfile:
                outfile.write(r.content)
            print('Download finished')

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

    sst, distance = OISST.sea_surface_temperature(lat, lon)

    coordinates_onsea = onsea(lat, lon)

    if not use_ICOADS and coordinates_onsea:
        temperature = sst
    elif use_ICOADS and coordinates_onsea:
        ICOADS = ICOADSFile(input_datetime)
        temperature, distance = ICOADS.temperature(input_datetime, lat, lon) 
    else:
        temperature, distance = _get_temperature_at_station(input_datetime, lat, lon)

    if distance > 100:
        warnings.warn('{0}: distance to {1}, {2} is {3} km.'.format(input_datetime, lat, lon, distance))

    return temperature

def temperature_range(datetimes, lat, lon):

    if isinstance(datetimes, list):
        station = Station(datetimes[0], lat, lon)
        datetimes = [hour_rounder(entry) for entry in datetimes]
    else:
        station = Station(datetimes, lat, lon)
        datetimes = hour_rounder(datetimes)

    # Sometimes the station has no data for the datetime, thus the loop
    retry = True
    while retry:
        col_names = ['Year', 'Month', 'Day', 'Hour', 'T']

        df = pd.read_csv(
            station.filepath, parse_dates={'Date': ['Year', 'Month', 'Day', 'Hour']}, 
            compression='gzip', quotechar='"', delim_whitespace=True, usecols=[0,1,2,3,4], names=col_names
            )

        df = df[df.Date.between(datetimes[0], datetimes[-1])]

        # If the dataframe is empty, station has no data for datetime and is removed from isd_history
        if df.empty:
            # Remove the current station from possible stations and search again
            station.reload()
            retry = True
        else:
            # Pick temperature for ever datetime in datetimes
            df = df.set_index('Date')
            df = df.loc[datetimes, :]
            temperature = df['T'].values * T_SCALINGFACTOR
            retry = False

    distance = station.distance

    if distance > 100:
        warnings.warn('{0}: distance to {1}, {2} is {3} km.'.format(datetimes[0], lat, lon, distance))

    return temperature, distance

def waypoints_temperature(datetimes, lat, lon):
    """ Get temperature for all waypoints
    """
    length = lat.size
    temperatures = np.zeros(length)

    OISST = OISSTFile(datetimes[0])

    sst, _ =  OISST.sea_surface_temperature(lat[0], lon[0])

    day = datetimes[0].day

    for i in range(length):
        # Read new OISST file if day switches
        if day != datetimes[i].day:
            day = datetimes[i].day
            OISST = OISSTFile(datetimes[i])

        sst, _ =  OISST.sea_surface_temperature(lat[i], lon[i])
        # If sst is number, location is on sea
        if isinstance(sst, np.float32):
            temperatures[i] = sst
        # Else on land
        else:
            temperature_at_station, distance = _get_temperature_at_station(datetimes[i], lat[i], lon[i])
            # If distance to weatherstation is to big, use last temperature
            if distance > 300:
                warnings.warn('{0}: distance to {1}, {2} is {3} km. \n Using last temperature'.format(datetimes[i], lat[i], lon[i], distance))
                temperatures[i] = temperatures[i-1]
            else:
                temperatures[i] = temperature_at_station

    return np.around(temperatures, 2)

def _get_temperature_at_station(input_datetime, lat, lon):
    # Round to the next full hour, because database has data for full hours
    input_datetime = hour_rounder(input_datetime)

    date = input_datetime.date()
    station = Station(date, lat, lon)

    # Sometimes the station has no data for the datetime, thus the loop
    retry = True
    while retry:
        col_names = ['Year', 'Month', 'Day', 'Hour', 'T']

        df = pd.read_csv(
            station.filepath, parse_dates={'Date': ['Year', 'Month', 'Day', 'Hour']}, 
            compression='gzip', quotechar='"', delim_whitespace=True, usecols=[0,1,2,3,4], names=col_names
            )

        df = df[df.Date.between(input_datetime, input_datetime)]

        # If the dataframe is empty, station has no data for datetime and is removed from isd_history
        if df.empty:
            # Remove the current station from possible stations and search again
            station.reload()
            retry = True
        else:
            temperature = df['T'].values[0] * T_SCALINGFACTOR  
            retry = False

    distance = station.distance

    return temperature, distance

def hour_rounder(t):
    """ Rounds to nearest hour by adding a timedelta hour if minute >= 30 """
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +timedelta(hours=t.minute//30))

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
