from flask import render_template, request, redirect, url_for
from app import app, mongo
from .sessions import getCurrentSessionUser

# Encrypt password, validate fields
@app.route('/register', methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        if not mongo.db.users.count({"$or": [{"email": email}, {"username": username}]}):
            name = request.form['name']
            password = request.form['password']
            mongo.db.users.insert({"name": name, "password": password, "email": email, "username": username})
            return redirect(url_for('login'))
        else:
            error = "Username or email already in use"
    return render_template("register.html", error=error)

@app.route('/users/profile')
def profile():
    user = getCurrentSessionUser()
    if user:
        return render_template('profile.html', user=user)
    return redirect(url_for('login', error="You must login first"))
