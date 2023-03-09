# Import modules
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

# connect to database
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Flask Setup
app = Flask(__name__)




# Flask Routes

# Start page at homepage-- list all the available routes.
@app.route("/")
def welcome():
    return (
        f"Welcome to the Home Page<br/><br/>"
        f"Available Routes:<br/><br/>"
        f"- Static Routes<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/><br/><br/>"
        f"- Dynamic Routes<br/>"
        f"/api/v1.0/<start><br/><br/>"
        f"* Please input date in the YYYY-MM-DD format.<br/>"
        f"Search for an individual date to get information starting from that date.<br/>"
        f"or<br/>"
        f"Search for a start and end date (ie. date1/date2) to get information in that range. <br/>"
       
    )

# Converting results from precipitation analysis to a dictionary and returning the JSON representation of dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create session
    session = Session(engine)

    # Set up query to get precipitation info    
    precipitation_analysis = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= (dt.date(2017, 8 ,23) - dt.timedelta(days= 365))).\
    order_by(measurement.date).all()

    # Close session
    session.close()

    # Zip lists and create dict
    date = [tple[0] for tple in precipitation_analysis]
    prc = [tple[1] for tple in precipitation_analysis]
    ziplist = dict(zip(date,prc))
    
    # Jsonify results
    return jsonify(ziplist)


# Returning a JSON list of all the stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    # Create session
    session = Session(engine)

    # Set up query to get station list
    station_list = session.query(station.station).all()

    # Close session    
    session.close()

    # Create list with info
    stations = list(np.ravel(station_list))

    # Jsonify results
    return jsonify(stations)



# Return a JSON of dates and temperature observations of the most-active station (USC00519281)for the previous year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    # Create session
    session = Session(engine)

    # Set up query to get tobs
    temp_year = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= (dt.date(2017, 8 ,23) - dt.timedelta(days= 365))).all()
    
    # Close session
    session.close()
    
    # Create list with info using list comprehension
    temp_info = temp_info = [{'date': date, 'tobs': tobs} for date, tobs in temp_year]

    # Jsonify results
    return jsonify(temp_info)


# Defining date function for the next two routes.
def toDate(dateString): 
    return dt.datetime.strptime(dateString, "%Y-%m-%d").date()

# Calculating the TMIN, TAVG, and TMAX for all the dates greater than or equal to the specified start date.
@app.route("/api/v1.0/<start>")
def start_route (start):
    # Create input date variable
    input_date = toDate(start)

    # Create session
    session = Session(engine)
    
    # Set up query to get results
    temp_results = (session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= input_date).group_by(measurement.date).all())
   
    # Close session
    session.close()

    # Create list with info using for loop
    temp_list = []
    for date, min, max, avg in temp_results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["min_tobs"] = min
        temp_dict["max_tobs"] = max
        temp_dict["avg_tobs"] = avg
        temp_list.append(temp_dict)
    
    # Jsonify results
    return jsonify(temp_list)



# Calculating TMIN, TAVG, and TMAX for the specified start date to the specified end date, inclusive.

@app.route("/api/v1.0/<start>/<end>")
def start_end_route (start, end):
    # Create input date variable
    input_start = toDate(start)
    input_end = toDate(end)
    
    
    # Create session
    session = Session(engine)

    # Set up query to get results
    start_end_results = (session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= input_start, measurement.date <= input_end).group_by(measurement.date).all())

    # Close session
    session.close()

    # Create list with info using for loop
    start_end_temp_list = []
    for date, min, max, avg in start_end_results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["min_tobs"] = min
        temp_dict["max_tobs"] = max
        temp_dict["avg_tobs"] = avg
        start_end_temp_list.append(temp_dict)
    
    # Jsonify results
    return jsonify(start_end_temp_list)
    


if __name__ == '__main__':
    app.run(debug=True)
