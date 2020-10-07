import gpxpy 
import numpy as np
import pandas as pd

def coordinates(filename):
    """Reads coordinates from gpx file"""
    amount_points = 0
    counter_points = 0

    # Open and parse gpx file
    gpx_file = open(filename, 'r') 
    gpx = gpxpy.parse(gpx_file)

    # Preallocate memory for coordinates
    for track in gpx.tracks: 
        for segment in track.segments: 
            for point in segment.points: 
                    amount_points = amount_points + 1
    coordinates = np.zeros([amount_points, 2])

    # Fill coordinates array
    for track in gpx.tracks: 
        for segment in track.segments: 
            for point in segment.points: 
                coordinates[counter_points, :] = [point.latitude, point.longitude]
                counter_points = counter_points + 1
    
    return coordinates

def dataframe(filename):
    """Reads point time and position as pandas dataframe"""
    # Open and parse gpx file
    gpx_file = open(filename, 'r') 
    gpx = gpxpy.parse(gpx_file)

    df_list = []
    for track in gpx.tracks: 
        for segment in track.segments: 
            for point in segment.points: 
                    data = {
                        'Date': [point.time],
                        'Lat': [point.latitude],
                        'Lon': [point.longitude]
                    }
                    df = pd.DataFrame(data = data, columns = ['Date', 'Lat', 'Lon'])
                    df_list.append(df)

    return pd.concat(df_list)