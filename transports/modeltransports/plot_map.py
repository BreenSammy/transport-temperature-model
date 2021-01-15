from datetime import date, timedelta
import glob
import os


import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
import pandas as pd

from matplotlib import rc

matplotlib.use('Agg')

matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'sans-serif',
    'text.usetex': True,
    'font.sans-serif': 'Arial',
    'mathtext.fontset' : 'cm'
})

def add_seconds(dataframe):
    """Add a column with total passed seconds to dataframe with ['Date'] column"""
    start = dataframe['Date'].iloc[0]
    length = len(dataframe.index)
    seconds = np.zeros(length)

    for i in range(length):
        passed_timedelta = dataframe['Date'].iloc[i] - start
        seconds[i] = passed_timedelta.total_seconds()

    dataframe.insert(1, 'seconds', seconds, True) 

def check_crossover(longitude_start, longitude_end):
    """Check if -180 to +180 crossover appears between two coordinates"""
    if np.sign(longitude_start) == np.sign(longitude_end):
        return False
    elif (abs(longitude_start) + abs(longitude_end)) > 180:
        return True

TUMBlue = '#0065BD'
TUMBlue1 = '#003359'
TUMBlue2 = '#005293'
TUMOrange = '#E37222'
TUMGreen = '#A2AD00'
TUMGray2 = '#7F7F7F'
TUMGray3 = '#CCCCCC'

routeone =  glob.glob('one' + '/*' +  '/weatherdata.csv')
routetwo =  glob.glob('two' + '/*' +  '/route.csv')

df_list_one = []
for path in routeone:
    df_list_one.append(pd.read_csv(path, parse_dates = ['Date']))
df_list_two = []
for path in routetwo:
    df_list_two.append(pd.read_csv(path, names = ['Lon', 'Lat']))
    
fig=plt.figure()
ax=fig.add_axes([0,0,1,1])

ax.set_axis_off()
fig.add_axes(ax)

# m = Basemap(projection='merc',llcrnrlat=-62,urcrnrlat=77,llcrnrlon=-180,urcrnrlon=180,resolution='l')
m = Basemap(projection='merc',llcrnrlat=-30,urcrnrlat=65,llcrnrlon=-120,urcrnrlon=155,resolution='l')

m.drawcoastlines(linewidth=0.5)
m.drawcountries()
m.fillcontinents(color=TUMGray3, zorder=0, alpha = 0.5)
colors = [TUMGreen, TUMBlue, TUMOrange]

stops = [
    [34.553799,113.84600],
    [48.644560,12.482933],
    [51.402545,12.453207],
    [40.546397,-74.49199]
]

text_shift = [
    [300000,300000],
    [300000,-600000],
    [300000,300000],
    [-3300000,300000]
]

text = [
    'Zellproduktion',
    'Systemproduktion',
    'Fahrzeugproduktion',
    'Auslieferung'
]
n = 0
for df in df_list_one:
    lons = df['Lon'].values
    lats = df['Lat'].values
    # lon_min, lat_min = m(lons[0], lats[0])
    # lon_max, lat_max = m(lons[-1], lats[-1])
    # print(lon_min)
    # m.scatter(lon_min, lat_min, s = 5, marker = "o", color='r', zorder=5)
    # m.scatter(lon_max, lat_max, s = 5, marker = "o", color='r', zorder=5)
    # plt.text(lon_min + 300000, lat_min + 300000, 'text',fontsize=7,fontweight='bold',
    #            color='k', 
    #            bbox=dict(facecolor='w', edgecolor='black', boxstyle='round'))
    # plt.text(lon_max + 300000, lat_max + 300000, 'text',fontsize=7,fontweight='bold',
    #            color='k', 
    #            bbox=dict(facecolor='w', edgecolor='black', boxstyle='round'))
    split_indices = []
    for i in range(len(lons) - 1):
        if check_crossover(lons[i], lons[i+1]):
            split_indices.append(i+1)
    
    lons = np.split(lons, split_indices)

    lats = np.split(lats, split_indices)
    for i in range(len(lons)):
        x, y = m(lons[i], lats[i])
        m.plot(x, y, '--', marker=None, color=colors[n])

    n += 1

for n in range(4):
    stop_lon, stop_lat = m(stops[n][1], stops[n][0])
    m.scatter(stop_lon, stop_lat, s = 5, marker = "o", color='r', zorder=5)
    plt.text(
        stop_lon + text_shift[n][0], stop_lat + text_shift[n][1], text[n],fontsize=7,fontweight='bold',
        color='k', 
        bbox=dict(facecolor='w', edgecolor='black', boxstyle='round')
        )

plotpath = os.path.join('route_1' + '.pdf')
fig.set_figheight(2.3622)
plt.savefig(plotpath, dpi = 500, bbox_inches='tight')
plt.clf()

fig=plt.figure()
ax=fig.add_axes([0,0,1,1])

ax.set_axis_off()
fig.add_axes(ax)

m = Basemap(projection='merc',llcrnrlat=45,urcrnrlat=58,llcrnrlon=-3,urcrnrlon=28,resolution='i')
# m = Basemap(projection='merc',llcrnrlat=45,urcrnrlat=60,llcrnrlon=2.5,urcrnrlon=22.5,resolution='i')

m.drawcoastlines(linewidth=0.5)
m.drawcountries()
m.fillcontinents(color=TUMGray3, zorder=0, alpha = 0.5)
colors = [TUMGreen, TUMBlue, TUMOrange]

n = 0
for df in df_list_two:
    lons = df['Lon'].values
    lats = df['Lat'].values
    lon_min, lat_min = m(lons[0], lats[0])
    lon_max, lat_max = m(lons[-1], lats[-1])
    split_indices = []
    for i in range(len(lons) - 1):
        if check_crossover(lons[i], lons[i+1]):
            split_indices.append(i+1)
    
    lons = np.split(lons, split_indices)

    lats = np.split(lats, split_indices)
    for i in range(len(lons)):
        x, y = m(lons[i], lats[i])
        m.plot(x, y, '--', marker=None, color=colors[n])

    n += 1

stops = [
    [51.017254, 16.888169],
    [52.306776, 10.515355],
    [50.784447, 12.492292],
    [48.265588, 11.671388]
]

text_shift = [
    [80000,80000],
    [80000,80000],
    [80000,-125000],
    [80000,-125000]
]

for n in range(4):
    stop_lon, stop_lat = m(stops[n][1], stops[n][0])
    m.scatter(stop_lon, stop_lat, s = 5, marker = "o", color='r', zorder=5)
    plt.text(
        stop_lon + text_shift[n][0], stop_lat + text_shift[n][1], text[n],fontsize=7,fontweight='bold',
        color='k', 
        bbox=dict(facecolor='w', edgecolor='black', boxstyle='round')
        )

plotpath = os.path.join('route_2' + '.pdf')
fig.set_figheight(2.3622)
plt.savefig(plotpath, dpi = 500, bbox_inches='tight')