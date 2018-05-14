from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
        f"/api/v1.0/passengers"
        f"/api/v1.0/stations"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    # Query for the dates and temperature observations from the last year.
    results = session.query(Measurement).all()
    all_tobs = []
    for temp in results:
        tobs_dict = {}
        tobs_dict["Date"] = temp.date
        tobs_dict["Tobs"] = temp.tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/stations")
def normal():
    return hello_dict


# @app.route("/api/v1.0/tobs")
# def jsonified():
#     return jsonify(hello_dict)


if __name__ == "__main__":
    app.run(debug=True)
