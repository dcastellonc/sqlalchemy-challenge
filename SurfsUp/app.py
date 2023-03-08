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

# Start at the homepage and list all the available routes.
@app.route("/")
def welcome():
    return (
        f"Welcome to the Home Page<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

# Convert results from precipitation analysis to a dictionary.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    precipitation_analysis = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= (dt.date(2017, 8 ,23) - dt.timedelta(days= 365))).\
    order_by(measurement.date).all()

    session.close()

    date = [tple[0] for tple in precipitation_analysis]
    prc = [tple[1] for tple in precipitation_analysis]
    ziplist = dict(zip(date,prc))
    ziplist

    return jsonify(ziplist)

    

# Return a JSON list of stations from the dataset.

# unique stations here:
# @app.route("/api/v1.0/stations")
# def stations():
#     session = Session(engine)

#     station_list = session.query(measurement.station, station.name).filter(measurement.station == station.station).all()
    
#     session.close()

#     station_dict = dict(station_list)
    
#     return jsonify(station_dict)



# ALL stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    all_station_data = session.query(measurement.id, measurement.station).all()

    session.close()

    station_dict = dict(all_station_data)
    return jsonify(station_dict)

# Return a JSON of dates and temperature observations of the most-active station (USC00519281)for the previous year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    temp_year = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= (dt.date(2017, 8 ,23) - dt.timedelta(days= 365))).all()
    temp_dict = dict(temp_year)

    session.close()

    return jsonify(temp_dict)



# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

@app.route("/api/v1.0/<start>")
def start_route ():



    return jsonify(justice_league_members)


@app.route("/api/v1.0/<start>/<end>")
def start_route ():



    return jsonify(justice_league_members)


if __name__ == '__main__':
    app.run(debug=True)
