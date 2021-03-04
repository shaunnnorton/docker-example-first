from flask import Blueprint, request, render_template, redirect, url_for, flash
from recipe_app.main.forms import RecipeForm, IngredientForm
from recipe_app.models import Recipe, Ingredient, recipe_ingredient_association
from recipe_app.main.helpers import clean_input_to_list, manage_ingredients
from flask_login import login_required, current_user


from recipe_app import app, db


main = Blueprint('main', __name__)


@main.route('/',methods=['GET','POST'])
def homepage():
    context = {
        'recipes':Recipe.query.all(),
        'ingredients':Ingredient.query.all()
    }

    return render_template('home.html',**context)


@main.route('/create-recipe',methods=['GET','POST'])
@login_required
def create_recipe():
    recipe_form = RecipeForm()

    context = {
        'recipe_form':recipe_form
    }

    if recipe_form.validate_on_submit():
        recipe_ingredients = manage_ingredients(clean_input_to_list(recipe_form.ingredients.data))
        ingredient_amounts = recipe_form.ingredient_amounts.data.split(",")
        new_recipe = Recipe(
            title=recipe_form.title.data,
            description=recipe_form.description.data,
            servings=recipe_form.servings.data,
            instructions=recipe_form.instructions.data,
            image=recipe_form.image_url.data 
        )
        index=0
        for ingredient in recipe_ingredients:
            if index < len(ingredient_amounts):
                new_association = recipe_ingredient_association(amount=ingredient_amounts[index],ingredient=ingredient)
                new_recipe.ingredients.append(new_association)
            else:
                new_association = recipe_ingredient_association(amount='',ingredient=ingredient)
                new_recipe.ingredients.append(new_association)
            index += 1 

        db.session.add(new_recipe)
        db.session.commit()
        flash(f"Created New Recipe {new_recipe.title}")
        return redirect(url_for('main.view_recipe', recipe_id=new_recipe.id))

    return render_template('create_recipe.html',**context)

@main.route('/recipe/<recipe_id>')
def view_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    context = {
        "recipe":recipe
    }
    
    return render_template('recipe.html',**context)

@main.route('/ingredient/<ingredient_id>')
def view_ingredient(ingredient_id):
    ingredient = Ingredient.query.get(ingredient_id)
    context = {
        'ingredient':ingredient
    }
    print(ingredient.recipes)
    return render_template('ingredient.html', **context)




@main.route("/profile", methods=['GET',"POST"])
@login_required
def view_profile():
    return render_template('profile.html')