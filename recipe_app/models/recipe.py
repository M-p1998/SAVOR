

class Recipe:
    def __init__(self,data):
        self.name=data["name"]
        self.description = data["description"]
        self.instructions= data["instructions"]
        self.date_made_on = data["date_made_on"]
        self.under_30_minutes = data["under_30_minutes"]
        