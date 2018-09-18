import re
from flask import render_template, request, redirect, url_for
from app import app
from .sessions import *
from passlib.hash import sha256_crypt

@app.route('/')
def index():
    user = getCurrentSessionUser()
    name = None
    if user:
        name = user["name"]
    return render_template('index.html', name=name)

@app.route('/login', methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        user = request.form['user']
        if user.find("@") == -1:
            field = "username"
            result = re.fullmatch('[A-Za-z0-9]+', user)
            if not result:
                return render_template('login.html', error="Invalid characters in username")
        else:
            field = "email"
        password = request.form['password']
        result = re.fullmatch('[A-Za-z0-9\*_\-\.\!\?]+', password)
        if result:
            if app.mongo.db.users.count({field: user}):
                user = app.mongo.db.users.find_one({field: user})
                if sha256_crypt.verify(password, user["password"]):
                    createSession(user)
                    return redirect('/')
                else:
                    error = "No user found with those credentials"
            else:
                error = "No user found with those credentials"
        else:
            error = "Invalid characters in password"
    else:
        if "error" in request.args:
            error = request.args.get("error")
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    removeSession()
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    user = getCurrentSessionUser()
    name = None
    if user:
        name = user["name"]
    return render_template('404.html', name=name), 404
