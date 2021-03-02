from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from recipe_app.models import User, Recipe, Ingredient


class RecipeForm(FlaskForm):
    """Form to create a Recipe"""
    title = StringField("Title", validators=[DataRequired(),Length(min=4,max=80)])
    description = TextAreaField('Description')
    servings = IntegerField("Servings")
    ingredients = QuerySelectMultipleField('Ingredients',query_factory=lambda: Ingredient.query)
    submit = SubmitField("Create Ingredient")
class IngredientForm(FlaskForm):
    """Form to create an Ingredient"""
    name = StringField("Name",validators=[DataRequired(),Length(max=80)])
    submit = SubmitField("ADD Ingredient")