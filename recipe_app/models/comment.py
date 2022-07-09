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

    @classmethod
    def createComment(cls,data):
        query="INSERT INTO comments (comment,user_id,recipe_id) VALUES (%(comment)s,%(user_id)s,%(recipe_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)