# sqlalchemy-challenge
## Instructions 
You've decide to do a climate analysis for Hawaii. The following sections outline the steps that you need to take to accomplish this task.

### Part 1: Analyze and Explore the Climate Data
Use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib. To do so, 

 Use the provided files (climate_starter.ipynb and hawaii.sqlite) to complete the climate analysis and data exploration.

- Complete the following steps:
    - Use the SQLAlchemy create_engine() function to connect to your SQLite database.
    - Use the SQLAlchemy automap_base() function to reflect your tables into classes, and then save references to the classes named station and measurement.
    - Link Python to the database by creating a SQLAlchemy session.
    - Perform a precipitation analysis and then a station analysis by completing the steps in the following two subsections.

*Precipitation Analysis*

- Find the most recent date in the dataset.
Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.

*Station Analysis*
- Calculate the total number of stations in the dataset.
- Find the most-active stations (that is, the stations that have the most rows).
- Plot the results as a histogram with bins=12, as the following image shows:


### Part 2: Design Your Climate App
Design a Flask API based on the queries that you just developed in the analysis. Use Flask to create your routes as follows:

- (/)
Start at the homepage.
List all the available routes.
- (/api/v1.0/precipitation) Convert the query results from your precipitation analysis and return the JSON representation of your dictionary.
- (/api/v1.0/stations) Return a JSON list of stations from the dataset.
- (/api/v1.0/tobs) Query dates and temperature observations of the most-active station for the previous year of data. Return a JSON list of temperature observations for the previous year.
- (/api/v1.0/<start> and /api/v1.0/<start>/<end>)
Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range. Calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.


