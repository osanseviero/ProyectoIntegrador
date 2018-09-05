from flask import render_template
from app import app
from ..db import mongo

@app.route('/')
def index():
    # return render_template('index.html')
    print(mongo)
    return render_template('index.html')
