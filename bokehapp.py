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



# Data frame for the nyc avergaes
# df = pd.read_csv('../data/zipcode_averages_nyc.csv')
df = pd.read_csv('./data/zipcode_averages_nyc.csv')

# File path for the shape file
fp = './data/shape-files/zipcode_shapes.shp'
map_df = gpd.read_file(fp)



# Function to take dataframe and map dataframe, find all the averages per zipcode and add these averages to the 
#     map dataframe
def add_averages_to_map_dataframe(dataframe, map_dataframe):
    boroughs = ["BROOKLYN", "BRONX", "QUEENS", "MANHATTAN", "STATEN ISLAND"]
    temp_map_dataframe = map_dataframe.copy()
    
    # Renaming columns
    dataframe.columns = boroughs
    # Adding the zipcodes as a column entry (before it was just the name of the index)
    dataframe['ZIPCODES'] = list(dataframe.index)
    
    #     Iterating through all columns (each column is a borough)
    #     But a zipcode is only located in one of the 5 boroughs. So, one column will 
    #     hold a useful value while the other 4 will hold NaN
    #     We are finding that useful value and ignoring the NaN
    averages = []
    for index, row in dataframe.iterrows():
        temp = 0
        for bor in boroughs:
            if (not(math.isnan(row[bor]))):
                temp = row[bor]
        averages.append(temp)
    # Adding the values found for each zipcode as its own column in the dataframe
    dataframe['AVERAGES'] = averages
    
    # The dataframe might not have all the same zipcodes as the map dataframe, so we need to give them values
    list_of_zipcodes_old = list(dataframe.index)
    list_of_zipcodes_new = list(temp_map_dataframe['ZIPCODE'])
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
    temp_map_dataframe['AVERAGES'] = new_average_list
    return temp_map_dataframe


def get_dataframes_for_each_year(main_dataframe, years):
    temp = []
    for i in years:
        temp_dataframe = main_dataframe.loc[ (main_dataframe['year'] == i) ].T
        # Getting rid of the first two rows 
        temp_dataframe = temp_dataframe.iloc[2:]
        temp.append(temp_dataframe)
    return temp



years = []
for i in range(2005, 2020):    
    years.append(str(i))

list_of_all_map_df = []
list_of_all_df = get_dataframes_for_each_year(df, years)

for df_year in list_of_all_df:
    temp_map = add_averages_to_map_dataframe(df_year, map_df)
    list_of_all_map_df.append(temp_map)



import re
def rgb_to_hex(rgb_color):
    
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

# Test
hex_output = rgb_to_hex([7,110,190])
print(hex_output)
    


# Custom colormap from matplotlib
a = cm.get_cmap('cool', 32)
b = cm.get_cmap('spring', 32)
c = cm.get_cmap('autumn_r', 64)
d = cm.get_cmap('bwr_r', 192)
e = cm.get_cmap('Greens', 192)

newcolors = np.vstack((a(np.linspace(0, 1, 32)), 
                       b(np.linspace(0, 1, 32)), 
                       c(np.linspace(0, 1, 64)),
                       d(np.linspace(0, 0.5, 192)),
                       e(np.linspace(0, 1, 192)),
                      ))

# Converting matplotlib colormap to something to be used in Bokeh
new_colors_hex = []
for i in range(len(newcolors)):
    rgb = []
    for j in range(3):
        num = int(newcolors[i][j] * 255)
        rgb.append(num)
    new_colors_hex.append(rgb_to_hex(rgb))



#Read data to json.
# map_json = json.loads(map_df.to_json())
list_of_map_json = [json.loads(map_elem.to_json()) for map_elem in list_of_all_map_df]

#Convert to String like object.
# json_data = json.dumps(map_json)
list_of_json_data = [json.dumps(map_json_elem) for map_json_elem in list_of_map_json]

print(len(list_of_map_json))
print(len(list_of_json_data))



def create_maps_for_each_year(json_data, map_json):
    #Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson = json_data)

    # Using the converted matplotlib colors
    final_palette = new_colors_hex

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



# Creating the maps
maps = []

for i in range(len(list_of_map_json)):
    temp_map = create_maps_for_each_year(list_of_json_data[i], list_of_map_json[i])
    maps.append(temp_map)
    
print(type(maps[0]))



from bokeh.io import curdoc, output_notebook
from bokeh.models import Slider, HoverTool
from bokeh.layouts import widgetbox, row, column

#Define function that returns json_data for year selected by user.    
def get_json_data(selectedYear):
    index = int(selectedYear) - 2005
    print(index)
    return list_of_json_data[index]
#     df_yr = df[df['year'] == yr]
#     merged = gdf.merge(df_yr, left_on = 'country_code', right_on = 'code', how = 'left')
#     merged.fillna('No data', inplace = True)
#     merged_json = json.loads(merged.to_json())
#     json_data = json.dumps(merged_json)
#     return json_data

#Input GeoJSON source that contains features for plotting.
geosource = GeoJSONDataSource(geojson = get_json_data(2005))
print(type(geosource))

# Using the converted matplotlib colors
final_palette = new_colors_hex

#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
max_value = 25000000
color_mapper = LinearColorMapper(palette = final_palette, low = 0, high = max_value, nan_color = '#d9d9d9')

#Define custom tick labels for color bar.
tick_labels = {'0': '$0', '5000000': '$5M', '10000000':'$10M', '15000000':'$15M', '20000000':'$20M', '25000000':'$25M'}

#Add hover tool
hover = HoverTool(tooltips = [ ('Zipcode','@ZIPCODE'),('Property Sale', '@AVERAGES')])

#Create color bar. 
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
                     border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)

#Create figure object.
p = figure(title = 'NYC Property Sales throughout the years', plot_height = 600 , plot_width = 600, toolbar_location = None, tools = [hover])
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

#Add patch renderer to figure. 
p.patches('xs', 'ys', source = geosource, fill_color = {'field' :'AVERAGES', 'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)

#Specify layout
p.add_layout(color_bar, 'below')

# Define the callback function: update_plot
def update_plot(attr, old, new):
    yr = slider.value
    new_data = get_json_data(yr)
    geosource.geojson = new_data
    p.title.text = 'NYC Property Sales in %d' %yr
    
# Make a slider object: slider 
slider = Slider(title = 'Year', start = 2005, end = 2019, step = 1, value = 2005)
slider.on_change('value', update_plot)

# Make a column layout of widgetbox(slider) and plot, and add it to the current document
layout = column(p,widgetbox(slider))
curdoc().add_root(layout)

# #Display plot inline in Jupyter notebook
# output_notebook()

# #Display plot
# show(layout)