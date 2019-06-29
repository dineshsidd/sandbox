import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
# db = SQLAlchemy(app)

# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(db.engine, reflect=True)

# # Save references to each table
# Samples_Metadata = Base.classes.sample_metadata
# Samples = Base.classes.samples


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route('/<page>')
def html_lookup(page):
    try:
        return render_template('{}'.format(page))
    except TemplateNotFound:
        abort(404)

@app.route("/map")
def get_map_data():
    global_temp_country = pd.read_csv('GlobalLandTemperaturesByCountry.csv')
    global_temp_country_clear = global_temp_country[~global_temp_country['Country'].isin(
    ['Denmark', 'Antarctica', 'France', 'Europe', 'Netherlands',
        'United Kingdom', 'Africa', 'South America'])]
    global_temp_country_clear = global_temp_country_clear.replace(
    ['Denmark (Europe)', 'France (Europe)', 'Netherlands (Europe)', 'United Kingdom (Europe)'],
    ['Denmark', 'France', 'Netherlands', 'United Kingdom'])

    countries = np.unique(global_temp_country_clear['Country'])
    mean_temp = []
    for country in countries:
        mean_temp.append({"country": country, "mean_temp" : 
        global_temp_country_clear[global_temp_country_clear['Country'] == 
        country]['AverageTemperature'].mean()})
    return jsonify(mean_temp)

@app.route("/path")
def get_os_path():
    return os.path.join(app.instance_path) 

if __name__ == "__main__":
    app.run()
