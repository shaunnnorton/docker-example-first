# Routes for viewing the current state of informaiton on the server
# or in the database.
from flask import (Blueprint, render_template,
                   send_from_directory)
from recipe_app.main.forms import SearchForm
from recipe_app.models import Recipe, Ingredient

from flask_login import login_required
import os

from recipe_app import app

view = Blueprint("view", __name__)


@view.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


@view.route('/', methods=['GET', 'POST'])
def homepage():
    """Homepage to be rendered on base route"""
    context = {
        'recipes': Recipe.query.all(),
        'ingredients': Ingredient.query.all()
    }

    return render_template('home.html', **context)


@view.route('/recipe/<recipe_id>')
def view_recipe(recipe_id):
    """Shows information for a recipe with given recipe id """
    recipe = Recipe.query.get(recipe_id)
    context = {
        "recipe": recipe
    }

    return render_template('recipe.html', **context)


@view.route('/ingredient/<ingredient_id>')
def view_ingredient(ingredient_id):
    """Shows All recipes with ingredient as and ingredient"""
    ingredient = Ingredient.query.get(ingredient_id)
    context = {
        'ingredient': ingredient
    }

    return render_template('ingredient.html', **context)


@view.route("/profile", methods=['GET', "POST"])
@login_required
def view_profile():
    """Shows the profile of the currently logged in user"""
    return render_template('profile.html')


@view.route('/search', methods=['GET', 'POST'])
def search():
    """Shows a page allowing for the searching of a recipe or ingredient"""
    form = SearchForm()
    if form.validate_on_submit():
        print('HELLO')

        recipe_results = Recipe.query.filter(
            Recipe.title.like(f'%{form.search_query.data}%')).all()
        ingredient_results = Ingredient.query.filter(
            Ingredient.name.like(f'%{form.search_query.data}%')).all()
        context = {
            'recipe_results': recipe_results,
            'ingredient_results': ingredient_results,
            'form': SearchForm(search_query=form.search_query.data)
        }
        print(context)
        return render_template('search.html', **context)

    return render_template('search.html', form=form)
