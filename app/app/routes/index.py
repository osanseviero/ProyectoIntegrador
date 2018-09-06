from flask import render_template, request, redirect, session
from app import app, mongo
from pprint import pprint

@app.route('/')
def index():
    name = None
    if "name" in session:
        name = session["name"]
    return render_template('index.html', name=name)

@app.route('/login', methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        user = request.form['user']
        if user.find("@") == -1:
            field = "username"
        else:
            field = "email"
        if not mongo.db.users.count({field: user}):
            error = "No user found with those credentials"
        else:
            mongo.db.users.find_one({field: user})
            pprint(user)
            return redirect('/')
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop("name", None)
    session.pop("token", None)
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
