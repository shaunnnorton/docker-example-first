from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from recipe_app.models import User

class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),Length(min=3,max=80)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8)])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username Not Avalible")


class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Log In")