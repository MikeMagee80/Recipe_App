from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)  #uses secret_key from __init__.py

@app.route('/')  #GET method, so no need to put method
def display_login():
    return render_template("login.html")

#need action route for registration, will be triggered by the POST of the registration form


@app.route('/user/registration', methods = ['POST'])  #action routes always return a redirect, never render_template
def process_registration():  #added request, redirect to top imports^
    # Validate the registration form
    # connect to the model
    if User.validate_registration(request.form) == False:
        return redirect('/')
    # Validate if the user already exists
    user_exists = User.get_one_to_validate_email(request.form)
    if user_exists != None:
        flash("This email already exists!", "error_registration_email")   #make sure flash is imported above
        return redirect('/')
    # proceed to create the user
    data = {
        **request.form,  #automatically copies all keys and values from dictionary to form
        "password" : bcrypt.generate_password_hash(request.form['password']) 
    }
    print(data)
    user_id = User.create(data)  #create "create" in user_model (change from User.creat(request.form) to (data), as the above dictionary is constructed)
    
    session['first_name'] = data['first_name'] #make sure session is imported above. (TDS: 1:36:16)
    session['email'] = data['email']
    session['user_id'] = user_id #created above
    return redirect('/recipes')  #initially ('/'), but changes to another route as we make it, so initially the page will just reload if it works
    #registration works!

@app.route('/user/login', methods = ['POST']) 
def process_login():
    current_user = User.get_one_to_validate_email(request.form)

    if current_user != None:
        if not bcrypt.check_password_hash(current_user.password, request.form['password']):
            flash("Wrong credentials", "error_login_credentials")
            return redirect('/')

        session['first_name'] = current_user.first_name 
        session['email'] = current_user.email
        session['user_id'] = current_user.id  

        return redirect('/recipes')

    else:
        flash("Wrong credentials", "error_login_credentials")
        return redirect('/')    #modified TDS: 1:57:20

# login works!!


# move @app.route('/recipes') to recipes_controller.py



@app.route('/user/logout')
def process_logout():
    session.clear()
    return redirect('/')