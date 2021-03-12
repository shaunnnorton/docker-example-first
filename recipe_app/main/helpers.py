from recipe_app.models import Ingredient
from recipe_app import app, db
from difflib import SequenceMatcher


def clean_input_to_list(_text):
    """Splits a string at commas and creates a list"""
    striped_input = _text.replace(' ','|')
    striped_input = striped_input.lower()
    seperated_input = striped_input.split(",")
    return seperated_input
    

# def split_amount_ingredient(_list):
#     """Attempts to split the amount of an ingredient from the name"""
#     ingredients = list()
#     amounts = list()
#     for item in _list:



def manage_ingredients(ingredient_list):
    """Insures all items in provided list are Ingredient models by querying or creating one"""
    ingredient_list_db = list()
    for item in ingredient_list:
        clean_item = item.lower()
        db_item = Ingredient.query.filter_by(name=clean_item).first()
        if db_item:
            ingredient_list_db.append(db_item)
            print(f"{clean_item} exists")
        else:
            new_ingredient = Ingredient(name=clean_item)
            db.session.add(new_ingredient)
            db.session.commit()
            ingredient_list_db.append(new_ingredient)
    return ingredient_list_db

test_string = "1 Cup Apples, 2 TBS Cheese, 5 Eggs"
print(clean_input_to_list(test_string))