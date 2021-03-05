import os
import unittest

from recipe_app import app, db, bcrypt
from recipe_app.models import User, Recipe, Ingredient, recipe_ingredient_association
from flask_login import current_user


def login(client, username, password):
    """logs in a user for testing"""
    data = {
        'username':username,
        'password':password
    }
    return client.post('/login', data=data, follow_redirects=True)

def logout(client):
    """Logs out a user for testing"""
    return client.get("/logout", follow_redirects=True)

def create_user():
    """Creates a test user"""

    password = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='shaun', password=password)
    db.session.add(user)
    db.session.commit()

def create_recipe():
    """Creates two test recipes with ingredients"""
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

    def test_homepage_signed_in(self):
        '''Test that recipes and ingredients are shown on homepage  '''
        create_recipe()
        create_user()
        login(self.app,'shaun', 'password')

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        response_data = response.get_data(as_text=True)

        self.assertIn('ThanksGiving',response_data)
        self.assertIn('Tea',response_data)
        self.assertIn('honey',response_data)
        self.assertIn('turkey',response_data)
        self.assertIn('teabags',response_data)

        self.assertIn('Logout',response_data)
        self.assertIn('Create Recipe',response_data)

        self.assertNotIn('Signup',response_data)

    def test_homepage_signed_out(self):
        """Test that signout and create recipe are not present and sign in is"""
        create_recipe()
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        response_data = response.get_data(as_text=True)

        self.assertIn('ThanksGiving',response_data)
        self.assertIn('Tea',response_data)
        self.assertIn('honey',response_data)
        self.assertIn('turkey',response_data)
        self.assertIn('teabags',response_data)

        self.assertIn('Signup', response_data)
        self.assertIn("Login", response_data)

        self.assertNotIn('Logout',response_data)
        self.assertNotIn('Create Recipe',response_data)

    def test_recipe_route(self):
        """Test Recipe Name and all ingredients appear"""
        create_recipe()

        response = self.app.get("/recipe/1")
        self.assertEqual(response.status_code, 200)

        response_txt = response.get_data(as_text=True)

        self.assertIn('ThanksGiving', response_txt)
        self.assertIn('turkey', response_txt)
        self.assertIn('ham', response_txt)
        self.assertIn('potatoes', response_txt)



        self.assertNotIn('teabags',response_txt)

    def test_ingredient_route(self):
        """Test both recipes appear when viewing water"""
        create_recipe()
        i = Ingredient.query.filter_by(name='water').first()
        id = i.id

        response = self.app.get(f'/ingredient/{id}')
        self.assertEqual(response.status_code, 200)

        response_txt = response.get_data(as_text=True)
        
        self.assertIn('water' , response_txt)
        self.assertIn('Tea' , response_txt)
        self.assertIn('ThanksGiving' , response_txt)


        self.assertNotIn("turkey", response_txt)


    def test_userprofile(self):
        """Test Profile Route Shows recipes that have been favorited"""
        create_recipe()
        create_user()
        login(self.app, 'shaun','password')
        new_fav = Recipe.query.get(1)
        user = User.query.get(1)
        user.favorite_recipes.append(new_fav)
        db.session.commit()
        
        response = self.app.get(f'/profile')
        self.assertEqual(response.status_code, 200)

        response_txt = response.get_data(as_text=True)

        self.assertIn('shaun',response_txt)
        self.assertIn('ThanksGiving',response_txt)

        self.assertNotIn("Tea", response_txt)

