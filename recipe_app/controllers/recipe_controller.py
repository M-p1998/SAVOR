from recipe_app import app
from recipe_app.models.recipe import Recipe
from recipe_app.models.user import User
from recipe_app.models.comment import Comment
from flask import render_template, redirect, session, flash, request


@app.route("/recipes/new")
def new():
    # recipe = Recipe.search_R()
    # print(recipe)
    data={
        "id": session["user_id"]
    }
    user=User.get_user_by_id(data)
    return render_template("create_recipe.html", user=user)

# @app.route("/results")
# def results():
#     return render_template("results.html", recipes = results)

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
    if "user_id" not in session:
        return redirect("/logout")

    data={
        "id":session["user_id"]
    } 
    recipe_data={
        "id": id,
        "user_id": session["user_id"]
    }
    user_data={
        "id":session["user_id"]
    }
    comments = Recipe.get_recipe_with_comment(recipe_data)
   
    # print(comments[0])
    # comments = User.get_comment_with_user(user_data)
    get_recipe=Recipe.get_one_recipe(recipe_data)
    get_user = User.get_user_by_id(user_data)
    user = Recipe.get_recipe_with_user(recipe_data)
    print(user)
    return render_template("view.html", recipe=get_recipe, user=get_user, NewUser=user, all=comments)

@app.route("/recipes/edit/<int:recipe_id>")
def edit(recipe_id):
    if "user_id" not in session:
        redirect ("/logout")
    data={
        "id": recipe_id
    }
    one=Recipe.get_one_recipe(data)
    return render_template("edit.html", oneRecipe=one)

@app.route("/update/recipe/<int:recipe_id>", methods=["post"])
def updateRecipe(recipe_id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/recipes/edit/{recipe_id}")
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

@app.route("/writeComment/<int:recipe_id>", methods=["post"])
def create_comment(recipe_id):
    if not Comment.validate_comment(request.form):
        return redirect(f"/recipes/{recipe_id}")
    print(request.form)
    data={
        "comment": request.form["comment"],
        "user_id": session["user_id"],
        # "recipe_id": request.form["recipe_id"],
        "recipe_id": recipe_id,
        "id" :recipe_id
    }
    comment = Comment.createComment(data)
    print(request.form)
    return redirect(f"/recipes/{recipe_id}")

@app.route("/comments/<int:comment_id>/<int:recipe_id>/add_like")
def like_comment(comment_id,recipe_id):
    data = {
        "user_id": session["user_id"],
        'comment_id': comment_id
    }
   
    c = Comment.add_like(data)
    print(data)
    return redirect(f"/recipes/{recipe_id}")

@app.route("/comments/<comment_id>/<int:recipe_id>/unlike")
def unlike_comment(comment_id,recipe_id):
    data = {
        'user_id': session['user_id'],
        "comment_id": comment_id
    }
    
    Comment.unLike(data)
    return redirect(f"/recipes/{recipe_id}")

# create search
# @app.route("/search" ,  methods=["post"])
# def search_recipe_with_all():
#     # if not Recipe.validate_search_recipe(request.form):
#     #     return redirect("/recipes/new")
#     # data={
#     #     "NAME": request.form["search_recipes"],
       
#     # }
#     if not Recipe.validate_search_recipe(request.form):
#         flash("Name must be at least 1 characters.", "search")
#         return redirect("/search")
    
#     data={
#         "NAME": request.form["search_recipes"],
#         "DESCRIPTION": request.form["DESCRIPTION"],
#         "INSTRUCTION": request.form["INSTRUCTION"],
#         "DATE_MADE_ON":request.form["DATE_MADE_ON"],
#         "UNDER_30_MINUTES":request.form["UNDER_30_MINUTES"]
#     }


    
    
#     # Recipe.search_R(data)
#     # return redirect("/dashboard")
#     results = Recipe.search_R(data)
#     if results:
#         return redirect("/results")
#     else:
#         flash("No results found.")
#         return redirect("/dashboard")


# Create a route for the search functionality
# @app.route("/search", methods=["POST"])
# def search_recipe():
#     data = {
#         "search_recipes": request.form["search_recipes"]
#     }

#     # Validate the search query
#     if not Recipe.validate_search_recipe(data):
#         flash("Search query must be at least 1 character long.", "search")
#         return redirect("/recipes/new")

#     # Search the database
#     results = Recipe.search_R(data)

#     # Check if any results were found
#     if results:
#         return render_template("results.html", recipes=results)
#     else:
#         flash("No results found.")
#         return redirect("/dashboard")

# In your search route function
# @app.route("/search" ,  methods=["post"])
# def search_recipe_with_all():
#     if not Recipe.validate_search_recipe(request.form):
#         flash("Name must be at least 1 characters.","search")
#         return redirect("/recipes/new")
#         # return redirect("/recipes/new")
#     data={
#         "search_recipes": request.form["search_recipes"]
#     }
#     results = Recipe.search_R(data)
#     print(results)
#     if results:
#         # return render_template("results.html", recipes=results)
#         return redirect("/results")
#     else:
#         flash("No results found.")
#         return redirect("/dashboard")


# @app.route("/search" ,  methods=["post"])
# def search_recipe_with_all():
#     if not Recipe.validate_search_recipe(request.form):
#         flash("Name must be at least 1 characters.","search")
#         return redirect("/recipes/new")
#         # return redirect("/recipes/new")
#     data={
#         "search_recipes": request.form["search_recipes"]
#     }
#     results = Recipe.search_R(data)
#     print(results)
#     if results:
#         return render_template("results.html", recipes=results)
#         # return redirect("/results")
#     else:
#         flash("No results found.")
#         return redirect("/dashboard")

# -----------------------------------------------

# import pymysql

# # Connect to the database
# connection = pymysql.connect(host='your_host',
#                              user='your_username',
#                              password='your_password',
#                              db='your_database')

# # Create a cursor object
# cursor = connection.cursor()

# # Execute the query
# cursor.execute(query, data)

# # Fetch the results
# results = cursor.fetchall()

# # Close the cursor and connection
# cursor.close()
# connection.close()



    
