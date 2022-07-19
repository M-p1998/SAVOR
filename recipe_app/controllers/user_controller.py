from recipe_app.config.mysqlconnection import connectToMySQL
from recipe_app import app
from flask import render_template, redirect, session, flash, request
from recipe_app.models.user import User
from recipe_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def register():
    return render_template("login_registration.html")

@app.route("/register", methods=["post"])
def createUser():
    if not User.validate_registration(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form["Password"])
    print(pw_hash)
    data={
        "Fname": request.form["Fname"],
        "Lname": request.form["Lname"],
        "Email": request.form["Email"],
        "Password": pw_hash
    }
    user_id = User.register_user(data)
    session ["user_id"] = user_id
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/logout")

    data={
        "id": session["user_id"]
    }
    user=User.get_user_by_id(data)
    recipe = Recipe.get_all_recipe()
    print(data)
    # print(recipe[0].user_id)
    return render_template("dashboard.html", user= user, recipes=recipe)

@app.route("/login", methods=["post"])
def login():
    if not User.validate_login(request.form):
        return redirect("/")

    user_data={
        "Email": request.form["Email"]
    }
    user_with_email= User.get_user_by_email(user_data)
    print(user_with_email)
    if not user_with_email:
        flash("Invalid Email/Password.","login")
        return redirect("/")
    
    if not bcrypt.check_password_hash(user_with_email.password,request.form["Password"]):
        return redirect("/")
    # populate session with logged in user's id
    session["user_id"] = user_with_email.id
    flash("Congrats!")
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/users")
def users():
    if "user_id" not in session:
        return redirect("/logout")

    # followed_users= User.show_users(data)
    users=User.get_all_users()
    # for users in user:
    #     for one in followed_users:
            
    #         if users.id == one.user_being_followed:
    #             users.one_follower = True 
    #             break
    #         else:
    #             users.one_follower=False
    # mysql = connectToMySQL("recipes")
    # query="SELECT user_being_followed FROM followers WHERE user_following = %(id)s;"
    data={
        "id":session["user_id"]
    } 
    # # {% if user.id != session.user_id %}
    # #  <td><a href="/follow/{{user.id}}">Follow</a></td>
                    
    #     # {% endif %}
    # followed_users = [user["user_being_followed"] for user in mysql.query_db(query,data)]
    followed_users = User.show_users(data)
    return render_template("users.html", user = users, followed_users=followed_users )

@app.route("/follow/<int:user_id>")
def follow(user_id):
    data={
        "uid":session["user_id"],
        "uid2": user_id 
    }
    User.followed_user(data)
    return redirect("/users")

@app.route("/unfollow/<int:user_id>")
def unfollow(user_id):
    
    data={
        "uid":session["user_id"],
        "uid2": user_id 
    }
    User.unfollowed_user(data)
    return redirect("/users")

@app.route("/profile/<int:user_id>")
def profile(user_id):
    data={
        "id": session["user_id"]
    }
    
    one_user = User.get_user_by_id(data)
    all_recipe=User.get_user_with_recipe(data)
    # userF=User.followed_user(data)
    user=User.get_user_with_user_being_followed(data)
    follower = User.get_user_with_followers(data)
    return render_template("profile.html", one_user=one_user, all_recipe=all_recipe, user=user,follower=follower)