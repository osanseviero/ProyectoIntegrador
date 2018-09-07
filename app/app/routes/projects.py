from flask import render_template, request, redirect, url_for
from app import app, mongo
from .sessions import *

@app.route('/projects')
def get_projects():
    user = getCurrentSessionUser()
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
            # Guardar CSV aqui o por aqui
            new_id = autoIncrement("projectId")
            project_object = {
                "id": new_id,
                "name": request.form["projectName"],
                "filePath": "",
                "type": request.form["type"]
            }
            mongo.db.users.update_one({"_id": user["_id"]}, {"$push": {"projects": project_object}})
            return redirect('/projects/' + str(new_id))
        return render_template('createProject.html', name=user["name"])
    return redirect(url_for('login', error="You must login first"))

@app.route('/projects/<int:project_id>')
def get_project(project_id):
    user = getCurrentSessionUser()
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
    mongo.db.counters.update_one({"_id": field}, {"$inc" : {"value": 1}})
    counter = mongo.db.counters.find_one({"_id": field})
    return counter["value"]

# Ver que pedo, como guardar CSV
def saveCSV():
    pass
