# CTP2020
Sources:
https://www1.nyc.gov/site/finance/taxes/property-annualized-sales-update.page
https://data.cityofnewyork.us/City-Government/Property-Valuation-and-Assessment-Data/yjxr-fw8i


## What am I looking at?
This is a fun little project to visualize the average NYC property sale by zipcode from 2005 through 2019. By using Bokeh and some other python libraries, we were able to visualize the property sales. We used a shape file to get us a map of NYC with zipcode boundaries. Then we used public NYC property sales to get the average property sale per zipcode and mapped them to the zipcodes in out graph. By using a slider, the map changes to show the averages for different years.    

The data was gathered from the sources above. Used pandas to clean it up and put everything into one file. In the 
data folder, you will find a bunch of different csv files, but the most important one is the zipcode_averages_nyc.csv file which holds all the averages needed. This is my first data science/data visualization project, so the data cleaning definitly is not the most efficient and not perfect. However, we were able to get the project to work on out local machine. We used Bokeh for the data visualization and jupyter for most of the data cleaning and testing. But since Bokeh in jupyter does not allow for dynamically changing maps, we had to take all the code from jupyter and place it into a regular python file. From there, we can start a bokeh serve and get the interactive maps to run on localhost. 

## TODO: 
- Clean up the code in the main file. i.e. adding the functions in another file and even a class if it makes sense. 
- Add a gif to this readme to show it working
- Since this project was done using an environment in anaconda, get a docker file for easy replication of this project
- Add a proper frontend and deploy this on heroku (or host it somewhere)
