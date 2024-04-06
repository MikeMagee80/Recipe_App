from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.recipe_model import Recipe




@app.route('/recipes') #use route names from wireframe urls
def display_recipes():
    if 'email' not in session:   #validate session, so only logged-in users can see this page
        return redirect('/')
    # Grab all the recipes!
    list_recipes =  Recipe.get_all_with_users()
    return render_template('recipes.html', list_recipes = list_recipes)

@app.route('/recipe/new')
def display_create_recipe():
    if 'email' not in session:   #validate session, so only logged-in users can see this page
        return redirect('/')
    return render_template('create_recipe.html')

@app.route('/recipe/create', methods = ['POST'])
def create_recipe():
    # validate
    if Recipe.validate_recipe(request.form) == False:
        return redirect('/recipe/new')
    # Create the recipe
    data = {
        **request.form,                  #dictionary 
        "user_id" : session['user_id']   #from session in login in users_controller.py
    }
    Recipe.create(data)
    # Redirect to the /recipes view (as in wireframe)
    return redirect('/recipes')

@app.route('/recipes/<int:id>')
def display_one(id):
    if 'email' not in session:   #validate session, so only logged-in users can see this page
        return redirect('/')
    data = {
        "id" : id
    }
    current_recipe = Recipe.get_one_with_user(data)   #need the user for labele purposes
    return render_template("recipe.html", current_recipe = current_recipe)


@app.route('/recipes/<int:id>/update')      #display route, so insert session
def display_update_recipe(id):
    if 'email' not in session:   #validate session, so only logged-in users can see this page
        return redirect('/')
    data = {
        "id" : id
    }
    current_recipe = Recipe.get_one_with_user(data)  #copied from above
    return render_template("update_recipe.html", current_recipe = current_recipe)    #this pre-populates edit page 


@app.route('/recipe/update/<int:id>', methods = ['POST'])
def update_recipe(id):
    if Recipe.validate_recipe(request.form) == False:
        return redirect( f'/recipes/{id}/update')
    recipe_data = {
        **request.form,
        "id" : id,
        "user_id" : session['user_id']  #added for access control 
    }
    Recipe.update_one(recipe_data)
    return redirect('/recipes')


@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
    data = {
        "id" : id
    }
    Recipe.delete_one(data)
    return redirect('/recipes')
