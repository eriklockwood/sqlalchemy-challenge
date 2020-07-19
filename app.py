import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# setup engine
engine = create_engine("sqlite:///../Instructions/Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/\<start\><br/>"
        f"/api/v1.0/\<starts\>/\<ends\><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return all precipitation data"""
    # Query all precipitation data
    results = session.query(Measurement.date, Measurement.station, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    for date, station, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["station"] = station
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return all tobs data"""
    # Query all tobs data
    results = session.query(Measurement.date, Measurement.station, Measurement.tobs).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = []
    for date, station, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["station"] = station
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    """Return a JSON list of the minimum temperature, the average
       temperature, and the max temperature for a given start range"""

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date > start).all()

    session.close()

    #create dict of start_tobs row data
    start_tobs = []
    for date, station, tobs in results:
        start_dict = {}
        start_dict["date"] = date
        start_dict["station"] = station
        start_dict["tobs"] = tobs
        start_tobs.append(start_dict)

    return jsonify(start_tobs)    

@app.route("/api/v1.0/<starts>/<ends>")
def end(starts,ends):
    """Return a JSON list of the minimum temperature, the average
       temperature, and the max temperature for a given start to end range"""

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date > starts).filter(Measurement.date < ends).all()

    session.close()

    #create dict of start_tobs_ends row data
    start_end_tobs = []
    for date, station, tobs in results:
        end_dict = {}
        end_dict["date"] = date
        end_dict["station"] = station
        end_dict["tobs"] = tobs
        start_end_tobs.append(end_dict)

    return jsonify(start_end_tobs)    

if __name__ == '__main__':
    app.run(debug=True)
