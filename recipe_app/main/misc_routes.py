# Routes that do not fill the typical purposes of viewing recipie
# informaiton or modifying recipe information
from flask import (Blueprint, request, render_template)
from recipe_app.main.forms import RecipeForm, IngredientForm

misc = Blueprint("misc", __name__)


@misc.route("/Test/Secret/GoAway", methods=["GET", "POST"])
def TestRoute():
    recipe_form = RecipeForm()
    ingredient_form = IngredientForm()

    if ingredient_form.validate_on_submit():
        print(ingredient_form.name.raw_data)

    context = {
        'recipe_form': recipe_form,
        'ingredient_form': ingredient_form
    }
    return render_template('test.html', **context)


@misc.route("/secret/mothersday/2021", methods=["GET"])
def mothers_day():
    if request.user_agent.platform == "iphone":
        return render_template("mothersdaytessa.html")

    print(request.user_agent.platform)

    return render_template("mothersdaymom.html")
