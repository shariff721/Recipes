from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    DB = "recipes_DB"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

        self.recipes = []

    @classmethod
    def save(cls,data):
        query = """ INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result 
    
    @classmethod
    def get_all(cls):
        query = """ SELECT * FROM users;"""
        results = connectToMySQL(cls.DB).query_db(query)
        
        all_users = []

        for user in results:
            all_users.append(cls(user))
        return all_users
    
    @classmethod
    def get_one_by_email(cls,data):
        query = """ SELECT * FROM users WHERE email = %(email)s """
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_one_by_id(cls,data):
        query = """
            SELECT * FROM users WHERE id = %(id)s
        """
        result = connectToMySQL(cls.DB).query_db(query,data)
        print(result)
        return cls(result[0])

    @staticmethod
    def validate_user(user):
        is_valid = True

        if len(user['first_name']) < 3:
            flash("Name must be atleat 3 characters.")
            is_valid = False

        if len(user['last_name']) < 3:
            flash("Name must be atleast 3 characters.")
            is_valid = False

        if len(user['password']) < 1:
            flash("Invalid password!!!")
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!!!")
            is_valid = False
        return is_valid
