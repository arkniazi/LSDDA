# views.py
from flask_pymongo import PyMongo
from flask import render_template
from flask import request
import re
from app import app
from math import *
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT']='27017'
app.config['MONGO_DBNAME']="LSDDA"

mongo = PyMongo(app,config_prefix='MONGO')

@app.route('/table')
def index():
    most_listened = mongo.db.test.find().sort([{"valence",-1}]).limit(5)
    m_sound_quality =  mongo.db.test.find().sort([("sound_quailty",1)]).limit(5)
    lowest_tempi = mongo.db.test.find().sort([("tempo",1)]).limit(5)
    max_energy = mongo.db.test.find().sort([("energy",-1)]).limit(10)
    danceable = mongo.db.test.find({"years":"2000s"}).sort([("danceability",-1)]).limit(10)
    
    return render_template("table.html",most_listen = most_listened,
        min_sound_quality = m_sound_quality,low_temp = lowest_tempi,
        max_energy = max_energy, danceable = danceable)

@app.route('/',methods = ['POST','GET'])
def result():
    if request.method == 'POST':
        a = request.form['gul']
        b = "^"+a
        regx = re.compile(b, re.IGNORECASE)
        try:
            a = float(a)
        except ValueError:
            print "Not a float"
        name = mongo.db.test.find({"$or":[{"artist_name": regx},
        {"song_title":regx},{"years": regx},{"duration": { "$eq":a}},{"energy":  { "$eq":a}}
        ,{"liveness":  { "$eq":a}},{"tempo":  { "$eq":a}},{"speechiness": { "$eq":a}},
        {"Sound_quailty":  { "$eq":a}}
        ,{"instrumentalness":  { "$eq":a}},{"loudness":  { "$eq":a}},{"valence":  { "$eq":a}},
        {"danceability":  { "$eq":a}}]})

        return render_template("index.html",name = name)
    elif request.method == 'GET':
        songs = mongo.db.test.find()
        return render_template("index.html",songs=songs)

@app.route('/about')
def about():
    return render_template("about.html")