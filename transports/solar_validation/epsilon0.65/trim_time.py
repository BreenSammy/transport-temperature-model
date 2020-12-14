import os

import pandas as pd


probepath = os.path.join(os.path.abspath('postProcessing'), 'probes', 'airInside.csv')
probes = pd.read_csv(probepath, comment = '#')

probes['time'] = probes['time'] - probes.iloc[1]['time']
probes = probes.drop(probes.index[0])

probes.to_csv('probes.csv', encoding='utf-8', index=False)

weatherdata = pd.read_csv('weatherdata.csv', parse_dates=['Date'], header = 0)

weatherdata = weatherdata.drop(weatherdata.index[0])
# print(weatherdata['Date'])
weatherdata['time'] = weatherdata['Date'] - weatherdata.iloc[0]['Date']
weatherdata['time'] = weatherdata['time'].apply(lambda timedelta: timedelta.total_seconds())

weatherdata.to_csv('weatherdata_with_time.csv', encoding='utf-8', index=False)