import copy
import glob
from math import ceil, floor
import os
import json

import altair as alt
import branca
import geopy.distance
import folium
from folium import plugins
import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tikzplotlib

matplotlib.use('Agg')

TUMBLUE = '#0065BD'
TUMWHITE = '#FFFFFF'
TUMBLACK = '#000000'
TUMBLUEDARK = '#003359'
TUMBLUELIGHT = '#64A0C8'
TUMORANGE = '#E37222'
TUMGREEN = '#A2AD00'

DOMAIN = ['ambient', 'average_air']
RANGE = [TUMBLUE, TUMORANGE]

def jet(steps = 256):
    """Get matplotlib colormap jet"""
    step = floor(256/steps)
    return [cm.jet(i) for i in range(0, 256, step)]

def create_stop_dataframe(stop_list):
    df = pd.concat(stop_list)
    # Create new stop dataframe
    stop = pd.DataFrame(
        data = {
            'start': df['Date'].iloc[0],
            'end': df['Date'].iloc[-1],
            'Lat': df['Lat'].values.mean(),
            'Lon': df['Lon'].values.mean(),
            'timestamps': 0,
            'ambient': 0,
            'average_air': 0
            },
        dtype=object, 
        index=[0]
        )
    # Add temperatures as lists
    stop.at[0, 'timestamps'] = df['Date'].values
    stop.at[0, 'ambient'] = df['ambient'].values
    stop.at[0, 'average_air'] = df['average_air'].values
    return stop

def filter_stops(waypoints):
    """Method to filter stop locations from all waypoints"""
    DISTANCETHRESHOLD = 15
    coordinates = waypoints[['Lat', 'Lon']].values
    stop_list = []
    stops = pd.DataFrame(columns=[
        'start', 'end', 'Lat', 'Lon', 'timestamps', 'ambient', 'average_air'
        ])

    for i in range(len(waypoints) - 1):
        distance = geopy.distance.distance(coordinates[i, :],coordinates[i + 1, :]).km
        if distance <= DISTANCETHRESHOLD: 
            # First point of stop needs to be added
            if stop_list == []:
                stop_list.append(waypoints.loc[i, :])
            stop_list.append(waypoints.loc[i+1, :])
            # Remove point at stop from waypoints
            waypoints = waypoints.drop([i])
        elif stop_list != []:
            # Remove last point at stop
            waypoints = waypoints.drop([i])
            df = pd.concat(stop_list)
            # Create new stop dataframe
            new_stop = create_stop_dataframe(stop_list)
            # Concat stops
            stops = pd.concat([stops, new_stop])
            stop_list = []

    if stop_list != []:
        new_stop = create_stop_dataframe(stop_list)
        # Concat stops
        stops = pd.concat([stops, new_stop])
        stop_list = []
    
    # Reindex dataframes
    waypoints.index = range(len(waypoints.index))
    stops.index = range(len(stops.index))

    return waypoints, stops

