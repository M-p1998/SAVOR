from recipe_app import app
from recipe_app.controllers import user_controller,recipe_controller


if __name__ == "__main__":
    app.run(debug=True)