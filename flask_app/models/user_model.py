from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import EMAIL_REGEX, DATABASE   #REGEX re.compile was already setup in the __init__.py



class User:
    def __init__(self, data):   #needs every data column from the database
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_one_to_validate_email(cls, data):   #"user must not already exist in the DB"
        query  = "SELECT * "
        query += "FROM users "
        query += "WHERE email = %(email)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)   #TDS: 1:14:50 in video 1

        if len(result) > 0: #IOW, that email doesn't exist in the DB
            current_user = cls(result[0])
            return current_user
        else:
            return None #instance

    @classmethod
    def create(cls, data):
        query  = "INSERT INTO users(first_name, last_name, email, password)" 
        query += "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"

        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @staticmethod
    def validate_registration(data):  #look at wireframe for required validations for registration
        is_valid = True
        if len(data['first_name']) < 2:
            flash("Your first name needs to have at least 2 characters", "error_registration_first_name")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Your lastname needs to have at least 2 characters", "error_registration_last_name")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email", "error_registration_email")
            is_valid = False
        if data['password'] != data['password_confirmation']:
            flash("Your passwords do not match", "error_registration_password_confirmation")
            is_valid = False
        return is_valid              #now integrate this into your controller   

