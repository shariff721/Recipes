from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.recipe import Recipe


@app.route("/new/recipe")
def add_new_recipe():
    return render_template("add_new_recipe.html")


@app.route("/process/recipe", methods=["POST"])
def process_recipe():
    if not Recipe.validate_spice(request.form):
        return redirect(request.referrer)
    else:
        data = {
            "name": request.form["name"],
            "under": request.form["under"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "date_made": request.form["date_made"],
            "user_id": session['user_id']
        }
        Recipe.add_recipe(data)
        return redirect('/dashboard')


@app.route('/delete/<int:id>')
def delete_spice(id):
    data = {
        "id": id
    }
    Recipe.delete_recipe(data)
    return redirect('/dashboard')


@app.route('/recipe/edit/<int:id>')
def edit_recipe(id):
    return render_template("edit_recipe.html", one_recipe = Recipe.get_one_with_owner({"id": id}))


@app.route('/recipe/update', methods=["POST"])
def update_my_recipe():
    if not Recipe.validate_spice(request.form):
        return redirect(request.referrer)
    # print(request.form)
    Recipe.update_recipe(request.form)
    return redirect('/dashboard')

@app.route('/recipe/<int:id>')
def show_one_recipe(id):
    data = {
        "id":id
    }
    one_recipe_posted = Recipe.get_one_with_owner(data)
    return render_template("recipe_dashboard.html",one_recipe_posted = one_recipe_posted)
