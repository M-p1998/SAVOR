from recipe_app.config.mysqlconnection import connectToMySQL
from recipe_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re	  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db_name="recipes"
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        # self.one_follower = False
        
    
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(Email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(results)
        if len(results) == 0:
            return False    
        else:
            return cls(results[0])

    @classmethod
    def register_user(cls, data):
        query= "INSERT INTO users (first_name,last_name,email,password,created_at,updated_at) VALUES (%(Fname)s,%(Lname)s,%(Email)s,%(Password)s,NOW(),NOW());"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results

    @staticmethod
    def validate_registration(data):
        is_valid = True
        if len(data["Fname"]) <2:
            flash("First name must be at least 2 characters.","register")
            is_valid = False

        if len(data["Lname"]) <2:
            flash("Last name must be at least 2 characters.","register")
            is_valid = False

        if len(data["Email"]) == 0:
            flash("Email must be entered.","register")
            is_valid = False
        elif not EMAIL_REGEX.match (data["Email"]):
            flash("Invalid email address!","register")
            is_valid = False

        # validation on passwords to have a least 1 number and 1 uppercase letter
        # elif not data["password"].isdigit():
        #     flash("Your password has a number in it.")
        #     is_valid=False
        # elif not len(data["password"]).isupper():
        #     flash("Your password has a capital letter in it.")
        #     is_valid=False

        if len(data["Password"]) <8:
            flash("Password must be at least 8 characters.","register")
            is_valid = False

        if data['Password'] != data["confirm_password"]:
            flash("Your passwords do not match.","register") 
            is_valid = False

        query = "SELECT * FROM users WHERE email = %(Email)s;"
        results = connectToMySQL(User.db_name).query_db(query,data)
        print(f"results:{results}")
        # we do not expect anything to be inside of result.
        if len(results) >= 1:
            flash("That email is already taken!","register")
            is_valid =False
        return is_valid

    @classmethod
    def login_user(cls,data):
        query="INSERT INTO users (email,password) VALUES (%(Email)s,%(Password)s);"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results

    @staticmethod
    def validate_login(data):
        is_valid = True
        return is_valid

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results=connectToMySQL(cls.db_name).query_db(query)
        users=[]
        for one_user in results:
            users.append(cls(one_user))
        return users

    @classmethod
    def followed_user(cls,data):
        query="INSERT INTO followers (user_following, user_being_followed) VALUES (%(uid)s, %(uid2)s);"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results

    @classmethod
    def unfollowed_user(cls,data):
        query="DELETE FROM followers WHERE user_following=%(uid)s AND user_being_followed=%(uid2)s;"
        results= connectToMySQL(cls.db_name).query_db(query,data)
        return results

    @classmethod
    def show_users(cls,data):
        query="SELECT user_being_followed FROM followers WHERE user_following = %(id)s;"
        # query = "SELECT * FROM users WHERE id <> %(id)s ORDER BY last_name ASC"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        users=[]
        for user in results:
            users.append(user["user_being_followed"])
        return users

   