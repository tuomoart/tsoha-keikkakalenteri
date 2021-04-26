from os import getenv

from flask_sqlalchemy import SQLAlchemy
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
        sql = "SELECT password FROM users WHERE username=:username;"
        result = self.db.session.execute(sql, {"username":username})
        self.db.session.commit()
        password = result.fetchone()
        return password

    def getName(self, username):
        sql = "SELECT name FROM users WHERE username=:username;"
        result = self.db.session.execute(sql, {"username":username}).fetchone()
        self.db.session.commit()
        return result[0]


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
        sql += "CREATE TABLE IF NOT EXISTS participants (id SERIAL PRIMARY KEY, jobId INT, userId INT, status TEXT);"
        self.db.session.execute(sql)
        self.db.session.commit()
    
    def getJobs(self, user):
        if self.isAdmin(user):
            sql = "SELECT j.id, j.name, j.time, j.location, array(SELECT string_to_array(u.id || ',' || u.name || ',' || p.status, ',') FROM participants p JOIN users u ON u.id=p.userId WHERE p.jobId=j.id) AS participants FROM jobs j ORDER BY j.time, j.name;"
            result =  self.db.session.execute(sql).fetchall()
        else:
            sql = "SELECT j.id, j.name, j.time, j.location, array(SELECT string_to_array(u.id || ',' || u.name || ',' || p.status, ',') FROM participants p JOIN users u ON u.id=p.userId WHERE p.jobId=j.id) AS participants FROM jobs j WHERE :username IN (SELECT u.username FROM participants p JOIN users u ON u.id=p.userId WHERE p.jobId=j.id) ORDER BY j.time, j.name;"
            result =  self.db.session.execute(sql, {"username":user}).fetchall()
        self.db.session.commit()
        return result
    
    def getJob(self, id):
        sql = "SELECT j.id, j.name, j.time, j.location, array(SELECT string_to_array(u.id || ',' || u.name || ',' || p.status, ',') FROM participants p JOIN users u ON u.id=p.userId WHERE p.jobId=j.id) AS participants FROM jobs j WHERE j.id=:jobId;"
        result =  self.db.session.execute(sql, {"jobId":id}).fetchone()
        self.db.session.commit()
        return result

    def createJob(self, name, time, location, participants):
        sql="INSERT INTO jobs (name, time, location) VALUES (:name,:time,:location) RETURNING id;"
        id = self.db.session.execute(sql, {"name":name,"time":time,"location":location}).fetchone()[0]
        for userId in participants:
            sql="INSERT INTO participants (jobId, userId, status) VALUES (:jobId,:userId, 'Waiting')"
            self.db.session.execute(sql, {"jobId":id, "userId":userId})
        self.db.session.commit()
    
    def updateJob(self, id, name, time, location, participants):
        sql="UPDATE jobs SET name=:name, time=:time, location=:location WHERE id=:id;"
        self.db.session.execute(sql, {"id":id,"name":name,"time":time,"location":location})
        self.db.session.commit()

    def markAccepted(self, jobId, userId):
        sql="UPDATE participants SET status='Accepted' WHERE jobId=:jobId AND userId=:userId;"
        self.db.session.execute(sql, {"jobId":jobId, "userId":userId})
        self.db.session.commit()

    def deleteEvent(self, id):
        sql="DELETE FROM jobs WHERE id=:jobId;"
        self.db.session.execute(sql, {"jobId":id})
        sql="DELETE FROM participants WHERE jobId=:jobId;"
        self.db.session.execute(sql, {"jobId":id})
        self.db.session.commit()
    
    def deleteParticipant(self, jobId, userId):
        sql="DELETE FROM participants WHERE jobId=:jobId AND userId=:userId;"
        self.db.session.execute(sql, {"jobId":jobId, "userId":userId})
        self.db.session.commit()