def transport(transport):

    data = copy.deepcopy(transport.weatherdata)
    data.rename(columns = {'T':'ambient'}, inplace = True) 
    if transport.type.lower() == 'car':
        temperature_air = transport.read_postprocessing('battery0_0')
    else:
        temperature_air = transport.read_postprocessing('airInside')
    # Merge weatherdata with air temperature
    temperature_air.rename(
        columns={'time':'seconds', 'average(T)': 'average_air'}, inplace=True
        )
    data = pd.merge(data, temperature_air, how='outer')
    # Interpolate missing values if something went wrong during postprocessing
    data['average_air'] = data['average_air'].interpolate()

    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    coordinates = data[['Lat', 'Lon']].values
    data = data.round({'average_air': 3})
    waypoints, stops = filter_stops(data)
    # Dataframe with coordinates of waypoints and stops for plotting of the route
    coordinates = pd.concat([
        waypoints.loc[:, ['Date', 'Lat', 'Lon']],
        stops.loc[:, ['start', 'Lat', 'Lon']].rename(columns = {
            'start': 'Date'
        })
    ])
    # Sort by date
    coordinates['Date'] = pd.to_datetime(coordinates['Date'])
    coordinates = coordinates.sort_values(by=['Date'])

    start_lat = data[['Lat']].values.mean()
    start_lon = data[['Lon']].values.mean()

    m = folium.Map(
        location=[start_lat, start_lon],
        zoom_start=4,
        tiles=None
        )

    folium.raster_layers.TileLayer('Cartodb Positron').add_to(m)
    folium.raster_layers.TileLayer('OpenStreetMap').add_to(m)
  
    fg_waypoints = folium.FeatureGroup(name='Waypoints')
    fg_stops = folium.FeatureGroup(name='Stops')
    m.add_child(fg_waypoints)
    m.add_child(fg_stops)

    index = [-15, -5, 5, 15, 25, 35, 45, 55]
    colormap = branca.colormap.LinearColormap(
        jet(steps = len(index)), 
        index=index, 
        vmin=index[0], 
        vmax=index[-1], 
        caption='Temperature inside the carrier')

    # Create marker for start of transport and create popup with graph of transport
    popup = folium.Popup()
    plot_data = data.melt(id_vars=['Date'], value_vars=['ambient', 'average_air'])
    chart = alt.Chart(plot_data).mark_line().encode(
            alt.X('Date:T', title='time'),
            alt.Y('value:Q', title='temperature in °C'),
            color=alt.Color(
                'variable', 
                scale=alt.Scale(domain=DOMAIN, range=RANGE),
                legend=alt.Legend(title="Legend")
                )
            ).properties(
                width=700,
                height=350
                )

    folium.features.VegaLite(chart.to_json(), width=900, height=350).add_to(popup)
    folium.Marker(
        data[['Lat', 'Lon']].values[0], 
        popup=popup, 
        tooltip='Start'
        ).add_to(m)

    # Create marker for end of transport
    popup = folium.Popup()
    plot_data_path = os.path.join(transport._postprocesspath_arrival, 'arrival.csv')
    # If values for arrival are available, create popup graph
    if os.path.exists(plot_data_path):
        plot_data = pd.read_csv(plot_data_path)
        plot_data['time'] = (plot_data['time']) / 3600
        plot_data['arrival_temperature'] = transport.arrival_temperature
        plot_data = plot_data.melt(id_vars=['time'], value_vars=['temperature', 'arrival_temperature'])
        chart = alt.Chart(plot_data).mark_line().encode(
                alt.X('time', title='time'),
                alt.Y('value:Q', title='temperature in °C'),
                color=alt.Color(
                    'variable', 
                    scale=alt.Scale(domain=['arrival_temperature', 'temperature'], range=RANGE),
                    legend=alt.Legend(title="Legend")
                    )
                ).properties(
                    width=700,
                    height=350
                    )
        folium.features.VegaLite(chart.to_json(), width=900, height=350).add_to(popup)

    folium.Marker(
        data[['Lat', 'Lon']].values[-1], 
        popup=popup, 
        tooltip='End'
        ).add_to(m)

    def plot_stop(stop):
        icon = plugins.BeautifyIcon( 
            background_color=colormap(stop['average_air'].mean()),  
            icon_shape='doughnut',
            icon='circle',
            text_color='#000', 
            border_color='transparent'
        )
        stop_popup = folium.Popup()

        plot_data = pd.DataFrame({
            'timestamps': stop['timestamps'],
            'ambient': stop['ambient'],
            'average_air': stop['average_air']
        })
        plot_data = plot_data.melt(id_vars=['timestamps'], value_vars=['ambient', 'average_air'])
        chart = alt.Chart(plot_data).mark_line(point=True).encode(
            alt.X('timestamps:T', title='time'),
            alt.Y('value:Q', title='temperature in °C'),
            color=alt.Color(
                'variable', 
                scale=alt.Scale(domain=DOMAIN, range=RANGE),
                legend=alt.Legend(title="Legend")
                )
            ).properties(
                width=500,
                height=250
                )

        folium.features.VegaLite(chart.to_json(), width=680, height=250).add_to(stop_popup)

        tooltip = """
            <h4>Stop</h4>
            <b>Start:</b> {start} <br>
            <b>End:</b> {end} <br>
            """
        
        folium.Marker(
            location=[stop.Lat, stop.Lon],
            popup = stop_popup,
            tooltip = tooltip.format(
                start = stop['start'],
                end = stop['end']
                )
            ).add_to(fg_stops)

        folium.Marker(
            location=[stop.Lat, stop.Lon],
            icon = icon
            ).add_to(fg_waypoints)

    def plot_waypoint(waypoint):
        html = """
            <b>Time:</b> {time} <br>
            <b>Ambient temperature:</b> {ambient} <br>
            <b>Air temperature:</b> {air} <br>
            """
        # if waypoint['average_air'] = float('nan'):
        #     waypoint['average_air'] 
        icon = plugins.BeautifyIcon( 
            background_color=colormap(waypoint['average_air']),  
            icon_shape='doughnut',
            icon='circle',
            # border_width = 1,
            text_color='#000', 
            border_color='transparent'
        )
        folium.Marker(
            location=[waypoint.Lat, waypoint.Lon],
            icon = icon,
            popup = folium.Popup(
                html.format(
                    time = waypoint['Date'],
                    ambient = waypoint['ambient'],
                    air = waypoint['average_air']
                    ), max_width=200)
            ).add_to(fg_waypoints)
   
    folium.PolyLine(coordinates[['Lat', 'Lon']].values, color=TUMBLUE).add_to(m)

    # Plot markers for waypoints and stops
    waypoints.apply(plot_waypoint, axis = 1)
    stops.apply(plot_stop, axis = 1)

    folium.LayerControl(collapsed=False).add_to(m)
    colormap.add_to(m)

    result_path = os.path.join(transport.path, 'visualization.html')
    m.save(result_path)

def _tikz_plot(plotpath):
    filename = os.path.splitext(os.path.basename(plotpath))[0] + '.pgf'
    plotpath = os.path.join(os.path.dirname(plotpath), 'tikz', filename)
    if not os.path.exists(os.path.dirname(plotpath)):
        os.makedirs(os.path.dirname(plotpath))
    tikzplotlib.save(plotpath, externalize_tables = True)

