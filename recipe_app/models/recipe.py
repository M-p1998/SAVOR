from recipe_app.config.mysqlconnection import connectToMySQL
from recipe_app.models import recipe
class Recipe:
    def __init__(self,data):
        self.id=data["id"]
        self.name=data["name"]
        self.description = data["description"]
        self.instruction= data["instruction"]
        self.date_made_on = data["date_made_on"]
        self.under_30_minutes = data["under_30_minutes"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create(cls,data):
        query="INSERT INTO recipes (name,description,instruction,date_made_on,under_30_minutes,user_id) VALUES (%(NAME)s,%(DESCRIPTION)s, %(INSTRUCTION)s, %(DATE_MADE_ON)s, %(UNDER_30_MINUTES)s, %(user_id)s);"
        return connectToMySQL("recipes").query_db(query,data)

    @classmethod
    def get_all_recipe(cls):
        query="SELECT * FROM recipes;"
        result = connectToMySQL("recipes").query_db(query)
        recipes=[]
        for one_recipe in result:
            recipes.append(cls(one_recipe))
        return recipes

    @classmethod
    def get_user_with_recipes(cls,data):
        query="SELECT * FROM users LEFT JOIN recipes ON recipes.user_id = users.id WHERE users.id = %(id)s ;"
        results= connectToMySQL("recipes").query_db(query,data)
        users = cls(results[0])
        for all in results:
            recipe_data={
                "id": all["recipes.id"],
                "name": all["name"],
                "description":all["description"],
                "instruction":all["instruction"],
                "date_made_on":all["date_made_on"]
            }
            users.recipe


