from recipe_app.models import Ingredient
from recipe_app import app, db


def clean_input_to_list(_text):
    """Splits a string at commas and creates a list"""
    striped_input = "".join(_text.split())
    striped_input = striped_input.lower()
    seperated_input = striped_input.split(",")
    return seperated_input
    

def manage_ingredients(ingredient_list):
    """Insures all items in provided list are Ingredient models by querying or creating one"""
    ingredient_list_db = list()
    for item in ingredient_list:
        db_item = Ingredient.query.filter_by(name=item).first()
        if db_item:
            ingredient_list_db.append(db_item)
            print(f"{item} exists")
        else:
            new_ingredient = Ingredient(name=item)
            db.session.add(new_ingredient)
            db.session.commit()
            ingredient_list_db.append(new_ingredient)
    return ingredient_list_db
