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

        self.LIKE=False

        # self.liked_by=[]
        
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

    # @classmethod
    # def likeComments(cls,data):
    #     # query="SELECT COUNT(comment_id) as times_liked from likes RIGHT JOIN comments ON comments.id = likes.comment_id JOIN users ON comments.user_id = users.id GROUP BY comment_id ORDER BY comments.created_at DESC;"
    #     query="SELECT * FROM comments LEFT JOIN likes ON comments.id = likes.comment_id LEFT JOIN users ON user.id = likes.user_id ;"
    #     results = connectToMySQL(cls.db_name).query_db(query,data)
    #     likes = []
    #     for like in results:
    #         # if like["comment_id"] in likes:
    #         #     like["liked_comments"] = True
    #         # else:
    #         #     like["liked_comments"]=False
    #         likes.append(cls(like))
    #     # c = 0
    #     # count = 0
    #     # for row in results:
    #     #     if not row["id"] == c:
    #     #         likes.append(cls(row))
    #     #         user_data={
    #     #             "id" : row["id"],
    #     #             "first_name" : row["first_name"],
    #     #             "last_name" :row["last_name"],
    #     #             "email" :row["email"],
    #     #             "password" :row["password"],
    #     #             "created_at" : row["created_at"],
    #     #             "updated_at": row["updated_at"]
    #     #         }
    #     #         likes[count].liked_by.append(user.User(user_data))
    #     #         c= row["id"]
    #     #         count += 1
    #     #     else:
    #     #         user_data={
    #     #             "id" : row["id"],
    #     #             "first_name" : row["first_name"],
    #     #             "last_name" :row["last_name"],
    #     #             "email" :row["email"],
    #     #             "password" :row["password"],
    #     #             "created_at" : row["created_at"],
    #     #             "updated_at": row["updated_at"]
    #     #         }
    #     #         likes[count-1].liked_by.append(user.User(user_data))

    #     return likes

   

    @classmethod
    def add_like(cls,data):
        query="INSERT INTO likes (user_id, comment_id) VALUES (%(user_id)s, %(comment_id)s);"
        results= connectToMySQL(cls.db_name).query_db(query,data)
        return results

    @classmethod
    def unLike(cls,data):
        query="DELETE FROM likes WHERE user_id= %(user_id)s AND comment_id = %(comment_id)s;"
        results= connectToMySQL(cls.db_name).query_db(query,data)
        return results