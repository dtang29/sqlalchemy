from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from sqlalchemy import and_


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"
        
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    # Query for the dates and temperature observations from the last year.
    
    #Find what last year is
    year =  int(dt.date.today().strftime("%Y")) - 1
    
    #Filter query for last year data only
    results = session.query(Measurement).\
              filter(func.strftime("%Y", Measurement.date) == str(year)).all()

    all_tobs = []
    for temp in results:
        tobs_dict = {}
        tobs_dict["Date"] = temp.date
        tobs_dict["Tobs"] = temp.tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/stations")
def stations():

    #Return a json list of stations from the dataset.
    stations = session.query(Station).all()
    all_stations = []
    for station in stations:
        stations_dict = {}
        stations_dict["Station"] = station.station
        stations_dict["Name"] = station.name
        all_stations.append(stations_dict)
    
    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def tobs():

    #Return a json list of Temperature Observations (tobs) for the previous year
    
    #Find what last year is
    year =  int(dt.date.today().strftime("%Y")) - 1
    
    #Filter query for last year data only
    results = session.query(Measurement).\
              filter(func.strftime("%Y", Measurement.date) == str(year)).all()

    all_tobs = []
    for temp in results:
        tobs_dict = {}
        tobs_dict["Tobs"] = temp.tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    #Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

    sel = [func.avg(Measurement.tobs),
        func.max(Measurement.tobs),
        func.min(Measurement.tobs)]


    stats = session.query(*sel).\
        filter(Measurement.date >= start, Measurement.date <= end).all()

    all_stats = []
    stats_dict = {}
    stats_dict["TAVG"] = stats[0][0]
    stats_dict["TMAX"] = stats[0][1]
    stats_dict["TMIN"] = stats[0][2]
    all_stats.append(stats_dict)

    return jsonify(all_stats)

@app.route("/api/v1.0/<start>")
def start(start):
    #Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

    sel = [func.avg(Measurement.tobs),
        func.max(Measurement.tobs),
        func.min(Measurement.tobs)]


    stats = session.query(*sel).\
        filter(Measurement.date >= start).all()

    all_stats = []
    stats_dict = {}
    stats_dict["TAVG"] = stats[0][0]
    stats_dict["TMAX"] = stats[0][1]
    stats_dict["TMIN"] = stats[0][2]
    all_stats.append(stats_dict)

    return jsonify(all_stats)


if __name__ == "__main__":
    app.run(debug=True)
