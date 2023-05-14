from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
import re
from flask import flash


class Recipe:
    DB = "recipes_DB"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under = data['under']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.owner = None

    @classmethod
    def add_recipe(cls, data):
        query = """
            INSERT INTO recipe (name, under, description, instructions, date_made,user_id) 
            VALUES (%(name)s, %(under)s, %(description)s, %(instructions)s, %(date_made)s,%(user_id)s);
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
    

    @classmethod
    def get_all_recipes_with_owner(cls):
        query = """
            SELECT * FROM recipe JOIN users ON recipe.user_id = users.id
        """
        results = connectToMySQL(cls.DB).query_db(query)
        all_recipes = []

        for user_row in results:
            
            one_recipe = cls(user_row)
            
            user_data = {
                "id": user_row["users.id"],
                "first_name": user_row["first_name"],
                "last_name": user_row["last_name"],
                "email": user_row["email"],
                "password": user_row["password"],
                "created_at": user_row["created_at"],
                "updated_at": user_row["updated_at"]
            }

            one_recipe.owner = user.User(user_data)
            all_recipes.append(one_recipe)

        return all_recipes
    

    @classmethod
    def update_recipe(cls, data):
        query = """
            UPDATE recipe
            SET name = %(name)s, under = %(under)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_one_with_owner(cls,data):
        query = """
            SELECT * FROM recipe JOIN users ON recipe.user_id = users.id
            WHERE recipe.id = %(id)s
        """
        results = connectToMySQL(cls.DB).query_db(query,data)

        one_recipe = cls(results[0]) 
        user_data = { 
            'id':results[0]['users.id'],
            'first_name':results[0]['first_name'],
            'last_name':results[0]['last_name'],
            'email':results[0]['email'],
            'password':results[0]['password'],
            'created_at':results[0]['users.created_at'],
            'updated_at':results[0]['users.updated_at']
        }
        # we create an instance of the User class with the user data.
        one_user = user.User(user_data)
        one_recipe.owner = one_user  

        return one_recipe


    @classmethod
    def delete_recipe(cls, data):
        query = """
            DELETE FROM recipe WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query,data)

    @staticmethod
    def validate_spice(spice):
        is_valid = True

        if len(spice['description']) < 1:
            flash("Description must not be blank.")
            is_valid = False

        if len(spice['date_made']) < 1:
            flash("Date must not be blank.")
            is_valid = False
        
        if "under" not in spice:
            flash(" Under cannot be left Empty")
            is_valid = False

        return is_valid
