from flask import Flask
from flask_pymongo import PyMongo

# Create flask application object
app = Flask(__name__)

# Set session secret key
app.secret_key = "b7Ux98ZEx95ix1bx8cS)xc6x8cx8excbP"

# Set up mongo database
mongo = PyMongo(app, uri="mongodb://localhost:27017/WebMLdb")

# Import routes
from .routes import *
