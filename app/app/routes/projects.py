import os, re
from flask import render_template, request, redirect, url_for
from app import app
from .sessions import getCurrentSessionUser
current_project = {"id":None}

@app.route('/projects')
def get_projects():
    user = getCurrentSessionUser(include_projects = True)
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
        error = None
        if request.method == "POST":
            project_name = request.form["project_name"]
            result = re.fullmatch('[A-Za-z0-9]+', project_name)
            if result:
                new_id = autoIncrement(user["_id"], "projects")
                if saveCSV(user["username"], new_id):
                    project_object = {"id": new_id, "name": project_name, "type": request.form["type"]}
                    app.mongo.db.users.update_one({"_id": user["_id"]}, {"$push": {"projects": project_object}})
                    return redirect(url_for('get_project', project_id=new_id))
                app.mongo.db.counters.update_one({"user_id": user["_id"], "collection": "projects"}, {"$inc": {"value": -1}})
                error = "Server error storing csv, try again later please"
            else:
                error = "Invalid characters in project name"
        return render_template('create_project.html', name=user["name"], error=error)
    return redirect(url_for('login', error="You must login first"))

def autoIncrement(id, collection):
    app.mongo.db.counters.update_one({"user_id": id, "collection": collection}, {"$inc" : {"value": 1}}, {"upsert": True})
    counter = app.mongo.db.counters.find_one({"user_id": id, "collection": collection})
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

@app.route('/projects/<int:project_id>')
def get_project(project_id):
    user = getCurrentSessionUser(include_projects = True)
    if user:
        if "projects" in user:
            selected = None
            for project in user["projects"]:
                if project["id"] == project_id:
                    selected = project
                    break
            if selected:
                error = None
                if "error" in request.args:
                    error = request.args.get("error")
                current_project["id"] = selected["id"]
                return render_template('project.html', name=user["name"], project=selected, error=error)
            return redirect(url_for('get_projects', error="There's no project with id = " + str(project_id)))
        return redirect(url_for('get_projects', error="You have no projects created"))
    return redirect(url_for('login', error="You must login first"))

@app.route('/projects/update', methods=["POST"])
def update_project():
    user = getCurrentSessionUser()
    if user:
        project_id = current_project["id"]
        error = None
        type = request.form["type"]
        project_name = request.form["project_name"]
        result = re.fullmatch('[A-Za-z0-9]+', project_name)
        if result:
            app.mongo.db.users.update_one({"_id": user["_id"], "projects.id": project_id}, {"$set": {"projects.$.name": project_name, "projects.$.type": type}})
        else:
            error = "Invalid characters in project name"
        return redirect(url_for("get_project", project_id=project_id, error=error))
    return redirect(url_for('login', error="You must login first"))

@app.route('/projects/delete', methods=["POST"])
def delete_project():
    user = getCurrentSessionUser()
    if user:
        project_id = current_project["id"]
        app.mongo.db.users.update_one({"_id": user["_id"]}, {"$pull": {"projects": {"id": project_id}}})
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"], user["username"], "project-" + str(project_id) + ".csv"))
        return redirect(url_for('get_projects'))
    return redirect(url_for('login', error="You must login first"))

@app.route('/projects/train', methods=["POST"])
def train_project():
    return "Working"

@app.route('/projects/predict', methods=["POST"])
def predict():
    return "Working"
