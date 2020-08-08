import pandas as pd
import geopandas as gpd
import json

from bokeh.plotting import figure
from bokeh.palettes import all_palettes 
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.io import curdoc
from bokeh.models import Slider, HoverTool
from bokeh.layouts import widgetbox, column

from utils import *


# This function is used at the end this file and is used to update the plot
#   Not placed in utils because it uses a few globals from this file
def update_plot(attr, old, new):
    """Updates the bokeh plot
        This is a function given by the Bokeh module
        Changes the geojson data based on the slider year
    """
    yr = slider.value
    new_data = get_json_data(list_of_json_data, yr)
    geosource.geojson = new_data
    p.title.text = 'NYC Property Sales in %d' %yr


# Data frame for the nyc avergaes
df = pd.read_csv('../data/zipcode_averages_nyc.csv')

# File path for the shape file
fp = '../data/shape-files/zipcode_shapes.shp'
map_df = gpd.read_file(fp)


# Creating a list of all the years needed
years = []
for i in range(2005, 2020):    
    years.append(str(i))

# Getting a list of all dataframes needed from years 2005-2019
list_of_all_df = get_dataframes_for_each_year(df, years)

list_of_all_map_df = []
for df_year in list_of_all_df:
    temp_map = add_averages_to_map_dataframe(df_year, map_df)
    list_of_all_map_df.append(temp_map)


# Getting a custom made colormap out of multiple colormaps from matplotlib
newcolors = get_color_in_rgb_decimal()

# Converting the custom colormap to hex
new_colors_hex = get_color_map_in_hex(newcolors)

# Read data to json
list_of_map_json = [json.loads(map_elem.to_json()) for map_elem in list_of_all_map_df]

# Convert to String like object
list_of_json_data = [json.dumps(map_json_elem) for map_json_elem in list_of_map_json]



# Creating the maps
maps = []

for i in range(len(list_of_map_json)):
    temp_map = create_maps_for_each_year(list_of_json_data[i], list_of_map_json[i], new_colors_hex)
    maps.append(temp_map)
    


#Input GeoJSON source that contains features for plotting.
geosource = GeoJSONDataSource(geojson = get_json_data(list_of_json_data, 2005))

# Using the converted matplotlib colors
final_palette = new_colors_hex

# Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
max_value = 25000000
color_mapper = LinearColorMapper(palette = final_palette, low = 0, high = max_value, nan_color = '#d9d9d9')

# Define custom tick labels for color bar.
tick_labels = {'0': '$0', '5000000': '$5M', '10000000':'$10M', '15000000':'$15M', '20000000':'$20M', '25000000':'$25M'}

# Add hover tool
hover = HoverTool(tooltips = [ ('Zipcode','@ZIPCODE'),('Property Sale', '@AVERAGES')])

# Create color bar. 
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
                    border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)

# Create figure object.
p = figure(title = 'NYC Property Sales throughout the years', plot_height = 600 , plot_width = 600, toolbar_location = None, tools = [hover])
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

# Add patch renderer to figure. 
p.patches('xs', 'ys', source = geosource, fill_color = {'field' :'AVERAGES', 'transform' : color_mapper},
        line_color = 'black', line_width = 0.25, fill_alpha = 1)

# Specify layout
p.add_layout(color_bar, 'below')

# Make a slider object: slider 
slider = Slider(title = 'Year', start = 2005, end = 2019, step = 1, value = 2005)
slider.on_change('value', update_plot)

# Make a column layout of widgetbox(slider) and plot, and add it to the current document
layout = column(p,widgetbox(slider))
curdoc().add_root(layout)

from bokeh.embed import server_document
script = server_document("https://localhost/5006/bokehplot")
print(script)

# Personal note (when in CTP2020/src directory)
#   conda env list
#   activate ctp