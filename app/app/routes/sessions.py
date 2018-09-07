from flask import session
from app import mongo
from uuid import uuid4

def getCurrentSessionUser():
    user = None
    if "token" in session:
        current_session = mongo.db.sessions.find_one({"token": session["token"]})
        if current_session:
            user = mongo.db.users.find_one({"_id": current_session["user_id"]}, {"password": 0})
    return user

def removeSession():
    if "token" in session:
        mongo.db.sessions.remove({"token": session["token"]})
        session.pop("token", None)

def createSession(user):
    token = str(uuid4())
    mongo.db.sessions.insert_one({"user_id": user["_id"], "token": token})
    session["token"] = token
