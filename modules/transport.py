import copy
from datetime import date, datetime 

import numpy as np
import pandas as pd

import weather.weather as weather
from route.route import Route

class Transport:
    def __init__(self, start, end, filename, stops = None):
        self.route = Route(start, end, filename, stops = stops)
        self.start = start
        self.end = end
        self.temperature = self.get_temperature()
        self.dataframe = self.get_dataframe()
        

    def get_temperature(self):
        length = len(self.route.dataframe.index)
        temperature = np.zeros([length, 1])
        lat = self.route.dataframe[['Lat']].values
        lon = self.route.dataframe[['Lon']].values
        for i in range(length):
            current_datetime = self.route.dataframe['Date'].values[i]
            current_datetime = pd.Timestamp(current_datetime)
            current_datetime = current_datetime.to_pydatetime()
            temperature[i] = weather.temperature(current_datetime, lat[i][0], lon[i][0])
        return temperature

    def get_dataframe(self):
        dataframe = copy.deepcopy(self.route.dataframe)
        dataframe['T'] = self.temperature
        return dataframe

    def to_csv(self, filename):
        self.dataframe.to_csv(filename, encoding='utf-8', index=False)    


       

lat = [51.38503, 50.407]
lon = [12.18273, 11.77477]
stop_start = [datetime(2019, 3, 2, 7, 15), datetime(2019, 3, 2, 9, 35)]
stop_end = [datetime(2019, 3, 2, 8, 15), datetime(2019, 3, 2, 10, 45)]

d = {'Start': stop_start, 'End': stop_end, 'Lat': lat, 'Lon': lon}

stops = pd.DataFrame(data = d)

print(stops)



start = datetime(2019, 3, 2, 5, 23)
end = datetime(2019, 3, 2, 14, 30)

Transport_berlin_garching = Transport(start, end, 'Berlin-Garching.csv', stops = stops)

print(Transport_berlin_garching.dataframe)

Transport_berlin_garching.to_csv('B-G.csv')




