from flask import Blueprint, request, render_template, redirect, url_for, flash
from recipe_app.main.forms import RecipeForm, IngredientForm
from recipe_app.models import Recipe, Ingredient


from recipe_app import app, db


main = Blueprint('main', __name__)


@main.route('/',methods=['GET','POST'])
def homepage():
    recipe_form = RecipeForm()
    ingredient_form = IngredientForm()

    context = {
        'recipe_form':recipe_form,
        'ingredient_form':ingredient_form

    }

    if ingredient_form.validate_on_submit():
        new_ingredient = Ingredient(name=ingredient_form.name.data)
        db.session.add(new_ingredient)
        db.session.commit()
        print("YOU MADE IT HERE")
        flash("NEW INGREDIENT ADDED")
        #context['recipe_form']= RecipeForm(recipe_form)
        return render_template('test.html',**context)

    return render_template('test.html',**context)