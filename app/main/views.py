import os

from flask import render_template, redirect, url_for, session, request, jsonify, flash

from config import Config
from . import main
from .forms import UserForm
from .. import db
from ..models import Product, Permission, Category
from ..product.views import generate_safe_pic_name
from ..public_tools import get_user_by_name


@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index():
    """
        The function for rendering the main page
    """
    # check if the user logged in
    if session.get("username"):
        print(session.get("username"))
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


@main.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    """
    For edit the user profile
    """

    current_user = get_user_by_name(session.get("username"))
    form = UserForm(username=current_user.username, email=current_user.email)

    # when the form is submitted legally (POST method)
    if form.validate_on_submit():
        # get the current username

        # user = User.query.filter(User.username == current_user).first()

        # get a list of file objects from the user upload
        pic = form.pictures.data
        print(pic)
        if pic.filename != "":

            # get the name of the picture
            pic_name = pic.filename
            pic_name_origin = pic_name
            # get the suffix of the picture
            suffix = pic_name.rsplit('.')[-1]

            if suffix in Config.ALLOWED_PIC_SUFFIXES:

                path = 'upload/avatar'

                # make sure the name of picture is safe
                pic_name = generate_safe_pic_name(pic_name)

                """
                save the picture in the local directory
                """
                # get the path to store the picture (dir + pic_name)
                file_path = os.path.join(Config.avatar_dir, pic_name).replace('\\', '/')

                # save the picture
                pic.save(file_path)

                """
                   save the picture in the database
                """
                pic_address = os.path.join(path, pic_name).replace('\\', '/')
                current_user.avatar = pic_address

                current_user.username = form.username.data
                current_user.email = form.email.data

                db.session.commit()

                flash('Picture "' + pic_name_origin + '" uploaded successfully!')

            else:
                flash(
                    "Fail to uploaded picture, the suffix should be only 'jpg', 'png', 'gif', 'bmp', 'webp', 'pcx', 'tif', 'jpeg', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo', 'eps', 'al', 'hdri', 'raw', 'wmf', 'flic', 'emf', 'ico', 'avif', 'apng'")

        else:
            flash("No pictures uploaded!")
        flash("Changed Successfully!")
        session['username'] = form.username.data

        return redirect(url_for('main.user_profile', username=form.username.data))

    # (GET method)
    return render_template('main/user_edit.html', form=form)


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
