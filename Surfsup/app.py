
# import modules
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# Set database and reflect the tables
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create an app and pass name
app = Flask(__name__)


# Create route for home and list routes on server 
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"SQLAlchemy Challenge </br>"
        f"Please review the following routes:</br>"
        f"<ul>"
        f"<li>/api/v1.0/precipitation</li>"
        f"<li>/api/v1.0/stations</li>"
        f"<li>/api/v1.0/tobs</li>"
        f"<li>/api/v1.0/2010-01-06</li>"
        f"<li>/api/v1.0/2010-01-06/2017-08-23</li>"
        f"<li>/about</li>"
        f"</ul>"
    )


# create route for /about path and define content
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return(
        f"SQLAlchemy About</br>"
        f"In this challenge, the climate was analyzed in Honolulu, Hawaii<br/>"
        f"to determine the best time to take a vacation to the island."
    ) 

# create route for /api/v1.0/precipitation and query data
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Servier received request for '/api/v1.0/precipitation'...")
    # start session from Python to database
    session = Session(engine) 
    # query date and precipitation from database
    data_precip = session.query(Measurement.date, Measurement.prcp)\
        .order_by(Measurement.date.desc())\
        .filter(Measurement.date > '2016-08-23').all()
    # close session
    session.close()

    # for loop to create a dictionary for date
    precip_dictionary = {}
    for date, prcp in data_precip:
    
        if date not in precip_dictionary:
            precip_dictionary[date] = []
            precip_dictionary[date].append(prcp)
        # if same date appears, then add to the list
        else:
            precip_dictionary[date].append(prcp)

    return jsonify(precip_dictionary)

# create route /api/v1.0/stations
@app.route("/api/v1.0/stations")
def station():
    print("Servier received request for '/api/v1.0/stations'.")
    # start session from Python to the database
    session = Session(engine) 
    # query date and precipitation from database
    stations = session.query(Station.name).all()
    # close session
    session.close()

    return jsonify(stations)

# create route <li>/api/v1.0/tobs</li>
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for '/api/v1.0/tobs'...")
     # create session from Python to the database
    session = Session(engine) 
    # query date and precipitation from database
    station_yr = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == 'USC00519281')\
        .filter(Measurement.date >= '2016-08-23').all()
    # close session
    session.close()

    # print the temperture from the most active station
    stat_list = list(np.ravel(station_yr))

    return jsonify(stat_list)

# create route /api/v1.0/<start>

@app.route("/api/v1.0/<start>")
def date_starts(start):
    print("Server received request for '/api/v1.0/<start>'...")
     # create session from Python to the database
    session = Session(engine) 
    
    # query date and precipitation from database
    stat_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.station == 'USC00519281')\
        .filter(Measurement.date >= start).first()
    # close session
    session.close()

    # create dictionary with lowest, average, and highest temp
    temps_dict = {"Low Temp": stat_results[0], "Average Temp": stat_results[1], "Hi Temp": stat_results[2]}

    return jsonify(temps_dict)

# create route /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>/<end>")
def date_start_end(start, end):
    print("Server received request for '/api/v1.0/<start>/<end>'...")
     # create session from Python to the database
    session = Session(engine) 
    # query start date, end date, and TOBS data from database 
    stat_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.station == 'USC00519281')\
        .filter(Measurement.date <= end)\
        .filter(Measurement.date >= start).first()
    # close session
    session.close()

    # create dictionary
    temps = {"Low Temp": stat_results[0], "Average Temp": stat_results[1], "Hi Temp": stat_results[2]}

    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)