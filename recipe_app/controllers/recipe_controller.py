from recipe_app import app
from recipe_app.models.recipe import Recipe
from recipe_app.models.user import User
from flask import render_template, redirect, session, flash, request


@app.route("/recipes/new")
def new():
    return render_template("create_recipe.html")

@app.route("/create/recipe", methods=["post"])
def createRecipe():
    if "user_id" not in session:
        return redirect("/logout")

    if not Recipe.validate_recipe(request.form):
        return redirect("/recipes/new")
    print (request.form)
    data={
        "NAME": request.form["NAME"],
        "DESCRIPTION":request.form["DESCRIPTION"],
        "INSTRUCTION":request.form["INSTRUCTION"],
        "DATE_MADE_ON":request.form["DATE_MADE_ON"],
        "UNDER_30_MINUTES":request.form["UNDER_30_MINUTES"],
        "user_id": session["user_id"]
    }
    Recipe.create(data) 
    print(data)
    return redirect("/dashboard")

@app.route("/recipes/<int:id>")
def view_one(id):
    recipe_data={
        "id": id
    }
    user_data={
        "id":session["user_id"]
    }
    # One= Recipe.get_one_recipe(data)
    get_recipe=Recipe.get_one_recipe(recipe_data)
    get_user = User.get_user_by_id(user_data)
    
    return render_template("view.html", recipe=get_recipe, user=get_user)

@app.route("/recipes/edit/<int:recipe_id>")
def edit(recipe_id):
    data={
        "id": recipe_id
    }
    one=Recipe.get_one_recipe(data)
    return render_template("edit.html", oneRecipe=one)

@app.route("/update/recipe/<int:recipe_id>", methods=["post"])
def updateRecipe(recipe_id):
    data={
        "id": recipe_id,
        "NAME": request.form["NAME"],
        "DESCRIPTION":request.form["DESCRIPTION"],
        "INSTRUCTION":request.form["INSTRUCTION"],
        "DATE_MADE_ON":request.form["DATE_MADE_ON"],
        "UNDER_30_MINUTES":request.form["UNDER_30_MINUTES"],
        "user_id": session["user_id"]
    }
    Recipe.update_recipe(data)
    return redirect("/dashboard")

@app.route("/delete/<int:recipe_id>")
def delete(recipe_id):
    data={
        "id": recipe_id
    }
    Recipe.delete_recipe(data)
    return redirect("/dashboard")
