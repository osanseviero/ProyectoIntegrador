from flask import render_template, redirect, url_for, session
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return "WORKING"

@app.route('/logout')
def logout():
    #session.pop("", None)
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
