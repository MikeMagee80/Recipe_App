from flask_app import app

from flask_app.controllers import users_controller, recipes_controller

if __name__=="__main__":
    app.run(debug=True)


# pip3 install pipenv

# pipenv install flask   now: pipenv install PyMySQL flask  
# NOW: pipenv install flask pymysql flask-bcrypt

# pipenv shell to activate virtual environment. exit to deactivate

# python3 server.py

# CTRL + C to quit