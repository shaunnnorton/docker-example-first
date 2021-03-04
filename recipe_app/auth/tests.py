import os
import unittest

from recipe_app import app, db, bcrypt
from recipe_app.models import User, Recipe, Ingredient, recipe_ingredient_association
from flask_login import current_user


def login(client, username, password):
    data = {
        'username':username,
        'password':password
    }
    return client.post('/login', data=data, follow_redirects=True)

def logout(client):
    return client.get("/logout", follow_redirects=True)

def create_user():
    password = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='shaun', password=password)
    db.session.add(user)
    db.session.commit()

def create_recipe():
    h2o = Ingredient(name='water')
    ingredients = [Ingredient(name='turkey'),Ingredient(name='ham'),Ingredient(name='potatoes'), h2o]
    r1 = Recipe(
        title='ThanksGiving'
    )
    for i in ingredients:
        new_association = recipe_ingredient_association(amount=10,ingredient=i)
        r1.ingredients.append(new_association)


    ingredients = [Ingredient(name='teabags'),Ingredient(name='honey'), h2o]
    r2 = Recipe(
        title='Tea'
    )
    for i in ingredients:
        new_association = recipe_ingredient_association(amount=10,ingredient=i)
        r2.ingredients.append(new_association)

    db.session.add(r1)
    db.session.add(r2)
    db.session.commit()


class Tests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['DATABASE_URL'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()


    def test_login(self):
        """Test Login Route"""
        create_user()

        response = self.app.post('login',data={'username':'shaun','password':'password'},follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_txt = response.get_data(as_text=True)

        self.assertIn("Logout",response_txt)

    def test_login_user_None(self):
        """Test Login Route When User dosent exist"""
        create_user()

        response = self.app.post('login',data={'username':'tutle','password':'password'},follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_txt = response.get_data(as_text=True)

        self.assertIn("Login",response_txt)


    def test_signup(self):
        """Test signup route"""
        user_info = {
            'username': 'username',
            'password':'password'
        }
        response = self.app.post('/signup',data=user_info)

        user_check = User.query.filter_by(username='username').first()
        self.assertIsNotNone(user_check)