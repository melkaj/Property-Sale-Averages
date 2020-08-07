# CTP2020
Sources:
https://www1.nyc.gov/site/finance/taxes/property-annualized-sales-update.page
https://data.cityofnewyork.us/City-Government/Property-Valuation-and-Assessment-Data/yjxr-fw8i


## What am I looking at?
This is a fun little project to visualize the average NYC property sale by zipcode from 2005 through 2019. By using Bokeh and some other python libraries, I was able to visualize the average property sales per zipcode. I used a shape file to get a map of NYC with zipcode boundaries. Then used public NYC property sales to get the average property sale per zipcode and mapped them to the zipcodes in out graph. By using a slider, the map changes to show the averages for different years.    

## Time line of the project
As I was learning about data science during Spring 2020, we used Jupyter for all of the practice. So, when starting this project, I started it off using Jupyter. The first step after planning and grabbing the proper data, was to clean it up and make sense of it all. There were 5 files of data for each year that had to be condensed into one file. 

Once the data was ready, the next step was to use Geopandas to visualize the plots. But something that became apparent shortly after was that Geopandas did not allow for dynamic plots. After some research and some consulting with my bootcamp instructor, Bokeh seemed to be the best option for this project. 

I then created the Bokeh plots out of cleaned up data but then another issue rose. Jupyer did not allow the slider to change the contents of the plot. So, I took all the code from Jupyter and placed it into its own python file. After doing so, I set up a Bokeh server and the plot worked perfect.

The next realization was how ugly the code was. Taking everything out from Jupyter and placing it into its own python file made it evident how sloppy the code was. I refactored some of the code and created some functions to make the code more readable and scalable. Then placed majority of the functions into another file. The code still does not look perfect, but it is in a much better place than what it was before.  

## Setup
- Since the project does not have a docker file yet for easy replication, you will need to set up your own environment for now. The necessary libraries can be found in the bokehapp.py file. Just look at the modules that are imported.
- Then in a terminal, go to the root of the project and execute the following command:
    - **bokeh serve --show bokehapp.py**
- The project should start to run and the browser will open up localhost and the interactive map should load. This may take a minute or so to load

## TODO: 
- Add a gif to this readme to show it working
- Since this project was done using an environment in anaconda, get a docker file for easy replication of this project
- Add a proper frontend and deploy this somewhere (if even possible)
- When changing the value of the slider, updating the map is a bit slow. Not too sure if its the limitation of the library, or from sloppy code, or from the amount of data that needs to be shown
- The hovering over the maps to show the zipcode, shows the number in scientific notation. Ideally, it would the number as price with commas  
