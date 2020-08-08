# CTP2020 Project - Property Sale Averages

## Table of contents
1. [Sources](#sources)
2. [What am I looking at?](#description)
3. [What happened during the creation of the project?](#outline)
4. [Setup](#setup)
5. [Possible future additions](#future)

## Sources: <a name="sources"></a>
- ### Propery sale averages by zipcode
https://www1.nyc.gov/site/finance/taxes/property-annualized-sales-update.page
- ### NYC shapefiles by zipcode
https://data.cityofnewyork.us/Business/Zip-Code-Boundaries/i8iw-xf4u/data?no_mobile=true

## What am I looking at? <a name="description"></a>
This is a fun little project to visualize the average NYC property sale by zipcode from 2005 through 2019. By using Bokeh and some other python libraries, I was able to visualize the average property sales per zipcode. I used a shape file to get a map of NYC with zipcode boundaries. Then used public NYC property sales to get the average property sale per zipcode and mapped them to the zipcodes in out graph. By using a slider, the map changes to show the averages for different years.    

## What happened during the creation of the project? <a name="outline"></a>
As I was learning about data science during Spring 2020, we used Jupyter for all of the practice. So, when starting this project, I started it off using Jupyter. The first step after planning and grabbing the proper data, was to clean it up and make sense of it all. There were 5 files of data for each year that had to be condensed into one file. This was mainly done in 'jupyter-files/Data_Cleaning.ipynb'.

Once the data was ready, the next step was to use Geopandas to visualize the plots. But something that became apparent shortly after was that Geopandas did not allow for dynamic plots. After some research and some consulting with my bootcamp instructor, Bokeh seemed to be the best option for this project. This first iteration of the project was done in 'jupyter-files/CTP2020-Project.ipynb'. 

I then created the Bokeh plots out of cleaned up data but then another issue rose. Jupyer did not allow the slider to change the contents of the plot. So, I took all the code from Jupyter and placed it into its own python file. After doing so, I set up a Bokeh server and the plot worked perfect.

The next realization was how ugly the code was. Taking everything out from Jupyter and placing it into its own python file made it evident how sloppy the code was. I refactored some of the code and created some functions to make the code more readable and scalable. Then placed majority of the functions into another file. The code still does not look perfect, but it is in a much better place than what it was before.


## Setup <a name="setup"></a>
- The most updated files of the project is located in the 'src' folder. The main file is 'bokehapp.py' and helper functions can be found in 'utils.py' 
- Since the project does not have a docker file yet for easy replication, you will need to set up your own environment for now. The necessary libraries can be found in 'src/bokehapp.py' and 'src/utils.py'. Just look at the modules that are imported.
- Then in a terminal, move into the 'src' folder and execute the following command:
    - **bokeh serve --show bokehapp.py**
- The project should start to run and the browser will open up localhost and the interactive map should load. This may take a minute or so to load

## Possible future additions <a name="future"></a>
The goal of this project was to get my feet wet in data science by gathering some data and then visualizing it. Now that goal has been reached, there are some cool things that can be added to this project. (Unfortunately, life is taking over at the moment and these additions won't come anytime soon) 
- Make this into a web application. Use Vue or React to create a frontend and then embed these Bokeh plots to the webpage
    - Then deploy the web application
- Use Docker to make this more replicable
- While hovering over the plot, the average is in scientific notation and not in USD
- The Bokeh plot changes quite slowly (i.e. when moving the slider); Would be nice to figure out if it is slow due to the limitations of the Bokeh library or from my messy code
