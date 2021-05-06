from flask import Flask
from flask import redirect, render_template, request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv
from flask_sqlalchemy import SQLAlchemy
import secrets

from PSGdatabase import PSGdatabase

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

db = PSGdatabase(app)

def getIds(list):
    res = []
    for i in list:
        res.append(i[0])
    return res

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/main")
def mainPage():
    try:
        isAdmin = db.isAdmin(session["username"])
    except:
        isAdmin = False
    
    try:
        user = session["username"]
        name = db.getName(user)
        jobs = db.getJobs(user)
        return render_template("main.html", name=name, isAdmin=isAdmin, jobs=jobs)
    except Exception as e:
        print(e)
        return redirect("/")
    

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = db.getPassword(username)
    if user == None:
        error = "Invalid username"
        return render_template("index.html", error=error)
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/main")
        else:
            error = "Invalid password"
            return render_template("index.html", error=error)
    

@app.route("/logout")
def logout():
    del session["username"]
    del session["csrf_token"]
    return redirect("/")

@app.route("/register", methods=["POST"])
def register():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    
    if db.isAdmin(session["username"]):
        name = request.form["name"]
        usergroup = request.form["usergroup"]
        username = request.form["username"]
        password = request.form["password"]
        passwordConf = request.form["passwordConf"]
        if name=="" or username=="" or password=="":
            error = "Name, username and password must be given!"
            return render_template("add_new_user.html", error=error)
        if db.usernameExists(username):
            error = "Username already exists!"
            return render_template("add_new_user.html", error=error)
        if password != passwordConf:
            error = "Passwords didn't match!"
            return render_template("add_new_user.html", error=error)
        hash_value = generate_password_hash(password)
        db.createUser(name, username, hash_value, usergroup)
        return redirect("/")
    else:
        error = "You are not an admin!"
        return render_template("add_new_user.html", error=error)

@app.route("/createJob", methods=["POST"])
def createJob():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    name = request.form["name"]
    time = request.form["time"]
    location = request.form["location"]
    participants = request.form.getlist("participants")
    db.createJob(name, time, location, participants)
    return redirect("/main")

@app.route("/updateJob", methods=["POST"])
def updateJob():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    id = request.args['event']
    name = request.form["name"]
    time = request.form["time"]
    location = request.form["location"]
    participants = request.form.getlist("participants")
    db.updateJob(id, name, time, location, participants)
    return redirect("/main")

@app.route("/accept")
def accept():
    jobId = request.args['event']
    userId = request.args['participant']
    db.markAccepted(jobId, userId)
    return redirect("/main")

@app.route("/deleteParticipant")
def deleteParticipant():
    jobId = request.args['event']
    userId = request.args['participant']
    db.deleteParticipant(jobId, userId)
    return redirect("/main")

@app.route("/deleteEvent")
def deleteEvent():
    db.deleteEvent(request.args['event'])
    return redirect("/main")

@app.route("/add_new_user")
def addNewUser():
    return render_template("add_new_user.html")

@app.route("/jobEditor")
def addNewJob():
    participants = db.getUsersInGroup("normal")
    locations = db.getLocations()
    try:
        jobId=request.args['event']
        jobData=db.getJob(jobId)
        participantIds = getIds(jobData[4])
        print(participantIds)
        return render_template("edit_job.html", locations=locations, participants=participants, job=jobData, participantIds=participantIds)
    except:
        return render_template("add_new_job.html", locations=locations, participants=participants)
    
    

@app.route("/purge")
def purge():
    db.purgeUsers()
    return redirect("/")
