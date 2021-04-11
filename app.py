from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
#app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///tuomoart?host=/home/tuomoart/pgsql/sock"
db = SQLAlchemy(app)


@app.route("/")
def index():
    result = db.session.execute("SELECT * FROM users")
    print(result.fetchall())
    return render_template("index.html")

@app.route("/main", methods=["POST"])
def result():
    return render_template("main.html", username=request.form["username"])

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user == None:
        error = "Invalid login credentials"
        return render_template("index.html", error=error)
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = username
            return redirect("/")
        else:
            error = "Invalid login credentials"
            return render_template("index.html", error=error)
    

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    usergroup = request.form["usergroup"]
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (name,username,password,usergroup) VALUES (:name,:username,:password,:usergroup)"
    db.session.execute(sql, {"name":name,"username":username,"password":hash_value,"usergroup":usergroup})
    db.session.commit()
    return redirect("/")

@app.route("/add_new_user")
def addNewUser():
    return render_template("add_new_user.html")

@app.route("/purge")
def purge():
    db.session.execute("DELETE FROM users")
    db.session.commit()
    return redirect("/")
