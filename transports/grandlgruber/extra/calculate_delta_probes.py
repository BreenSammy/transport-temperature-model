import os

import pandas as pd

transportdirectory, _ = os.path.split(
    os.path.dirname(os.path.abspath(__file__))
    )
print(transportdirectory)
path = os.path.join(
    transportdirectory,
    'postProcessing',
    'probes',
    'battery10_0.csv'
)

probedata = pd.read_csv(path, comment = '#')
timeseries = probedata['time']
print(timeseries)
probedata = probedata.drop(['time'], axis = 1)

max_temperature = probedata.max(axis=1)
min_temperature = probedata.min(axis=1)

delta_T = max_temperature - min_temperature
delta_T = delta_T.to_frame().join(timeseries)
delta_T.columns =['delta_T', 'time']
delta_T = delta_T[['time', 'delta_T']] 
print(delta_T['delta_T'].mean())
delta_T.to_csv('battery10_0_deltaT.csv', encoding='utf-8', index=False)
print(delta_T)
