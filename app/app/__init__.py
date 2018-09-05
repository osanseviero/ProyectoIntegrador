from flask import Flask
from flask_pymongo import PyMongo

# Create flask application object
app = Flask(__name__)

# Set session secret key
app.secret_key = "insert super secret key here"

# Set up mongo database
mongo = PyMongo(app, uri="mongodb://localhost:27017/WebMLdb")

# Import routes
from .routes import *
