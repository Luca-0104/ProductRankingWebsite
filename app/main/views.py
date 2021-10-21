from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from . import main
from .. import db, moment
from ..models import Product, Permission, User


@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index():


    if current_user.is_authenticated and current_user.can(Permission.VIEW_ALL_PRODUCT):
        # for users who logged in
        products = Product.query.order_by(Product.release_time.desc()).all()

    else:
        # for anonymous users
        products = Product.query.order_by(Product.release_time.desc()).limit(5)


    return render_template('main/index.html', products=products)


# for test
@main.route('/secret')
@login_required
def secret():
    return 'nothing here ~'


@main.route('/user/<username>')
def user(username):
    """
    For showing the user profile
    :param username: the username the get from the frontend
    """
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('main/user.html', user=user)
