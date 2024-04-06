from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import EMAIL_REGEX, DATABASE   #REGEX re.compile was already setup in the __init__.py
from flask_app.models.user_model import User 



class Recipe:
    def __init__(self, data):
        self.id = data['id']        #all column headings from recipe database table
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.cooked_date = data['cooked_date']
        self.under_30 = data['under_30']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query  = "INSERT INTO recipes(name, description, instructions, cooked_date, under_30, user_id) "
        query += "VALUES( %(name)s, %(description)s, %(instructions)s, %(cooked_date)s, %(under_30)s, %(user_id)s);"

        return connectToMySQL(DATABASE).query_db(query, data) #returns the id, not an instance


    @classmethod
    def get_all_with_users(cls):   #create and test query on workbench to make sure it works, before placing it here
        query  = "SELECT * "
        query += "FROM recipes " 
        query += "JOIN users ON recipes.user_id = users.id;"

        results = connectToMySQL(DATABASE).query_db(query)  # produces list of dictionaries
        list_recipes = []   #instances
        for row in results:  #looping through each row coming from db
            current_recipe = cls(row)
            user_data = {
                **row,
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"],
                "id" : row["users.id"]
            }
            current_user = User(user_data)
            current_recipe.user = current_user    #(TDS: 48:00)
            list_recipes.append(current_recipe)
        return list_recipes



    @classmethod
    def get_one_with_user(cls, data):     #works with @app.route('/recipes/<int:id>')
        query  = "SELECT * "
        query += "FROM recipes " 
        query += "JOIN users ON recipes.user_id = users.id "
        query += "WHERE recipes.id = %(id)s;"   #retrieves single user with id matching the recipe

        result = connectToMySQL(DATABASE).query_db(query, data)  #result creates single instance (from single ref'd id)

        if len(result) > 0:
            current_recipe = cls(result[0])   #single instance returned
            user_data = {
                **result[0],   #needed to display user who contributed recipe, on recipe.html
                "created_at" : result[0]["users.created_at"],
                "updated_at" : result[0]["users.updated_at"],
                "id" : result[0]["users.id"]
            }
            current_recipe.user = User(user_data)
            return current_recipe            
        else:
            return None

    @classmethod
    def update_one(cls, data):
        query  = "UPDATE recipes "
        query += "SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, "
        query += "cooked_date = %(cooked_date)s, under_30 = %(under_30)s, user_id = %(user_id)s "  #user_id added from session (in recipes_controller), because the user is only allowed to edit his own submissions
        query += "WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def delete_one(cls, data):
        query  = "DELETE FROM recipes "
        query += "WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)



    @staticmethod
    def validate_recipe(data):    #check wireframe stickynotes (add a new recipe page) for required validations
        is_valid = True
        if data['name'] == "":
            flash("Name must not be empty", "error_recipe_name")
            is_valid = False
        if data['description'] == "":
            flash("description must not be empty", "error_recipe_description")
            is_valid = False
        if data['instructions'] == "":
            flash("Instructions must not be empty", "error_recipe_instructions")
            is_valid = False
        if data['cooked_date'] == "":
            flash("Cooked date must not be empty", "error_recipe_cooked_date")
            is_valid = False
        if len(data['name']) < 3:
            flash("Name must be at least 3 characters long", "error_recipe_name")
            is_valid = False
        if len(data['description']) < 3:
            flash("description must be at least 3 characters long", "error_recipe_description")
            is_valid = False
        if len(data['instructions']) < 3:
            flash("Instructions must be at least 3 characters long", "error_recipe_instructions")
            is_valid = False

        return is_valid