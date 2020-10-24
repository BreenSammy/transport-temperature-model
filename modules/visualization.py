import copy
from math import floor
import os
import json

import altair as alt
import branca
import geopy.distance
import folium
from folium import plugins
from matplotlib import cm
import numpy as np
import pandas as pd

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
    step = floor(256/steps)
    return [cm.jet(i) for i in range(0, 256, step)]

def filter_stops(waypoints):
    """Method to filter stop locations from all waypoints"""
    coordinates = waypoints[['Lat', 'Lon']].values
    stop_list = []
    stops = pd.DataFrame()

    for i in range(len(waypoints) - 1):
        distance = geopy.distance.distance(coordinates[i, :],coordinates[i + 1, :]).km
        if distance <= 10: 
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
            new_stop = pd.DataFrame(
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
            new_stop.at[0, 'timestamps'] = df['Date'].values
            new_stop.at[0, 'ambient'] = df['ambient'].values
            new_stop.at[0, 'average_air'] = df['average_air'].values
            # Concat stops
            stops = pd.concat([stops, new_stop])
            stop_list = []

    # Reindex dataframes
    waypoints.index = range(len(waypoints.index))
    stops.index = range(len(stops.index))

    return waypoints, stops

def create(transport):

    data = copy.deepcopy(transport.weatherdata)
    data.rename(columns = {'T':'ambient'}, inplace = True) 
    temperature_air = transport.read_postprocessing('airInside')
    data['average_air'] = temperature_air['average(T)']
    # Transform datetime objects to strings
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    coordinates = data[['Lat', 'Lon']].values
    data = data.round({'average_air': 3})

    waypoints, stops = filter_stops(data)

    start_lat = data[['Lat']].values.mean()
    start_lon = data[['Lon']].values.mean()

    m = folium.Map(
        location=[start_lat, start_lon],
        zoom_start=7,
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
            )

    folium.features.VegaLite(chart.to_json()).add_to(popup)
    folium.Marker(
        data[['Lat', 'Lon']].values[0], 
        popup=popup, 
        tooltip='Start'
        ).add_to(m)

    # Create marker for end of transport
    popup = folium.Popup()
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
            )

        folium.features.VegaLite(chart.to_json()).add_to(stop_popup)

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
   
    folium.PolyLine(coordinates, color=TUMBLUE).add_to(m)

    # Plot markers for waypoints and stops
    waypoints.apply(plot_waypoint, axis = 1)
    stops.apply(plot_stop, axis = 1)

    folium.LayerControl(collapsed=False).add_to(m)
    colormap.add_to(m)

    result_path = os.path.join(transport.path, 'visualization.html')
    m.save(result_path)



