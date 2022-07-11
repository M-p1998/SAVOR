from recipe_app.models import recipe
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
    # def get_all_comments(cls):
    #     query="SELECT * FROM comments;"
    #     results= connectToMySQL(cls.db_name).query_db(query)
    #     comments=[]
    #     for comment in results:
    #         comments.append(cls(comment))
    #     return comments

    @classmethod
    def get_comment_with_recipe(cls,data):
        query="SELECT * FROM comments LEFT JOIN recipes on recipes.id = comments.recipe_id WHERE comments.id = %(id)s;"
        results =  connectToMySQL(cls.db_name).query_db(query,data)
        comments = cls(results[0])
        for one_recipe in results:
            recipe_data={
                "id":one_recipe["recipes.id"],
                "name":one_recipe["name"],
                "description" : one_recipe["description"],
                "instruction": one_recipe["instruction"],
                "date_made_on" : one_recipe["date_made_on"],
                "under_30_minutes" : one_recipe["under_30_minutes"],
                "user_id" : one_recipe["user_id"],
                "created_at" : one_recipe["created_at"],
                "updated_at" : one_recipe["updated_at"]
            }
            recipes = recipe.Recipe(recipe_data)
            comments.recipess = recipes
            
        return comments
