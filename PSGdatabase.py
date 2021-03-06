from os import getenv

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


class PSGdatabase:
    def __init__(self, app):
        self.app = app
        self.db = SQLAlchemy(app)

        self.initializeUsers()
        self.initializeJobs()
        self.initializeLocations()
    
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
    
    def getUsersInGroup(self, group):
        result =  self.db.session.execute("SELECT id, name FROM users WHERE usergroup=:group;", {"group":group}).fetchall()
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

    def getIdByUsername(self, username):
        sql = "SELECT id FROM users WHERE username=:username;"
        result = self.db.session.execute(sql, {"username": username}).fetchone()[0]
        return result
    
    # Jobs:

    def initializeJobs(self):
        sql = "CREATE TABLE IF NOT EXISTS jobs (id SERIAL PRIMARY KEY, name TEXT, time TEXT, location INT);"
        sql += "CREATE TABLE IF NOT EXISTS participants (id SERIAL PRIMARY KEY, jobId INT, userId INT, status TEXT);"
        self.db.session.execute(sql)
        self.db.session.commit()
    
    def getJobs(self, user):
        if self.isAdmin(user):
            sql = "SELECT j.id, j.name, j.time, (SELECT name FROM locations l WHERE l.id = j.location), array(SELECT string_to_array(u.id || ',' || u.name || ',' || p.status, ',') FROM participants p JOIN users u ON u.id=p.userId WHERE p.jobId=j.id) AS participants FROM jobs j ORDER BY j.time, j.name;"
            result =  self.db.session.execute(sql).fetchall()
        else:
            sql = "SELECT j.id, j.name, j.time, (SELECT name FROM locations l WHERE l.id = j.location), array(SELECT string_to_array(u.id || ',' || u.name || ',' || p.status, ',') FROM participants p JOIN users u ON u.id=p.userId WHERE p.jobId=j.id) AS participants FROM jobs j WHERE :username IN (SELECT u.username FROM participants p JOIN users u ON u.id=p.userId WHERE p.jobId=j.id) ORDER BY j.time, j.name;"
            result =  self.db.session.execute(sql, {"username":user}).fetchall()
        self.db.session.commit()
        return result
    
    def getJob(self, id):
        sql = "SELECT j.id, j.name, j.time, (SELECT name FROM locations l WHERE l.id = j.location), array(SELECT string_to_array(u.id || ',' || u.name || ',' || p.status, ',') FROM participants p JOIN users u ON u.id=p.userId WHERE p.jobId=j.id) AS participants FROM jobs j WHERE j.id=:jobId;"
        result =  self.db.session.execute(sql, {"jobId":id}).fetchone()
        self.db.session.commit()
        return result

    def addParticipants(self, jobId, participants):
        for userId in participants:
            sql="INSERT INTO participants (jobId, userId, status) VALUES (:jobId,:userId, 'Waiting')"
            self.db.session.execute(sql, {"jobId":jobId, "userId":userId})
        self.db.session.commit()

    def createJob(self, name, time, location, participants):
        locationId = self.getLocationId(location)
        sql="INSERT INTO jobs (name, time, location) VALUES (:name,:time,:location) RETURNING id;"
        id = self.db.session.execute(sql, {"name":name,"time":time,"location":locationId}).fetchone()[0]
        self.addParticipants(id, participants)
    
    def updateJob(self, id, name, time, location, participants):
        locationId = self.getLocationId(location)
        sql="UPDATE jobs SET name=:name, time=:time, location=:location WHERE id=:id;"
        self.db.session.execute(sql, {"id":id,"name":name,"time":time,"location":locationId})
        sql="DELETE FROM participants WHERE jobId=:jobId;"
        self.db.session.execute(sql, {"jobId":id})
        self.addParticipants(id, participants)
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
    
    # Locations

    def initializeLocations(self):
        sql = "CREATE TABLE IF NOT EXISTS locations (id SERIAL PRIMARY KEY, name TEXT);"
        self.db.session.execute(sql)
        self.db.session.commit()
    
    def getLocations(self):
        result = self.db.session.execute("SELECT id, name FROM locations;").fetchall()
        return result
    
    def addLocation(self, name):
        sql = "INSERT INTO locations (name) VALUES (:name) RETURNING id;"
        res = self.db.session.execute(sql, {"name":name}).fetchone()[0]
        return res
    
    def getLocationId(self, name):
        sql = "SELECT id FROM locations WHERE name=:name"
        result = self.db.session.execute(sql, {"name":name}).fetchall()
        if len(result)<1:
            result = self.addLocation(name)
        else:
            result = result[0][0]
        return result

