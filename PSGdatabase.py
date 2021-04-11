from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import generate_password_hash

class PSGdatabase:
    def __init__(self, app):
        self.app = app
        self.db = SQLAlchemy(app)

        self.initializeUsers()
    
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
        result =  self.db.session.execute("SELECT * FROM users").fetchall()
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
