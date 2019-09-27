import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)


# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"api/v1.0/tobs")

# Station Route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a list of stations"""
    results = session.query(Station.station).all()
    session.close()
    
    #Tuples to list
    station_names = list(np.ravel(results))
    
    return jsonify(station_names)

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    """Return a list of all precipitation data"""
    results = session.query(Measurement.prcp, Measurement.date).all()
    session.close()
    
    all_precipitation = []
    for prcp, date in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_precipitation.append(prcp_dict)

    # Tuples to list
    # p/recip_data = list(np.ravel(results))
    
    return jsonify(all_precipitation)

# TObs Route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    """Return a list of TObs for the previous year"""
    results = session.query(Measurement.tobs).\
        filter(func.strftime(Measurement.date) > '2016-08-23').all()
    session.close()

    #Tuples to list
    temp_data = list(np.ravel(results))

    return jsonify(temp_data)

# Select a year route
@app.route("/api/v1.0/tobs/<date>")
def tobs_by_date(date):
    session = Session(engine)
    sel = [Measurement.date,
           func.avg(Measurement.tobs),
           func.max(Measurement.tobs),
           func.min(Measurement.tobs)]
    results = session.query(*sel).\
        filter(func.strftime(Measurement.date) > date).all()

    #Tuples to list
    tobs_by_date = list(np.ravel(results))

    return jsonify(tobs_by_date)

if __name__ == '__main__':
    app.run(debug=True)     