import os, re
from flask import render_template, request, redirect, url_for, jsonify
from app import app
from .sessions import getCurrentSessionUser, removeSession
from passlib.hash import sha256_crypt

@app.route('/register', methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        result = re.fullmatch('[A-Za-z0-9]+', username)
        if result:
            if not app.mongo.db.users.count({"$or": [{"email": email}, {"username": username}]}):
                name = request.form['name']
                result = re.fullmatch('[A-Za-z]+', name)
                if result:
                    password = request.form['password']
                    result = re.fullmatch('[A-Za-z0-9\*_\-\.\!\?]+', password)
                    if result:
                        if password == request.form["repassword"]:
                            password = sha256_crypt.encrypt(password)
                            app.mongo.db.users.insert({"name": name, "password": password, "email": email, "username": username})
                            os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], username))
                            return redirect(url_for('login'))
                        else:
                            error = "Passwords don't match"
                    else:
                        error = "Invalid characters in password"
                else:
                    error = "Invalid characters in name"
            else:
                error = "Username or email already in use"
        else:
            error = "Invalid characters in username"
    return render_template("register.html", error=error)

@app.route('/users/profile')
def profile():
    user = getCurrentSessionUser()
    if user:
        error = None
        if "error" in request.args:
            error = request.args.get("error")
        return render_template('profile.html', user=user, error=error)
    return redirect(url_for('login', error="You must login first"))

@app.route('/users/update/info', methods=["PUT"])
def update_user_info():
    user = getCurrentSessionUser()
    if user:
        updates = {}
        error = None
        email = request.form["email"]
        name = request.form["name"]
        username = request.form["username"]
        if email != user["email"]:
            updates["email"] = email
        if name != user["name"]:
            result = re.fullmatch('[A-Za-z]+', name)
            if result:
                updates["name"] = name
            else:
                error = "Invalid characters in name"
        if username != user["username"]:
            result = re.fullmatch('[A-Za-z0-9]+', username)
            if result:
                updates["username"] = username
                os.rename(os.path.join(app.config["UPLOAD_FOLDER"], user["username"]), os.path.join(app.config["UPLOAD_FOLDER"], username))
            else:
                error = "Invalid characters in username"
        if not error:
            app.mongo.db.users.update_one({"_id": user["_id"]}, updates)
        return redirect(url_for("profile", error=error))
    return redirect(url_for("login", error="You must login first"))

@app.route('/users/update/password', methods=["PUT"])
def update_user_password():
    user = getCurrentSessionUser()
    if user:
        error = None
        current_password = request.form["current_password"]
        password = request.form["password"]
        result = re.fullmatch('[A-Za-z0-9\*_\-\.\!\?]+', current_password)
        if result:
            result = re.fullmatch('[A-Za-z0-9\*_\-\.\!\?]+', password)
            if result:
                if password == request.form["repassword"]:
                    hash = app.mongo.db.users.find_one({"_id": user["_id"]}, {"password" : 1})["password"]
                    if not sha256_crypt.verify(current_password, hash):
                        error = "Incorrect password"
                else:
                    error = "Passwords don't match"
            else:
                error = "Invalid characters in new password"
        else:
            error = "Invalid characters in current password"
        if not error:
            password = sha256_crypt.encrypt(password)
            app.mongo.db.users.update_one({"_id": user["_id"]}, {"password": password})
        return redirect(url_for("profile", error=error))
    return redirect(url_for("login", error="You must login first"))

@app.route('/users/delete', methods=["DELETE"])
def delete_user():
    user = getCurrentSessionUser()
    if user:
        removeSession()
        app.mongo.db.users.delete_one({"_id": user["_id"]})
        path = os.path.join(app.config["UPLOAD_FOLDER"], user["username"])
        for file in os.listdir(path):
            os.remove(os.path.join(app.config["UPLOAD_FOLDER"], user["username"], file))
        os.rmdir(path)
        return redirect('/')
    return redirect(url_for("login", error="You must login first"))