def plot(
    transport, 
    tikz = False, 
    format_ext = '.jpg', 
    dpi = 250, 
    marker = None
    ):

    YLABELS = {
        'heattransfercoefficient': 'heattransfercoefficient in W/(m^2 K)',
        'speed': 'speed in m/s',
        'temperature': 'temperature in °C'
    }
    
    files =  glob.glob(transport._postprocesspath + '/**/*.csv', recursive=True)
    temperature_battery_files = glob.glob(transport._postprocesspath_temperature + '/battery*.csv')
    temperature_airInside_file = os.path.join(transport._postprocesspath_temperature, 'airInside.csv')
    wallheatflux_files = glob.glob(transport._postprocesspath_wallHeatFlux + '/*.csv')
    arrival_file = os.path.join(transport._postprocesspath_arrival, 'arrival.csv')
    probe_files = glob.glob(transport._postprocesspath_probes + '/*.csv')
    remaining_files = glob.glob(transport._postprocesspath + '/*.csv')
    # Stop if no plot data is available
    if not files:
        raise ValueError('No plot data available')

    # Plot temperature data of battery regions
    columnnames = ['min(T)', 'max(T)', 'average(T)']
    for columnname in columnnames:
        fig = plt.figure(1)
        ax = fig.add_subplot(111)
        legendlabels = []
        for filepath in temperature_battery_files:
            regionname = os.path.splitext(os.path.basename(filepath))[0]
            df = pd.read_csv(filepath, sep=',', comment='#')
            ax.plot(df['time'] / 3600, df[columnname], marker = marker)
            legendlabels.append(regionname)

        ax.set_xlabel('time in h')
        ax.set_ylabel('temperature in °C')
        ax.grid(linestyle='--', linewidth=2, axis='y')    
        ax.legend(legendlabels, loc='center left', bbox_to_anchor=(1, 0.5), ncol = ceil(len(legendlabels) / 16))
        plotpath = os.path.join(transport._plotspath, 'batteries_' + columnname + format_ext)
        fig.savefig(plotpath, dpi = dpi, bbox_inches='tight')
        if tikz:
            _tikz_plot(plotpath)
        plt.clf()

    # Plot probes
    for filepath in probe_files:
        df = pd.read_csv(filepath, sep=',', comment='#')
        [plt.plot(df['time'] / 3600, df[str(i)], marker = marker) for i in range(df.shape[1] - 1)]
        plt.xlabel('time in h')
        plt.ylabel(YLABELS['temperature'])
        plt.grid(linestyle='--', linewidth=2, axis='y')
        regionname = os.path.splitext(os.path.basename(filepath))[0]
        plotpath = os.path.join(transport._probesplotspath, regionname + format_ext)
        plt.savefig(plotpath, dpi = dpi)
        if tikz:
            _tikz_plot(plotpath)
        plt.clf()

    # Plot heattransfercoefficient and speed
    for filepath in remaining_files:
        df = pd.read_csv(filepath, names = ['time', 'y_data'])
        plt.step(df['time'] / 3600, df['y_data'], color = TUMBLUE)
        filename = os.path.splitext(os.path.basename(filepath))[0]
        plt.xlabel('time in h')
        plt.ylabel(YLABELS[filename])
        plt.grid(linestyle='--', linewidth=2, axis='y')
        plotpath = os.path.join(transport._plotspath, filename + format_ext)
        plt.savefig(plotpath, dpi = dpi)
        if tikz:
            _tikz_plot(plotpath)
        plt.clf()

    # Plot airInside
    if os.path.exists(temperature_airInside_file):    
        df_airInside = pd.read_csv(temperature_airInside_file) 
        df_airInside['ambient'] = transport.weatherdata['T']
        plt.plot(df_airInside['time'] / 3600, df_airInside['ambient'], marker = marker, color = TUMBLUE)
        plt.plot(df_airInside['time'] / 3600, df_airInside['average(T)'], marker = marker, color = TUMORANGE)
        plt.xlabel('time in h')
        plt.ylabel(YLABELS['temperature'])
        plt.grid(linestyle='--', linewidth=2, axis='y')
        plt.legend(['ambient temperature', 'average air temperature'], loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol = 2) 
        plotpath = os.path.join(transport._plotspath, 'plot' + format_ext)
        plt.savefig(plotpath, dpi = dpi, bbox_inches='tight')
        if tikz:
            _tikz_plot(plotpath)
        plt.clf()

    # Plot aarrival
    if os.path.exists(arrival_file):    
        df = pd.read_csv(arrival_file) 
        plt.plot(df['time'] / 3600, df['temperature'], marker = marker, color = TUMBLUE)
        plt.xlabel('time in h')
        plt.ylabel(YLABELS['temperature'])
        plt.grid(linestyle='--', linewidth=2, axis='y')
        plotpath = os.path.join(transport._plotspath, 'arrival' + format_ext)
        plt.savefig(plotpath, dpi = dpi, bbox_inches='tight')
        if tikz:
            _tikz_plot(plotpath)
        plt.clf()