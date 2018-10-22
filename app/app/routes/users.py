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

@app.route('/users/update/info', methods=["POST"])
def update_user_info():
    user = getCurrentSessionUser()
    if user:
        updates = {}
        error = None
        email = request.form["email"]
        name = request.form["name"]
        username = request.form["username"]
        if email != user["email"]:
            if app.mongo.db.users.count({"email": email}):
                error = "Email already in use"
            else:
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
                if app.mongo.db.users.count({"username": username}):
                    error = "Username already in use"
                else:
                    updates["username"] = username
                    os.rename(os.path.join(app.config["UPLOAD_FOLDER"], user["username"]), os.path.join(app.config["UPLOAD_FOLDER"], username))
            else:
                error = "Invalid characters in username"
        if not error and updates != {}:
            app.mongo.db.users.update_one({"_id": user["_id"]}, {"$set": updates})
        return redirect(url_for("profile", error=error))
    return redirect(url_for("login", error="You must login first"))

@app.route('/users/update/password', methods=["POST"])
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
                    user = app.mongo.db.users.find_one({"_id": user["_id"]}, {"password" : 1})
                    if not sha256_crypt.verify(current_password, user["password"]):
                        error = "Incorrect password"
                else:
                    error = "Passwords don't match"
            else:
                error = "Invalid characters in new password"
        else:
            error = "Invalid characters in current password"
        if not error:
            password = sha256_crypt.encrypt(password)
            app.mongo.db.users.update_one({"_id": user["_id"]}, {"$set": {"password": password}})
        return redirect(url_for("profile", error=error))
    return redirect(url_for("login", error="You must login first"))

@app.route('/users/delete', methods=["POST"])
def delete_user():
    user = getCurrentSessionUser()
    if user:
        from shutil import rmtree
        app.mongo.db.users.delete_one({"_id": user["_id"]})
        user_dir_path = os.path.join(app.config["UPLOAD_FOLDER"], user["username"])
        rmtree(user_dir_path)
        return redirect(url_for("logout"))
    return redirect(url_for("login", error="You must login first"))
