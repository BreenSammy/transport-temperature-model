import copy
from datetime import date, datetime 
import json
from json import JSONEncoder
import os

import numpy as np
import pandas as pd

import modules.weather.weather as weather
from .route.route import Route

class Transport:
    def __init__(self, start, end, cargo, route_filename, stops = None):
        self.route = Route(start, end, route_filename, stops = stops)
        self.start = start
        self.end = end
        self.cargo = cargo
        self.temperature = self.get_temperature()
        self.weatherdata = self.get_weatherdata()
        
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

    def get_weatherdata(self):
        dataframe = copy.deepcopy(self.route.dataframe)
        dataframe['T'] = self.temperature
        return dataframe

    def save_weatherdata(self, filename):
        """Saves transport dataframe as .csv file"""
        self.weatherdata.to_csv(filename, encoding='utf-8', index=False)
    
    def to_json(self, filename):
        """Saves transport object data as json file"""
        with open(filename, 'w') as outfile:
            json.dump(self, outfile, cls = TransportEncoder, indent = 4,)
    
    def save(self,name):
        """Save transport as json and weatherdata as csv"""
        folderpath = os.path.join('transports', name)
        jsonpath = os.path.join(folderpath, name + '.json')
        weatherdatapath = os.path.join(folderpath, name +'_weatherdata.csv')
        
        if not os.path.exists(folderpath):
            os.makedirs(folderpath)

        self.to_json(jsonpath)
        self.save_weatherdata(weatherdatapath)

class TransportEncoder(JSONEncoder):
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"
    def default(self, transport):

        if isinstance(transport, Transport):
            # Encode dataframe stops to json conform dict
            stops = transport.route.stops.to_dict("index")
            for index, info in stops.items():
                stops[index]["Start"] = stops[index]["Start"].strftime("%s %s" % (
                        self.DATE_FORMAT, self.TIME_FORMAT
                    ))
                stops[index]["End"] = stops[index]["End"].strftime("%s %s" % (
                        self.DATE_FORMAT, self.TIME_FORMAT
                    ))
            
            return {
                "Start": transport.start.strftime("%s %s" % (
                    self.DATE_FORMAT, self.TIME_FORMAT
                )),
                "End": transport.end.strftime("%s %s" % (
                    self.DATE_FORMAT, self.TIME_FORMAT
                )),
                "Route": {
                    "Filename": transport.route.filename,
                    "Stops":  stops
                },
                "Cargo": [item.to_dict() for item in transport.cargo]           
            }


