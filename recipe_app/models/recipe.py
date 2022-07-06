from 
class Recipe:
    def __init__(self,data):
        self.id=data["id"]
        self.name=data["name"]
        self.description = data["description"]
        self.instruction= data["instruction"]
        self.date_made_on = data["date_made_on"]
        self.under_30_minutes = data["under_30_minutes"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

