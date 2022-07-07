from recipe_app.config.mysqlconnection import connectToMySQL
from recipe_app.models import user
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

        self.users=[]

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
    def get_recipe_with_user(cls):
        query="SELECT * FROM recipes LEFT JOIN users on users.id = recipes.user_id ;"
        results= connectToMySQL("recipes").query_db(query)
        recipe = cls(results[0])
        for all in results:
            recipe_data={
                "id": all["users.id"],
                "first_name": all["first_name"],
                "last_name":all["last_name"],
                "email":all["email"],
                "password":all["password"],
                "created_at":all["created_at"],
                "updated_at":all["updated_at"]
            }
            recipe.users.append(user.User(recipe_data))
        return recipe

    @classmethod
    def get_one_recipe(cls,data):
        query="SELECT * FROM recipes WHERE recipes.id=%(id)s;"
        results=  connectToMySQL("recipes").query_db(query,data)
        return cls(results[0])


