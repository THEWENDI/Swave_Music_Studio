from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class User:
    db = "sw_db"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.message = data['message']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (name,email,message) VALUES(%(name)s,%(email)s,%(message)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_contact(user):
        is_valid = True
        # (User.db) User is the class name!!
        if len(user['name']) < 2:
            flash("name must be at least 3 characters","register")
            is_valid= False
        if len(user['email']) < 4:
            flash("email must be at least 5 characters","register")
            is_valid= False
        if len(user['message']) < 5:
            flash("message must be at least 6 characters","register")
            is_valid= False
        return is_valid

    @staticmethod
    def validate_login(formdata):
        is_valid = True
        user = User.get_by_email(formdata)
        if not user:
            flash("Invalid Login","login")
            is_valid= False
        elif not bcrypt.check_password_hash(user.password,formdata['password']):
            flash("Invalid Login","login")
            is_valid= False
        return is_valid