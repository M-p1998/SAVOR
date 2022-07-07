from recipe_app import app
from recipe_app.models.recipe import Recipe
from recipe_app.models.user import User
from flask import render_template, redirect, session, flash, request

@app.route("/recipes/new")
def new():
    return render_template("create_recipe.html")

@app.route("/create/recipe", methods=["post"])
def createRecipe():
    data={
        "NAME": request.form["NAME"],
        "DESCRIPTION":request.form["DESCRIPTION"],
        "INSTRUCTION":request.form["INSTRUCTION"],
        "DATE_MADE_ON":request.form["DATE_MADE_ON"],
        "UNDER_30_MINUTES":request.form["UNDER_30_MINUTES"],
        "user_id": session["user_id"]
    }
    Recipe.create(data)
    return redirect("/dashboard")

@app.route("/recipes/<int:recipe_id>")
def view_one(recipe_id):
    data={
        "id": recipe_id
    }
    # One= Recipe.get_one_recipe(data)
    get_recipe=Recipe.get_one_recipe(data)
    get_user = User.get_user_by_id(data)
    return render_template("view.html", One_recipe=get_recipe, One=get_user)