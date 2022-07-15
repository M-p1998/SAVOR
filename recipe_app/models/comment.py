from recipe_app.models import recipe
from recipe_app.models import user
from recipe_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Comment:
    db_name="recipes"
    def __init__(self,data):
        self.id = data["id"]
        self.comment = data["comment"]
        self.user_id =data["user_id"]
        self.recipe_id =data["recipe_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.userss = []

        self.userName=""
        
    @classmethod
    def createComment(cls,data):
        query="INSERT INTO comments (comment,user_id,recipe_id) VALUES (%(comment)s,%(user_id)s,%(recipe_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_user_with_comment(cls,data):
        query="SELECT * FROM users LEFT JOIN comments ON comments.user_id = users.id WHERE users.id = %(id)s ;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        comment = cls(results[0])
        for one_user in results:
            user_data={
                "id" : one_user["id"],
                "first_name" : one_user["first_name"],
                "last_name" :one_user["last_name"],
                "email" :one_user["email"],
                "password" :one_user["password"],
                "created_at" : one_user["created_at"],
                "updated_at": one_user["updated_at"]
            }
            comment.userss.append(user.User(user_data))
        return comment

    @staticmethod
    def validate_comment(data):
        is_valid=True
        if len(data["comment"]) < 3:
            flash("Comment must be at least 3 characters.","comment")
            is_valid = False
        return is_valid