import json
import os

from flask import render_template, redirect, url_for, session, request, jsonify, flash, current_app

from config import Config
from . import main
from .forms import UserForm
from .. import db
from ..models import Product, Permission, User, Category, Cart, History, CommentPic, Comment, ProductPic, \
    UserProductRank, Role
from ..product.views import generate_safe_pic_name
from ..public_tools import get_user_by_name


@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index():
    """
        The function for rendering the main page
    """
    # logger
    current_app.logger.info("come in /index")

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
    # logger
    current_app.logger.info("come in /user_profile/<username>")

    # query the user object by using the username, which is got from the frontend
    user = get_user_by_name(username)
    return render_template('main/user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    """
    For edit the user profile
    """
    # logger
    current_app.logger.info("come in /edit-profile")

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
    # logger
    current_app.logger.info("come in /products-in-category/<category_name>")

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


@main.route('/my-cart')
def my_cart():
    """
        showing the page of "my shopping cart" of current user
    """
    # logger
    current_app.logger.info("come in /my-cart")

    # if the user has logged in
    if session.get("username"):

        # get the instance of the current user
        current_user = get_user_by_name(session.get("username"))

        # get a list of cart relations of this user (with all the products in his cart)
        cart_relation_list = current_user.cart_relations.all()

        if len(cart_relation_list) < 1:
            # logger
            current_app.logger.warning("in /my-cart - no product found in cart")

        return render_template('main/my_cart.html', user=current_user, cart_relation_list=cart_relation_list)

    # if the user has not logged in
    else:
        return redirect(url_for('auth.login'))


@main.route('/shopping-history')
def shopping_history():
    """
        showing the page of "my shopping history" of current user
    """
    # logger
    current_app.logger.info("come in /shopping-history")

    # if the user has logged in
    if session.get("username"):

        # get the instance of the current user
        current_user = get_user_by_name(session.get("username"))

        # query all the shopping history of this user
        history_list = current_user.history_relations.all()

        if len(history_list) < 1:
            # logger
            current_app.logger.warning("in /shopping-history - no history found")

        return render_template('main/shopping_history.html', user=current_user, history_list=history_list)

    # if the user has not logged in
    else:
        return redirect(url_for('auth.login'))


# ------------------------------ BACK-END Server (using Ajax) ----------------------------------
@main.route('/api/change-theme', methods=['POST'])
def change_theme():
    if request.method == "POST":
        # logger
        current_app.logger.info("post request from ajax /api/change-theme")

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
            # logger
            current_app.logger.error("post request from ajax /api/change-theme - no target theme")
            return jsonify({'returnValue': 1})
    return jsonify({'returnValue': 1})


@main.route('/api/admin-delete-data', methods=['POST'])
def admin_delete_data():
    """
    This function is for administrator to delete the data in database.
    There are 3 types of deletion: products, and all
    We cannot just delete all users and do not delete all products,
    this is because, every product has a retailer user, so that
    if the users gone, products should be deleted as well.
    """
    if request.method == "POST":
        # logger
        current_app.logger.info("post request from ajax /api/admin-delete-data")

        delete_type = request.form["type"]

        print("delete_type")
        print(delete_type)

        # we only accept the type of "all"
        if delete_type == "all":
            # delete all the data in the database
            db.drop_all()
            db.create_all()

            # insert back these two tables
            Role.insert_roles()
            Category.insert_categories()

            # insert the admin users back to the database
            User.insert_only_admin_users()

            return jsonify({'returnValue': 0})

        else:
            # logger
            current_app.logger.error("post request from ajax /api/admin-delete-data - delete type error")
            return jsonify({'returnValue': 1})

    return jsonify({'returnValue': 1})


@main.route('/api/cart/update-product-count', methods=['POST'])
def update_product_count():
    """
        update the product account of a specific cart relation, which is about
        current user and the given product
    """

    if request.method == "POST":
        # logger
        current_app.logger.info("post request from ajax /api/cart/update-product-count")

        product_id = request.form["product_id"]
        new_count = request.form["new_count"]

        # new_count from ajax might be 0
        if new_count != 0:
            # get the instance of current user
            current_user = get_user_by_name(session.get("username"))

            # check if the cart relation already exists
            cart_relation = Cart.query.filter_by(product_id=product_id, user_id=current_user.id).first()

            # if exist
            if cart_relation:
                cart_relation.product_count = new_count
                db.session.commit()
            else:
                # logger
                current_app.logger.error("post request from ajax /api/cart/update-product-count - product in cart is not found")
                return jsonify({'returnValue': 1})

        return jsonify({'returnValue': 0})

    return jsonify({'returnValue': 1})


@main.route('/api/cart/remove-cart-relation', methods=['POST'])
def remove_cart_relation():
    """
        remove a specific cart relation according to the cart_id
    """
    if request.method == "POST":
        # logger
        current_app.logger.info("post request from ajax /api/cart/remove-cart-relation")

        # get the cart_id from ajax
        cart_id = request.form["cart_id"]

        # query the cart relation from database
        cart = Cart.query.get(cart_id)

        if cart:
            # logger
            current_app.logger.warning("post request from ajax /api/cart/remove-cart-relation - a product is being removed from user cart database")

            # remove it from database
            db.session.delete(cart)
            db.session.commit()

        return jsonify({'returnValue': 0})

    # logger
    current_app.logger.error("post request from ajax /api/cart/remove-cart-relation - NOT a POST request")
    return jsonify({'returnValue': 1})


@main.route('/api/cart/purchase', methods=['POST'])
def purchase():
    """
        get a list of id of cart relations that should be purchased.
        we should remove them from database - Cart table and add the records
        into the History table.
    """
    if request.method == "POST":
        # logger
        current_app.logger.info("post request from ajax /api/cart/purchase")

        # get the cart_id_list from ajax
        list_json = request.form["JSON_cart_list"]


        if list_json:
            # unpack json back to list
            cart_id_list = json.loads(list_json)

            # get the instance of current user
            current_user = get_user_by_name(session.get("username"))

            # record these cart relations into History table
            for cart_id in cart_id_list:
                cart = Cart.query.get(cart_id)
                new_history = History(user=current_user, product=cart.product, product_count=cart.product_count)
                db.session.add(new_history)
            db.session.commit()

            # delete those cart relations in Cart table
            for cart_id in cart_id_list:
                cart = Cart.query.get(cart_id)
                db.session.delete(cart)
            db.session.commit()

            return jsonify({'returnValue': 0})

        else:
            # logger
            current_app.logger.error("post request from /api/cart/purchase - JSON transform failed")

            return jsonify({'returnValue': 1})
    return jsonify({'returnValue': 1})




