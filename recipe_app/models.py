from recipe_app import db
from sqlalchemy.orm import backref
from sqlalchemy import String, Column, Text, Table, ForeignKey
from flask_login import UserMixin
import enum


class User(db.Model,UserMixin):
    """User Model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    favorite_recipes = db.relationship('Recipe',secondary='user_recipe',back_populates='favorites')


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text())
    servings = db.Column(db.Integer)
    instructions = db.Column(db.Text())
    ingredients = db.relationship('recipe_ingredient_association',back_populates='recipe')
    favorites = db.relationship("User",secondary="user_recipe", back_populates='favorite_recipes')
    image = db.Column(db.String(200), nullable=True)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    recipes = db.relationship('recipe_ingredient_association',back_populates='ingredient')
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

class recipe_ingredient_association(db.Model):
    __tablename__ = 'recipe_ingredient_association'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    recipe = db.relationship('Recipe',back_populates="ingredients")
    ingredient = db.relationship('Ingredient',back_populates='recipes')
    amount = db.Column(db.String(40))


user_recipe_table = db.Table('user_recipe',
    db.Column('user_id',db.Integer, db.ForeignKey('user.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
)

# recipe_ingredient_table = db.Table('recipe_ingredient',
#     db.Column('recipe_id',db.Integer, db.ForeignKey('recipe.id')),
#     db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'))
# )