import os, re, json
from flask import render_template, request, redirect, url_for, jsonify
from app import app
from .sessions import getCurrentSessionUser, getOneUser
from werkzeug.utils import secure_filename
from ..ai.tuner import HPTuner
from ..ai.hparams import HParams
from ..ai.trainer import predict_tf_model

current = {"project": None}

@app.route('/projects')
def get_projects():
    user = getCurrentSessionUser(include_projects = True)
    if user:
        error = None
        projects = []
        current["project"] = None
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
            result = re.fullmatch('[A-Za-z0-9_ ]+', project_name)
            if result:
                if not app.mongo.db.users.count({"_id": user["_id"], "projects": {"$elemMatch": {"name": project_name}}}):
                    label = request.form["label"]
                    result = re.fullmatch('[A-Za-z0-9_]+', label)
                    if result:
                        features = request.form["features"]
                        result = re.fullmatch('[A-Za-z0-9_:, ]+', features)
                        if result:
                            features = [feature.split(":") for feature in features.replace(" ","").split(",")]
                            new_id = autoIncrement(user["_id"], "projects")
                            filename = saveCSV(user["username"], project_name)
                            if filename:
                                trials_number = 5
                                project_object = {"id": new_id, "name": project_name, "type": request.form["type"], "filename": filename, "label": label, "features": features, "selected_model": -1}
                                trials_list = train_project(user['username'], project_object, trials_number)
                                project_object["trials"] = trials_list
                                app.mongo.db.users.update_one({"_id": user["_id"]}, {"$push": {"projects": project_object}})
                                return redirect(url_for('get_project', project_id=new_id))
                            else:
                                app.mongo.db.counters.update_one({"user_id": user["_id"], "collection": "projects"}, {"$inc": {"value": -1}})
                                error = "Server error storing csv, try again later please"
                        else:
                            error = "Invalid characters in features field"
                    else:
                        error = "Invalid characters in label field"
                else:
                    error = "You have other project with the same name"
            else:
                error = "Invalid characters in project name"
        return render_template('create_project.html', name=user["name"], error=error)
    return redirect(url_for('login', error="You must login first"))

def autoIncrement(id, collection):
    app.mongo.db.counters.update_one({"user_id": id, "collection": collection}, {"$inc" : {"value": 1}}, upsert=True)
    counter = app.mongo.db.counters.find_one({"user_id": id, "collection": collection})
    return int(counter["value"])

def saveCSV(username, projectName):
    if 'csv' not in request.files:
        return None
    file = request.files['csv']
    filename_splited = file.filename.rsplit('.', 1)
    if len(filename_splited) >= 2 and filename_splited[1].lower() == "csv":
        filename = secure_filename(file.filename)
        project_path = os.path.join(app.config['UPLOAD_FOLDER'], username, projectName)
        os.mkdir(project_path)
        file.save(os.path.join(project_path, filename))
        return filename
    return None

def train_project(username, project, trials_number):
    space = {
        "batch_size": [10, 50, 100, 200],
        "train_steps": [100, 1000, 2000, 3000],
        "model_type": ['NN', 'Linear'],
    }
    tuner = HPTuner(os.path.join(app.config['UPLOAD_FOLDER'], username, project['name'], 'models'),
                    project['type'] == 'classification',
                    os.path.join(app.config['UPLOAD_FOLDER'], username, project['name'], project['filename']),
                    project['label'],
                    project['features'],
                    space)
    trials = []
    for t in range(trials_number):
        current_trial = tuner.generate_trial()
        trials.append({
            "id": current_trial["trial"],
            "hyperparameters": current_trial["hparams"],
            "metrics": {}
        })
        for key, item in current_trial["metrics"][0].items():
            trials[t]["metrics"][key] = float(item)
    return trials

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
                current["project"] = selected
                features_string = ",".join([":".join(sublist) for sublist in selected["features"]])
                return render_template('project.html', name=user["name"], project=selected, features_string=features_string, error=error)
            return redirect(url_for('get_projects', error="There's no project with id = " + str(project_id)))
        return redirect(url_for('get_projects', error="You have no projects created"))
    return redirect(url_for('login', error="You must login first"))

