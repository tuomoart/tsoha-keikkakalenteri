from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import generate_password_hash

class PSGdatabase:
    def __init__(self, app):
        self.app = app
        self.db = SQLAlchemy(app)

        self.initializeUsers()
        self.initializeJobs()
    
    #Users:

    def initializeUsers(self):
        sql = "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT, username TEXT, password TEXT, usergroup TEXT, email TEXT, phone TEXT);"
        self.db.session.execute(sql)
        self.db.session.commit()

        admin = getenv("ADMIN_USERNAME")
        user = self.getPassword(admin)
        if user == None:
            hash_value = generate_password_hash(getenv("ADMIN_PASSWORD"))
            self.createUser(admin, admin, hash_value, "admin")

    def getUsers(self):
        result =  self.db.session.execute("SELECT id, name FROM users;").fetchall()
        self.db.session.commit()
        return result
    
    def getPassword(self, username):
        sql = "SELECT password FROM users WHERE username=:username"
        result = self.db.session.execute(sql, {"username":username})
        self.db.session.commit()
        password = result.fetchone()
        return password

    def createUser(self, name, username, passHash, usergroup):
        sql = "INSERT INTO users (name,username,password,usergroup) VALUES (:name,:username,:password,:usergroup)"
        self.db.session.execute(sql, {"name":name,"username":username,"password":passHash,"usergroup":usergroup})
        self.db.session.commit()
        return True
    
    def isAdmin(self, username):
        sql = "SELECT usergroup FROM users WHERE username=:username"
        result = self.db.session.execute(sql, {"username":username})
        self.db.session.commit()
        usergroup = result.fetchone()[0]
        return usergroup == "admin"
    
    def usernameExists(self, username):
        sql = "SELECT * FROM users WHERE username=:username"
        result = self.db.session.execute(sql, {"username":username})
        self.db.session.commit()
        found = result.fetchall()
        return len(found) > 0

    def purgeUsers(self):
        self.db.session.execute("DELETE FROM users")
        self.db.session.commit()

    def getIdByUsername(self, username):
        sql = "SELECT id FROM users WHERE username=:username;"
        result = self.db.session.execute(sql, {"username": username}).fetchone()[0]
        return result
    
    # Jobs:

    def initializeJobs(self):
        sql = "CREATE TABLE IF NOT EXISTS jobs (id SERIAL PRIMARY KEY, name TEXT, time TEXT, location TEXT);"
        sql += "CREATE TABLE IF NOT EXISTS participants (id SERIAL PRIMARY KEY, jobId INT, userId INT);"
        self.db.session.execute(sql)
        self.db.session.commit()
    
    def getJobs(self, user):
        if self.isAdmin(user):
            sql = "SELECT j.id, j.name, j.time, j.location, array(SELECT u.name FROM participants p JOIN users u ON u.id=p.userId WHERE p.jobId=j.id) AS participants FROM jobs j ORDER BY j.time, j.name;"
            result =  self.db.session.execute(sql).fetchall()
        else:
            id = self.getIdByUsername(user)
            sql = "SELECT j.id, j.name, j.time, j.location, array(SELECT u.name FROM participants p JOIN users u ON u.id=p.userId WHERE p.jobId=j.id) AS participants FROM jobs j WHERE :username IN (SELECT u.name FROM participants p JOIN users u ON u.id=p.userId WHERE p.jobId=j.id) ORDER BY j.time, j.name;"
            result =  self.db.session.execute(sql, {"username":user}).fetchall()
        self.db.session.commit()
        return result

    def createJob(self, name, time, location, participants):
        sql="INSERT INTO jobs (name, time, location) VALUES (:name,:time,:location) RETURNING id;"
        id = self.db.session.execute(sql, {"name":name,"time":time,"location":location}).fetchone()[0]
        for userId in participants:
            sql="INSERT INTO participants (jobId, userId) VALUES (:jobId,:userId)"
            self.db.session.execute(sql, {"jobId":id, "userId":userId})
        self.db.session.commit()