from recipe_app import db
from sqlalchemy.orm import backref
from sqlalchemy import String, Column, Text, Table, ForeignKey
import enum


class User(db.Model):
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
    ingredients = db.relationship("Ingredient", secondary='recipe_ingredient',back_populates='recipes')
    favorites = db.relationship("User",secondary="user_recipe", back_populates='favorite_recipes')


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    recipes = db.relationship('Recipe',secondary='recipe_ingredient',back_populates='ingredients')
    def __repr__(self):
        return self.name
user_recipe_table = db.Table('user_recipe',
    db.Column('user_id',db.Integer, db.ForeignKey('user.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
)

recipe_ingredient_table = db.Table('recipe_ingredient',
    db.Column('recipe_id',db.Integer, db.ForeignKey('recipe.id')),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'))
)