# Routes that modify the state of the server
from flask import (Blueprint, render_template, redirect, url_for,
                   flash)
from recipe_app.main.forms import RecipeForm
from recipe_app.models import Recipe, recipe_ingredient_association
from recipe_app.main.helpers import manage_ingredients
from flask_login import login_required, current_user

from recipe_app import db


modify = Blueprint("modify", __name__)


@modify.route('/create-recipe', methods=['GET', 'POST'])
@login_required
def create_recipe():
    """Allows the user to create a recipe if they are authenticated"""
    recipe_form = RecipeForm()

    context = {
        'recipe_form': recipe_form
    }

    if recipe_form.validate_on_submit():
        recipe_ingredients = manage_ingredients(
            recipe_form.ingredients.raw_data)
        print(recipe_ingredients)
        ingredient_amounts = recipe_form.ingredient_amounts.raw_data
        imgurl = recipe_form.image_url.data
        if len(recipe_form.image_url.data) < 6:
            imgurl = ('https://www.dropbox.com/s/bw12'
                      + '7notc75i8yn/Chicken.gif?raw=1')

        new_recipe = Recipe(
            title=recipe_form.title.data,
            description=recipe_form.description.data,
            servings=recipe_form.servings.data,
            instructions=recipe_form.instructions.data,
            image=imgurl
        )
        index = 0
        for ingredient in recipe_ingredients[:-1]:
            if index < len(ingredient_amounts):
                new_association = recipe_ingredient_association(
                    amount=ingredient_amounts[index], ingredient=ingredient)
                new_recipe.ingredients.append(new_association)
            else:
                new_association = recipe_ingredient_association(
                    amount='', ingredient=ingredient)
                new_recipe.ingredients.append(new_association)
            index += 1

        db.session.add(new_recipe)
        db.session.commit()
        flash(f"Created New Recipe {new_recipe.title}")
        return redirect(url_for('main.view_recipe', recipe_id=new_recipe.id))

    return render_template('create_recipe.html', **context)


@modify.route('/favorite/<recipe_id>')
@login_required
def add_favorite(recipe_id):
    """Adds the recipe with given id the the current users favorites"""
    recipe = Recipe.query.get(recipe_id)
    current_user.favorite_recipes.append(recipe)
    db.session.commit()
    flash('You Have Favorited This Recipe!')
    return redirect(url_for('main.view_recipe', recipe_id=recipe_id))


@modify.route('/unfavorite/<recipe_id>')
@login_required
def remove_favorite(recipe_id):
    """Removes the recipe with the given recipe_id from the current
     users favorites."""
    recipe = Recipe.query.get(recipe_id)
    if recipe in current_user.favorite_recipes:
        current_user.favorite_recipes.remove(recipe)
        db.session.commit()
    flash('You Have Unfavorited This Recipe!')
    return redirect(url_for('main.view_recipe', recipe_id=recipe_id))


@modify.route("/remove/recipe/<recipe_id>")
@login_required
def remove_recipe(recipe_id):
    if current_user.is_authenticated:
        recipe = Recipe.query.get(recipe_id)
        for item in recipe.ingredients:
            db.session.delete(item)
        db.session.delete(recipe)
        db.session.commit()
        return redirect(url_for("main.homepage"))
    return redirect(url_for("main.homepage"))
