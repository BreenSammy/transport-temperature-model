import glob
import os

import sys
sys.path.append("../..")
import modules.transport as transport

import numpy as np
import pandas as pd


schenker_transports = glob.glob('schenker_*')
print(schenker_transports)
distance_list = []

for path in schenker_transports:
    path = os.path.join(path, 'weatherdata.csv')
    # schenker_transport =transport.from_json(os.path.join(path, 'transport.json')) 
    df = pd.read_csv(path)
    distance_list.append(df['distance'])
    # schenker_transport.get_weatherdata()
    # schenker_transport.save()

distances = pd.concat(distance_list)
print(distances.mean())