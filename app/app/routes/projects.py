from flask import render_template, request, redirect, url_for
from app import app
from .sessions import *
from werkzeug.utils import secure_filename
import os

@app.route('/projects')
def get_projects():
    user = getCurrentSessionUser(include_projects = 1)
    if user:
        error = None
        projects = []
        if "projects" in user:
            projects = user["projects"]
        if "error" in request.args:
            error = request.args.get("error")
        return render_template('projects.html', name=user["name"], projects=projects, error=error)
    return redirect(url_for('login', error="You must login first"))

@app.route('/projects/create', methods=["GET","POST"])
def create_project():
    user = getCurrentSessionUser()
    if user:
        if request.method == "POST":
            # Preguntar a arthur cuales son los nombres de los campos
            new_id = autoIncrement("projectId")
            if not saveCSV(user["username"], new_id):
                return render_template('create_project.html', name=user["name"], error="Server error storing csv, try again later please")
            project_object = {
                "id": new_id,
                "name": request.form["project_name"],
                "type": request.form["type"]
            }
            app.mongo.db.users.update_one({"_id": user["_id"]}, {"$push": {"projects": project_object}})
            return redirect('/projects/' + str(new_id))
        return render_template('create_project.html', name=user["name"], error=None)
    return redirect(url_for('login', error="You must login first"))

@app.route('/projects/<int:project_id>')
def get_project(project_id):
    user = getCurrentSessionUser(include_projects = 1)
    if user:
        if "projects" in user:
            selected = None
            for project in user["projects"]:
                if project["id"] == project_id:
                    selected = project
                    break
            return render_template('project.html', name=user["name"], project=selected)
        return redirect(url_for('get_projects', error="You have no projects created"))
    return redirect(url_for('login', error="You must login first"))

def autoIncrement(field):
    app.mongo.db.counters.update_one({"_id": field}, {"$inc" : {"value": 1}})
    counter = app.mongo.db.counters.find_one({"_id": field})
    return counter["value"]

def saveCSV(username, projectId):
    if 'csv' not in request.files:
        return False
    file = request.files['csv']
    filename_splited = file.filename.rsplit('.', 1)
    if len(filename_splited) >= 2 and filename_splited[1].lower() == "csv":
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], username, "project-" + str(projectId) + ".csv"))
        return True
    return False
