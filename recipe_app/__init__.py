from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from recipe_app.config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)


from recipe_app.main.routes import main as main_routes
app.register_blueprint(main_routes)



with app.app_context():
    db.create_all()
