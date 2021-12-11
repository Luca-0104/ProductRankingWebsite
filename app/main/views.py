from flask import render_template, redirect, url_for, session, request, jsonify

from . import main
from .. import db
from ..models import Product, Permission, User, Category
from ..public_tools import get_user_by_name


@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index():
    """
        The function for rendering the main page
    """
    # check if the user logged in
    if session.get("username"):
        current_user = get_user_by_name(session.get("username"))
        if current_user.can(Permission.VIEW_ALL_PRODUCT):
            # for users who logged in
            products = Product.query.order_by(Product.rank.desc()).all()
        else:
            # for users do not have the permission
            products = Product.query.order_by(Product.rank.desc()).limit(4)
    else:
        # for anonymous users
        products = Product.query.order_by(Product.rank.desc()).limit(4)

    return render_template('main/index.html', products=products)


@main.route('/user_profile/<username>')
def user_profile(username):
    """
    For showing the user profile
    :param username: the username the get from the frontend
    """
    # query the user object by using the username, which is got from the frontend
    user = get_user_by_name(username)
    return render_template('main/user.html', user=user)


@main.route('/products-in-category/<category_name>')
def products_in_category(category_name):
    """
    For showing the products in a specific category
    :param category_name:   the name of the category we will show
    """
    # if the user has logged in
    if session.get("username"):
        # find out the category object by using the category_name
        category = Category.query.filter_by(name=category_name).first()
        # find the products that are under this category
        products = category.products
        return render_template('main/category_products.html', products=products)

    # if the user has not logged in
    else:
        return redirect(url_for('auth.login'))


# ------------------------------ BACK-END Server (using Ajax) ----------------------------------
@main.route('/api/change-theme', methods=['POST'])
def change_theme():
    if request.method == "POST":
        # get the target them from the request
        target_theme = request.form["target_theme"]

        # if the target theme is gotten
        if target_theme:
            # if the user has logged in, we change the theme of this user in database and session
            if session.get("username"):
                # get the user instance
                current_user = get_user_by_name(session.get("username"))

                # update the theme in database
                current_user.theme = target_theme
                db.session.commit()
                # update the them in session
                session["theme"] = target_theme

            # if the user not logged in, we change the theme in the session
            else:
                # update the them in session
                session["theme"] = target_theme

            return jsonify({'returnValue': 0})

        else:
            return jsonify({'returnValue': 1})
    return jsonify({'returnValue': 1})

