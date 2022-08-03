# import dependencies
import datetime as dt
import numpy as np
import pandas as pd
# to connect to sqlite
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# to connect to flask
from flask import Flask, jsonify

# access sqlite database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect databse into classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# variables for each table/class
Measurement = Base.classes.measurement
Station = Base.classes.station

# session link from python to database
session = Session(engine)

# define the flask app
app = Flask(__name__)

# define the welcome route (homepage)
@app.route("/")

# welcome route function, version 1
# <br/> for new line
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    <br/>Available Routes:
    <br/>/api/v1.0/precipitation
    <br/>/api/v1.0/stations
    <br/>/api/v1.0/tobs
    <br/>/api/v1.0/temp/start/end
    ''')

# precipitation route
@app.route("/api/v1.0/precipitation")

# precipitation function
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# stations route
@app.route("/api/v1.0/stations")

# stations function
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# temperature observations route
@app.route("/api/v1.0/tobs")

# temperature function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# statistics routes
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# statistics function
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
