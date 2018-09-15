from flask import render_template, request, redirect, url_for, jsonify
from app import app
from .sessions import getCurrentSessionUser, removeSession

# Encrypt password, validate fields
@app.route('/register', methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        if not app.mongo.db.users.count({"$or": [{"email": email}, {"username": username}]}):
            name = request.form['name']
            password = request.form['password']
            app.mongo.db.users.insert({"name": name, "password": password, "email": email, "username": username})
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

# Dunno if have to validate if update was successful
@app.route('/users/update', methods=["PUT"])
def update_user():
    user = getCurrentSessionUser()
    if user:
        name = request.form["name"] or user["name"]
        username = request.form["username"] or user["username"]
        email = request.form["email"] or user["email"]
        password = request.form["password"] or user["password"]
        app.mongo.db.users.update_one({"_id": user["_id"]}, {"name": name, "password": password, "email": email, "username": username})
        return redirect(url_for("profile"))
    return redirect(url_for("login", error="You must login first"))

# Dunno if have to validate if delete was successful
@app.route('/users/delete')
def delete_user():
    user = getCurrentSessionUser()
    if user:
        removeSession()
        app.mongo.db.users.delete_one({"_id": user["_id"]})
        return redirect('/')
    return redirect(url_for("login", error="You must login first"))
