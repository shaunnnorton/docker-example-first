from flask import Blueprint, request, render_template, redirect, url_for, flash
from recipe_app.auth.forms import LoginForm, SignUpForm
from recipe_app.models import User
from flask_login import login_user, logout_user


from recipe_app import db, bcrypt


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', "POST"])
def login():
    """Route for loggging in a user"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            print(next_page)
            return redirect(next_page if next_page else '/')

    return render_template('login.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """Creates a new User Model provided informaiton from the signup form"""
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('You Created Your Account!')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)


@auth.route('/logout')
def logout():
    """Signs out the current user."""
    logout_user()
    return redirect('/')
