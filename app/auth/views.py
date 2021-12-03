from flask import request, url_for, redirect, flash, render_template, session
from flask_login import login_user, login_required, logout_user

from app import db
from . import auth
from app.auth.forms import LoginForm, RegisterForm
from app.models import User


@auth.route('/logout')
@login_required
def logout():
    """
    The function to log the user out
    :return: redirect back to the home page
    """
    logout_user()
    flash('You have been logged out')
    return redirect(url_for("main.index"))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    # when the form is submitted legally (POST method)
    if form.validate_on_submit():

        # create a new user object
        user = User(email=form.email.data, username=form.username.data, password=form.password1.data, role_id=int(form.role.data))
        db.session.add(user)
        db.session.commit()
        flash("Register Successfully! You can go for login now!")

        return redirect(url_for('auth.login'))

    # (GET method)
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # when the form is submitted legally (POST method)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            # call the login_user function in the Flask-Login extension to mark the user as logged in the session
            login_user(user, form.remember_me.data)

            # get the original url that the user was browsing before login
            next = request.args.get('next')
            # ensure the relative url, avoiding the malicious redirection
            if next is None or not next.startswith('/'):
                next = url_for('main.index')

                # session["username"] = ""

            # redirect back to the original url or the index page
            return redirect(next)

        # if we get here, this means the user give the wrong data and login failed
        flash("Login Failed! Check your username or password.")

    # (GET method)
    return render_template('auth/login.html', form=form)
