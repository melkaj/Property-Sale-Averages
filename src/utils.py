
import pandas as pd
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.pyplot as plt
import geopandas as gpd
import csv
import json
import math

from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer
from bokeh.palettes import all_palettes 
import colorcet as cc


from bokeh.io import curdoc, output_notebook
from bokeh.models import Slider, HoverTool
from bokeh.layouts import widgetbox, row, column



# Function to take dataframe and map dataframe, find all the averages per zipcode and add these averages to the 
#     map dataframe
def add_averages_to_map_dataframe(dataframe, map_dataframe):
    """Returns the map_dataframe but with an additional column that holds the averages per zipcode

    @param  dataframe       A dataframe with the appropriate averages from a specific year
    @param  map_dataframe   A dataframe with the zipcode shapes
    """

    # List of boroughs
    boroughs = ["BROOKLYN", "BRONX", "QUEENS", "MANHATTAN", "STATEN ISLAND"]
    
    # Making a copy of the original map_dataframe
    map_dataframe_copy = map_dataframe.copy()
    
    # Renaming columns
    dataframe.columns = boroughs
    # Adding a new column named 'ZIPCODES' and its value will be the actual zipcodes from each borough
    dataframe['ZIPCODES'] = list(dataframe.index)
    
    # 
    #     Iterating through all columns (each column is a borough)
    #     But a zipcode is only located in one of the 5 boroughs. So, one column will 
    #     hold a useful value while the other 4 will hold NaN
    # Dataframe looks like this:
    #       BROOKLYN    BRONX   QUEENS  MANHATTAN   STATENISLAND
    # 11214   400k       Nan      NaN      NaN          NaN
    # 10303   NaN        NaN      NaN      NaN          700k
    #     We are finding that useful value and ignoring the NaN
    #     Creating a list that looks like the following, however the zipcode is implicit:
    #       AVERAGE
    #        400k           (zipcode is 11214)
    #        700k           (zipcode is 10303) 
    averages = []
    for index, row in dataframe.iterrows():
        average = 0
        for bor in boroughs:
            if (not(math.isnan(row[bor]))):
                average = row[bor]
        averages.append(average)
    # Adding the values found for each zipcode as its own column in the dataframe
    dataframe['AVERAGES'] = averages
    
    # The ZIPCODE column on the dataframe might not exactly match the ZIPCODE column in the map_dataframe
    #       (as they were taken from two different sources)
    # so, we need to match them up
    list_of_zipcodes_old = list(dataframe.index)
    list_of_zipcodes_new = list(map_dataframe_copy['ZIPCODE'])
    new_average_list = []

    for zip in list_of_zipcodes_new:
        if zip in list_of_zipcodes_old:
            index = list_of_zipcodes_old.index(zip)
            new_average_list.append(averages[index])
        else:
            new_average_list.append(0)
            
    # Dropping columns that are not needed (the boroughs)
    dataframe = dataframe.drop(boroughs, axis=1)

    # Adding a new column to the shape dataframe to hold the averages
    map_dataframe_copy['AVERAGES'] = new_average_list
    return map_dataframe_copy


def match_list_values(list_one, list_two):
    matched_list = []

    for zip in list_two:
        if zip in list_one:
            index = list_one.index(zip)
            matched_list.append(averages[index])
        else:
            matched_list.append(0)


def get_dataframes_for_each_year(main_dataframe, years):
    """Returns a list of dataframes based on the array given

    @param  main_datafram   A dataframe with all the available zipcode averages
    @param  years           List of strings. String should be a 'year' i.e. ['2005', '2006']
    """
    list_of_dataframes = []
    for year in years:
        dataframe_by_year = main_dataframe.loc[ (main_dataframe['year'] == year) ].T
        # Getting rid of the first two rows 
        dataframe_by_year = dataframe_by_year.iloc[2:]
        list_of_dataframes.append(dataframe_by_year)
    return list_of_dataframes

    
import re
def rgb_to_hex(rgb_color):
    """Converts rgb color format to rgb hexidecimal and returns hex string
        Bokehs colormaps are in hexidecimal and matplotlibs are in decimal
        This conversion will help build a custom colormap for the bokeh graphs
        
    @param  rgb_color   List of 3 integers. Each integer represents the r g & b values
    EX: rgb_to_hex([7,102, 230])
        returns #0766e6
    """
    
    [r,g,b] = rgb_color
    
    # check if in range 0~255
    assert 0 <= r <= 255
    assert 0 <= g <= 255
    assert 0 <= b <= 255
 
    r = hex(r).lstrip('0x')
    g = hex(g).lstrip('0x')
    b = hex(b).lstrip('0x')
    # re-write '7' to '07'
    r = (2 - len(r)) * '0' + r
    g = (2 - len(g)) * '0' + g
    b = (2 - len(b)) * '0' + b
 
    hex_color = '#' + r + g + b
    return hex_color


def create_maps_for_each_year(json_data, map_json, final_color_palette):
    #Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson = json_data)

    # Using the converted matplotlib colors
    final_palette = final_color_palette

    #Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
    max_value = 25000000
    color_mapper = LinearColorMapper(palette = final_palette, low = 0, high = max_value)


    #Define custom tick labels for color bar.
    tick_labels = {'0': '$0', '5000000': '$5M', '10000000':'$10M', '15000000':'$15M', '20000000':'$20M', '25000000':'$25M'}

    #Create color bar. 
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width = 500, height = 20, border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)

    #Create figure object.
    p = figure(title = 'NYC Property Sales in 2005', plot_height = 600 , plot_width = 600, toolbar_location = None)
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    #Add patch renderer to figure. 
    p.patches('xs','ys', source = geosource,fill_color = {'field' :'AVERAGES', 'transform' : color_mapper}, line_color = 'black', line_width = 0.25, fill_alpha = 1)

    #Specify figure layout.
    p.add_layout(color_bar, 'below')
    
    return p


#Define function that returns json_data for year selected by user.    
def get_json_data(list_of_json_data, selectedYear):
    index = int(selectedYear) - 2005
    print(index)
    return list_of_json_data[index]