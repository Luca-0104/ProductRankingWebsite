from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from . import main
from .. import db, moment
from ..models import Product, Permission, User, Category


@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index():
    """
        The function for rendering the main page
    """

    if current_user.is_authenticated and current_user.can(Permission.VIEW_ALL_PRODUCT):
        # for users who logged in
        products = Product.query.order_by(Product.rank.desc()).all()

    else:
        # for anonymous users
        products = Product.query.order_by(Product.rank.desc()).limit(4)


    return render_template('main/index.html', products=products)


# for test
@main.route('/secret')
@login_required
def secret():
    return 'nothing here ~'


@main.route('/user_profile/<username>')
def user_profile(username):
    """
    For showing the user profile
    :param username: the username the get from the frontend
    """
    # query the user object by using the username, which is got from the frontend
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('main/user.html', user=user)


@main.route('/products-in-category/<category_name>')
@login_required
def products_in_category(category_name):
    """
    For showing the products in a specific category
    :param category_name:   the name of the category we will show
    """
    # find out the category object by using the category_name
    category = Category.query.filter_by(name=category_name).first()
    # find the products that are under this category
    products = category.products
    return render_template('main/category_products.html', products=products)

