#!/usr/bin/env python3

import os
import json

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

matplotlib.use('Agg')

def skip_condition(index):
    if index % 20 == 1:
        return False
    return True
    
def calibration(temperature):
    return 97.6/113 * temperature + 97.6*(1 - 109/113)

filepath = os.path.abspath('response.json')
simulation_cooldown_path = os.path.join('cooldown', 'postProcessing', 'arrival', 'battery0_0.csv')
simulation_warmup_path = os.path.join('warmup', 'postProcessing', 'arrival', 'battery0_0.csv')

df_simulation_cooldown = pd.read_csv(simulation_cooldown_path)
df_simulation_warmup = pd.read_csv(simulation_warmup_path)

with open(filepath) as json_file:
    json_dict = json.load(json_file)

batterytemperature = np.array(json_dict["results"]["A"]["series"][0]["points"])
ambienttemperature = np.array(json_dict["results"]["A"]["series"][1]["points"])

start_timestamp = 1602853037000 
equilibrium_cooldown = 1603113635000
end_cooldown = 1603175487000
end_warmingup = 1603358436000

df_dict = {
    "timestamp": ambienttemperature[:,1],
    "ambient": ambienttemperature[:,0],
    "battery": batterytemperature[:,0]
}

df = pd.DataFrame(data = df_dict)
df['ambient'] = calibration(df['ambient'])
df['battery'] = calibration(df['battery'])

df_cooldown = df[df.timestamp.between(start_timestamp, equilibrium_cooldown)]
df_warmingup = df[df.timestamp.between(end_cooldown, end_warmingup)]

df_cooldown['timestamp'] = (df_cooldown['timestamp'] - start_timestamp) / 1000
df_warmingup['timestamp'] = (df_warmingup['timestamp'] - end_cooldown) / 1000

df.to_csv('temperature_full.csv', encoding='utf-8', index=False)
df_cooldown.to_csv('temperature_cooldown.csv', encoding='utf-8', index=False)
df_warmingup.to_csv('temperature_warmingup.csv', encoding='utf-8', index=False)


fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.set_ylim([-10,30])

hours = (df_cooldown['timestamp'] - df_cooldown['timestamp'].iloc[0]) / 3600000

plt.plot(hours, df_cooldown['battery'])
plt.plot(hours, df_cooldown['ambient'])
plt.plot(df_simulation_cooldown['time'] / 3600, df_simulation_cooldown['average(T)'])
plt.plot(df_simulation_cooldown['time'] / 3600, df_simulation_cooldown['max(T)'])
plt.xlabel('time in h')
plt.ylabel('temperature in °C')
plt.legend(['internal', 'ambient', 'simulation'], loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol = 3)
plt.savefig('cooldown.png', dpi = 250, bbox_inches='tight')
plt.clf()

fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.set_ylim([-10,30])

hours = (df_warmingup['timestamp'] - df_warmingup['timestamp'].iloc[0]) / 3600000

df_simulation_warmup = df_simulation_warmup.loc[df_simulation_warmup['time'] <= hours.iloc[-1]*3600 + 7200]

plt.plot(hours, df_warmingup['battery'])
plt.plot(hours, df_warmingup['ambient'])
plt.plot(df_simulation_warmup['time'] / 3600, df_simulation_warmup['min(T)'])
plt.plot(df_simulation_warmup['time'] / 3600, df_simulation_warmup['average(T)'])
plt.xlabel('time in h')
plt.ylabel('temperature in °C')
plt.legend(['internal', 'ambient', 'simulation'], loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol = 3)
plt.savefig('warmup.png', dpi = 250, bbox_inches='tight')

print(df_warmingup)
df_warmingup = pd.read_csv('temperature_warmingup.csv', names = ['time', 'ambient', 'battery'], skiprows= lambda x: skip_condition(x))
df_cooldown = pd.read_csv('temperature_cooldown.csv', names = ['time', 'ambient', 'battery'],skiprows= lambda x: skip_condition(x))
print(df_warmingup)
df_warmingup.to_csv('temperature_warmingup.csv', encoding='utf-8', index=False)
df_cooldown.to_csv('temperature_cooldown.csv', encoding='utf-8', index=False)