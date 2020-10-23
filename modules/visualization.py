import copy
import os
import json

import altair as alt
import branca
import geopandas as gpd
import folium
from folium import plugins
from folium.features import GeoJson, GeoJsonTooltip, GeoJsonPopup
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

def jet():
    return [cm.jet(i) for i in range(256)]

def create(transport):

    data = copy.deepcopy(transport.weatherdata)
    temperature_air = transport.read_postprocessing('airInside')
    data['average_air'] = temperature_air['average(T)']
    # Transform datetime objects to string
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')

    data = gpd.GeoDataFrame(
        data, geometry=gpd.points_from_xy(data.Lon, data.Lat), crs='EPSG:4326')
    data.to_file("countries.geojson", driver='GeoJSON')
    
    start = data[['Lat', 'Lon']].values[0]
    coordinates = data[['Lat', 'Lon']].values

    data = data.round({'average_air': 3})
    print(data)
    m = folium.Map(
        location=start,
        zoom_start=7,
        tiles='Cartodb Positron'
        )

    fg_waypoints = folium.FeatureGroup(name='Waypoints')
    m.add_child(fg_waypoints)

    colormap = branca.colormap.LinearColormap(jet(), index=None, vmin=-10, vmax=50, caption='')

    # print(colormap(10))
    # g1 = plugins.FeatureGroupSubGroup(fg, 'group1')
    # m.add_child(g1)

    # g2 = plugins.FeatureGroupSubGroup(fg, 'group2')
    # m.add_child(g2)

    popup = GeoJsonPopup(
        fields=['Date','T'],
        aliases=['Time',"Ambient temperature"]
    )

    tooltip = GeoJsonTooltip(
        fields=['Date','T', 'average_air'],
        aliases=['Time',"Ambient temperature", "Air temperature"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )

    html = """
        <b>Time:</b> {time} <br>
        <b>Ambient temperature:</b> {ambient} <br>
        <b>Air temperature:</b> {air} <br>
        """

    # iframe = branca.element.IFrame(html=html, width=500, height=300)
    # popup = folium.Popup(iframe, max_width=500)

    def plot_waypoint(waypoint):
        temperature = waypoint['T']
        icon = plugins.BeautifyIcon( 
            background_color=colormap(temperature),  
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
                    ambient = waypoint['T'],
                    air = waypoint['average_air']
                    ), max_width=200)
            ).add_to(fg_waypoints)
   
    route = folium.PolyLine(coordinates, color=TUMBLUE).add_to(m)

    data.apply(plot_waypoint, axis = 1)
    # plugins.PolyLineTextPath(
    #     route,
    #     'Transport route',
    #     offset=-5
    #     ).add_to(m)

    # g = folium.GeoJson(
    #     data,
    #     tooltip=tooltip,
    #     popup=popup
    # ).add_to(fg_waypoints)

    


        # for feature in gj.data['features']:
        # if feature['geometry']['type'] == 'Point':
        #     folium.Marker(location=list(reversed(feature['geometry']['coordinates'])),
        #                   icon=folium.Icon(
        #                       icon_color='#ff033e',
        #                       icon='certificate',
        #                       prefix='fa')
        #                   ).add_to(layer)

    folium.LayerControl(collapsed=False).add_to(m)
    colormap.add_to(m)

    result_path = os.path.join(transport.path, 'visualization.html')
    m.save(result_path)

# create(transport1)


# chart_json = json.loads(chart.to_json())

# popup = folium.Popup(max_width=650)
# folium.features.VegaLite(chart_json, height=350, width=650).add_to(popup)
# folium.Marker([30, -80], popup=popup).add_to(m)



