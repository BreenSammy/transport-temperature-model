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

routepaths =  glob.glob('routes' + '/*.*')
df_list = []
for path in routepaths:
    df_list.append(pd.read_csv(path, parse_dates = ['Date']))
    
fig=plt.figure()
ax=fig.add_axes([0,0,1,1])

ax.set_axis_off()
fig.add_axes(ax)

m = Basemap(projection='merc',llcrnrlat=-62,urcrnrlat=77,llcrnrlon=-180,urcrnrlon=180,resolution='l')

m.drawcoastlines(linewidth=0.5)
m.drawcountries()
m.fillcontinents(color=TUMGray3, zorder=0, alpha = 0.5)

n = 0
for df in df_list:
    lons = df['Longitude'].values
    lats = df['Latitude'].values
    split_indices = []
    for i in range(len(lons) - 1):
        if check_crossover(lons[i], lons[i+1]):
            split_indices.append(i+1)
    
    lons = np.split(lons, split_indices)

    lats = np.split(lats, split_indices)
    for i in range(len(lons)):
        x, y = m(lons[i], lats[i])
        m.plot(x, y, marker=None, color=TUMBlue)

    add_seconds(df)
    df.to_csv(routepaths[n], encoding='utf-8', index=False)
    n += 1

plotpath = os.path.join('scatter' + '.pdf')
# fig.set_size_inches(4.77, 3.5)
plt.savefig(plotpath, dpi = 500, bbox_inches='tight')

