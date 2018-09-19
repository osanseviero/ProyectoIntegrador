from flask import Flask
from flask_pymongo import PyMongo
# from flask_mail import Mail

# Create flask application object
app = Flask(__name__)

# Set session secret key
app.secret_key = "b7Ux98ZEx95ix1bx8cS)xc6x8cx8excbP"

# Set up mongo database
app.mongo = PyMongo(app, uri="mongodb://localhost:27017/WebMLdb")

# Set up file upload configuration
# Set uploads folder
app.config['UPLOAD_FOLDER'] = '/data/uploads/'
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 megabytes, change this to max upload size allowed, if needed

# Import routes
from .routes import *
