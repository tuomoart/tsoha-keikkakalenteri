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
    try:
        isAdmin = db.isAdmin(session["username"])
    except:
        isAdmin = False
    return render_template("index.html", isAdmin=isAdmin)

@app.route("/main", methods=["POST"])
def result():
    return render_template("main.html", username=request.form["username"])

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
            return redirect("/")
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

@app.route("/add_new_user")
def addNewUser():
    return render_template("add_new_user.html")

@app.route("/purge")
def purge():
    db.purgeUsers()
    return redirect("/")