@app.route('/projects/update', methods=["POST"])
def update_project():
    user = getCurrentSessionUser()
    if user:
        updates = {}
        error = None
        type = request.form["type"]
        project_name = request.form["project_name"]
        label = request.form["label"]
        features = request.form["features"]
        features = [feature.split(":") for feature in features.replace(" ","").split(",")]
        if type != current["project"]["type"]:
            updates["projects.$.type"] = type
        if project_name != current["project"]["name"]:
            result = re.fullmatch('[A-Za-z0-9_ ]+', project_name)
            if result:
                if not app.mongo.db.users.count({"_id": user["_id"], "projects": {"$elemMatch": {"name": project_name}}}):
                    updates["projects.$.name"] = project_name
                    os.rename(os.path.join(app.config["UPLOAD_FOLDER"], user["username"], current["project"]["name"]), os.path.join(app.config["UPLOAD_FOLDER"], user["username"], project_name))
                else:
                    error = "You have other project with the same name"
            else:
                error = "Invalid characters in project name"
        if label != current["project"]["label"]:
            result = re.fullmatch('[A-Za-z0-9_]+', label)
            if result:
                updates["projects.$.label"] = label
            else:
                error = "Invalid characters in label"
        if features != current["project"]["features"]:
            result = re.fullmatch('[A-Za-z0-9_:, ]+', features)
            if result:
                updates["projects.$.features"] = features
            else:
                error = "Invalid characters in features"
        if not error and updates != {}:
            app.mongo.db.users.update_one({"_id": user["_id"], "projects.id": current["project"]["id"]}, {"$set": updates})
        return redirect(url_for("get_project", project_id=current["project"]["id"], error=error))
    return redirect(url_for('login', error="You must login first"))


@app.route('/projects/delete', methods=["POST"])
def delete_project():
    user = getCurrentSessionUser()
    if user:
        from shutil import rmtree
        project_id = current["project"]["id"]
        project_name = current["project"]["name"]
        app.mongo.db.users.update_one({"_id": user["_id"]}, {"$pull": {"projects": {"id": project_id}}})
        project_path = os.path.join(app.config["UPLOAD_FOLDER"], user["username"], project_name)
        rmtree(project_path)
        return redirect(url_for('get_projects'))
    return redirect(url_for('login', error="You must login first"))

@app.route('/projects/select_trial', methods=["POST"])
def select_trial():
    user = getCurrentSessionUser()
    if user:
        tid = int(request.form["id"])
        app.mongo.db.users.update_one({"_id": user["_id"], "projects.id": current["project"]["id"]}, {"$set": {"projects.$.selected_model": tid}})
        current["project"]["selected_model"] = tid
        return redirect(url_for('get_project', project_id=current['project']['id']))
    return redirect(url_for('login', error="You must login first"))

@app.route('/projects/predict', methods=["GET","POST"])
def predict():
    if request.method == "POST":
        data = json.loads(request.data.decode("utf-8"))
        if "username" in data and "p_id" in data and "data" in data:
            user = getOneUser(data["username"], data["p_id"])
            project = user["projects"][0]
            if project["selected_model"] == -1:
                return jsonify({"error":"select model first"})
            features = project["features"]
            label = project["label"]
            classification = project["type"] == "classification"
            csv_dir = os.path.join(app.config["UPLOAD_FOLDER"], user["username"], project["name"], project["filename"])
            model_dir = os.path.join(app.config["UPLOAD_FOLDER"], user["username"], project["name"], "models", str(project["selected_model"]))
            for t in project["trials"]:
                if t["id"] == project["selected_model"]:
                    params = t["hyperparameters"]
            hparams = HParams(batch_size=params["batch_size"], train_steps=params["train_steps"], model_type=params["model_type"])
            predict_data = data["data"]
            predictions = predict_tf_model(model_dir, hparams, classification, csv_dir, label, features, predict_data)
            predictions = list(predictions)
            result = []
            for p in predictions:
                if classification:
                    result.append({"class": p["classes"][0].decode("utf-8"), "probability": float(max(p["probabilities"]))})
                else:
                    result.append(p["predictions"][0])
            return jsonify(result)
        else:
            return jsonify({"error":"missing parameters"})
    else:
        user = getCurrentSessionUser()
        if user:
            if current["project"]["selected_model"] == -1:
                return redirect(url_for("get_project", project_id=current["project"]["id"], error="Select model first"))
            for t in current["project"]["trials"]:
                if t["id"] == current["project"]["selected_model"]:
                    trial = t
            return render_template("predict.html", name=user['username'], id=current["project"]["id"], trial=trial, features=current["project"]["features"], label=current["project"]["label"], p_type=current["project"]["type"])
        return redirect(url_for('login', error="You must login first"))
