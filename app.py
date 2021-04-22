from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv
from flask_sqlalchemy import SQLAlchemy

from PSGdatabase import PSGdatabase

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

db = PSGdatabase(app)

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
        jobs = db.getJobs(user)
        print(jobs)
        return render_template("main.html", isAdmin=isAdmin, jobs=jobs)
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
            return redirect("/main")
        else:
            error = "Invalid password"
            return render_template("index.html", error=error)
    

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["POST"])
def register():
    if db.isAdmin(session["username"]):
        name = request.form["name"]
        usergroup = request.form["usergroup"]
        username = request.form["username"]
        password = request.form["password"]
        passwordConf = request.form["passwordConf"]
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
    name = request.form["name"]
    time = request.form["time"]
    location = request.form["location"]
    participants = request.form.getlist("participants")
    db.createJob(name, time, location, participants)
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

@app.route("/add_new_user")
def addNewUser():
    return render_template("add_new_user.html")

@app.route("/add_new_job")
def addNewJob():
    participants = db.getUsers()
    return render_template("add_new_job.html", participants=participants)

@app.route("/purge")
def purge():
    db.purgeUsers()
    return redirect("/")
