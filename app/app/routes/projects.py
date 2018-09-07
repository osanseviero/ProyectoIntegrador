from flask import render_template, request, redirect
from app import app, mongo
from .sessions import *

@app.route('/projects')
def get_projects():
    pass

@app.route('/projects/create')
def create_project():
    pass

@app.route('/projects/<int:project_id>')
def get_project(project_id):
    pass

def autoIncrement(field):
    mongo.db.counters.update_one({"_id": field}, {"$inc" : {"value": 1}})
    counter = mongo.db.counters.find_one({"_id": field})
    return counter["value"]
