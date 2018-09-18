from flask import session
from app import app
from uuid import uuid4

def getCurrentSessionUser(include_projects = False):
    user = None
    if "token" in session:
        current_session = app.mongo.db.sessions.find_one({"token": session["token"]})
        if current_session:
            projection = {"password": 0}
            if not include_projects:
                projection["projects"] = 0
            user = app.mongo.db.users.find_one({"_id": current_session["user_id"]}, projection)
    return user

def removeSession():
    if "token" in session:
        app.mongo.db.sessions.remove({"token": session["token"]})
        session.pop("token", None)

def createSession(user):
    token = str(uuid4())
    app.mongo.db.sessions.insert_one({"user_id": user["_id"], "token": token})
    session["token"] = token
