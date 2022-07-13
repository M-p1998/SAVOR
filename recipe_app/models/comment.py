from recipe_app.models import recipe
from recipe_app.models import user
from recipe_app.config.mysqlconnection import connectToMySQL

class Comment:
    db_name="recipes"
    def __init__(self,data):
        self.id = data["id"]
        self.comment = data["comment"]
        self.user_id =data["user_id"]
        self.recipe_id =data["recipe_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.recipess = []

    @classmethod
    def createComment(cls,data):
        query="INSERT INTO comments (comment,user_id,recipe_id) VALUES (%(comment)s,%(user_id)s,%(recipe_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    # @classmethod
    # def get_user_with_comment(cls,data):
    #     query="SELECT * FROM users LEFT JOIN comments ON comments.user_id = users.id WHERE users.id = %(id)s ;"
    #     results = connectToMySQL(cls.db_name).query_db(query,data)
    #     user = cls(results[0])
    #     for one_user in results:
    #         comment_data={
    #             "id" : one_user["id"],
    #             "comment" : one_user["comment"],
    #             "user_id" :one_user["user_id"],
    #             "recipe_id" :one_user["recipe_id"],
    #             "created_at" : one_user["created_at"],
    #             "updated_at": one_user["updated_at"]
    #         }
    #         user.comment.append(comment)


    