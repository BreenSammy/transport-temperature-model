# Creates weatherdata file for Leinberger simulation from ambient.csv file. Execute before ttm.

from datetime import date, timedelta, datetime
import os

import numpy as np
import pandas as pd

lat = 45.3271037
lon = -122.7640678

ambient = pd.read_csv('ambient.csv')
ambient['time'] = np.floor(ambient['time']) - np.floor(ambient.iloc[0]['time'])

startdatetime = datetime(year = 2005, month= 9, day = 26, hour = 23, minute = 48)
lons = np.zeros(len(ambient['time'].values))
lats = np.zeros(len(ambient['time'].values))
lons[:] = lon
lats[:] = lat

weatherdata = pd.DataFrame()
weatherdata['Date'] = [startdatetime + timedelta(seconds = item) for item in ambient['time'].values]
weatherdata['Lat'] = lats
weatherdata['Lon'] = lons
weatherdata['T'] = ambient.iloc[:,1]

print(weatherdata.iloc[-1]['Date'] - weatherdata.iloc[0]['Date'])

prerun = pd.DataFrame(data = {
    'Date': datetime(year = 2005, month= 9, day = 26, hour = 19, minute = 48),
    'Lat': lat,
    'Lon': lon,
    'T': 24.66469812246901
    },
    index=[0],
    )

weatherdata = pd.concat([prerun, weatherdata])
print(weatherdata)

weatherdata.to_csv('weatherdata.csv', encoding='utf-8', index=False)
