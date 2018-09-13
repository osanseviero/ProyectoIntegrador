from flask import render_template, request, redirect
from app import app, mongo
from .sessions import *

@app.route('/')
def index():
    user = getCurrentSessionUser()
    name = None
    if user:
        name = user["name"]
    return render_template('index.html', name=name)

# Validate fields
@app.route('/login', methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        user = request.form['user']
        if user.find("@") == -1:
            field = "username"
        else:
            field = "email"
        if mongo.db.users.count({field: user}):
            user = mongo.db.users.find_one({field: user})
            createSession(user)
            return redirect('/')
        else:
            error = "No user found with those credentials"
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


# Status 405 for methods not allowed
