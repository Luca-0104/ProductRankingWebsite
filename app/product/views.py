import os
from datetime import datetime
import random

from flask import request, url_for, redirect, flash, render_template, session, jsonify, current_app
from sqlalchemy import and_
from werkzeug.utils import secure_filename

from app import db
from config import Config
from . import product
from app.product.forms import ProductUploadForm
from ..auth.forms import LoginForm
from ..decorators import permission_required
from ..models import Permission, Product, ProductPic, UserProductRank, User, Category, Comment, Cart
from .forms import ProductUploadForm
from ..public_tools import get_user_by_name


def generate_safe_pic_name(pic_name):
    """
    To avoid the replicated picture name in our picture repository,
    we append the current date time and a random int into the file name

    :param pic_name: The original picture name
    :return:    A safe picture name contains the datetime of now and a long random integer
    """
    # logger
    current_app.logger.info("a new picture is uploaded with save name")

    # due to ':' and space cannot be contained in the picture name, we replace them with '.' and '_'
    datetime_suffix = str(datetime.utcnow()).replace(" ", "_").replace(":", ".")

    # get a random int
    random_num_suffix = random.randint(0, 9999999999)

    # call the secure_filename function in the werkzeug, this can make the filename safe (for example, replace the blank space with '_', and so on)
    pic_name = secure_filename(pic_name)

    # append the datetime and random int into the pic_name, at the end but before the suffix (.png, .jpg ...)
    pic_name = pic_name[:pic_name.rfind(".")] + '_' + str(
        random_num_suffix) + '_' + datetime_suffix + pic_name[pic_name.rfind("."):]

    return pic_name


@product.route('/upload-product', methods=['GET', 'POST'])
def upload_product():
    # logger
    current_app.logger.info("come into /upload-product")

    form = ProductUploadForm()

    # check if the user logged in
    if session.get("username"):

        current_user = get_user_by_name(session.get("username"))

        # get all the categories from database
        all_cate_list = Category.query.all()

        if form.validate_on_submit():

            # get a list of categories of this product
            cate_lst = request.values.getlist('categories[]')

            """
                store the product object into the database
            """
            product = Product(name=form.name.data,
                              description=form.description.data,
                              price=form.price.data,
                              user_id=current_user.id)

            db.session.add(product)
            db.session.commit()

            # append the selected categories to this product
            for cate_id in cate_lst:
                product.categories.append(Category.query.get(cate_id))

            # if no selected categories, we will give it a default one -- "others"
            if len(cate_lst) == 0:
                product.categories.append(Category.query.get(12))

            db.session.commit()

            flash("Product uploaded successfully!")

            """
                dealing with the uploaded pictures
            """

            # get a list of file objects from the user upload
            picture_list = form.pictures.data

            # check if there are pictures uploaded
            if len(picture_list) > 0 and picture_list[0].filename != "":

                # loop through the list getting and storing each picture
                for pic in picture_list:

                    # get the name of the picture
                    pic_name = pic.filename
                    pic_name_origin = pic_name
                    # get the suffix of the picture
                    suffix = pic_name.rsplit('.')[-1]

                    if suffix in Config.ALLOWED_PIC_SUFFIXES:
                        path = 'upload/product'

                        # make sure the name of picture is safe
                        pic_name = generate_safe_pic_name(pic_name)

                        """
                            save the picture in the local directory
                        """
                        # get the path to store the picture (dir + pic_name)
                        file_path = os.path.join(Config.product_dir, pic_name).replace('\\', '/')

                        # save the picture
                        pic.save(file_path)

                        """
                            save the picture in the database
                        """
                        pic_address = os.path.join(path, pic_name).replace('\\', '/')
                        pic_object = ProductPic(address=pic_address, product_id=product.id)

                        db.session.add(pic_object)
                        db.session.commit()

                        flash('Picture "' + pic_name_origin + '" uploaded successfully!')

                    else:
                        flash(
                            "Fail to uploaded picture, the suffix should be only 'jpg', 'png', 'gif', 'bmp', 'webp', 'pcx', 'tif', 'jpeg', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo', 'eps', 'al', 'hdri', 'raw', 'wmf', 'flic', 'emf', 'ico', 'avif', 'apng'")

            else:
                flash("No pictures uploaded!")

            return redirect(url_for('main.index'))

        return render_template('product/upload.html', form=form, allCategories=all_cate_list)

    # for the anonymous users
    else:
        return redirect(url_for('auth.login'))


@product.route('/remove-product')
def remove_product():
    pass


@product.route('/product-details/<int:product_id>')
def product_details(product_id):
    """
    for rendering the template to display the detail information about a specific product
    :param product_id: the id of the selected product that is got from the frontend
    :return:
    """
    # logger
    current_app.logger.info("come into /product-details/<int:product_id>")

    # get the product by id
    product = Product.query.get(product_id)

    # only the user who has logged in has the ranking relation to the product
    if session.get("username"):
        # get the user object
        current_user = get_user_by_name(session.get("username"))

        # filter out the rating relation be tween user and product
        pu_relation = current_user.ranked_product_relations.filter(
            and_(UserProductRank.user == current_user, UserProductRank.product == product)).first()
        is_anonymous_user = False

    else:
        # for the anonymous user, we keep the pu_relation as None
        pu_relation = None
        is_anonymous_user = True

    return render_template('product/detail.html', product=product, pu_relation=pu_relation,
                           is_anonymous_user=is_anonymous_user, is_in_product_detail=True)


@product.route('/edit-product')
def edit_product():
    pass


@product.route('/rank/<product_id>-<rank>')
def rank_product(product_id, rank):
    """ This route is Abandoned """
    # logger
    current_app.logger.error("come into /rank/<product_id>-<rank>, this has been abandoned, this should be done with ajax")

    # check if the user logged in
    if session.get("username"):
        # get the user object
        current_user = get_user_by_name(session.get("username"))

        # cast the rank from str to float, so that it can be calculated
        rank = float(rank)

        # find the product by id
        product = Product.query.get(product_id)

        '''
            record the n to n relationship between user and the product rank
            record the current product is ranked by current user
            ! Also record the rate that this user ranked this product
        '''
        pu_relation = UserProductRank(user=current_user, product=product, rank=rank)
        db.session.add(pu_relation)

        '''
            calculate the average rate, 
            (current total rate + this rate) / (current rate times + 1)
        '''
        product.rank = ((product.rank * product.rank_count) + rank) / (product.rank_count + 1)
        product.rank_count += 1

        db.session.add(product)
        db.session.commit()

        flash("Submitted! Thanks for your feedback!")

        return render_template('product/detail.html', product=product, pu_relation=pu_relation, is_anonymous_user=False)


    # for the anonymous users
    else:
        return redirect(url_for('auth.login'))


# ------------------------------ BACK-END Server (using Ajax) ----------------------------------
@product.route('/api/product/stars', methods=['POST'])
def get_stars():
    # get the star number from the db
    # return the star number of specific product

    if request.method == "POST":
        # logger
        current_app.logger.info("post request from ajax /api/product/stars")

        product_id = request.form["product_id"]
        product = Product.query.get(product_id)

        if product:
            current_user = get_user_by_name(session.get("username"))
            # filter out the ranking relation be tween user and product
            pu_relation = current_user.ranked_product_relations.filter(
                and_(UserProductRank.user == current_user, UserProductRank.product == product)).first()
            return jsonify({'returnValue': 0, "star_num": pu_relation.rank})

        else:
            # logger
            current_app.logger.error("post request from ajax /api/product/stars - product not found")
            return jsonify({'returnValue': 1})
    return jsonify({'returnValue': 1})


@product.route('/api/product/stars/rate', methods=['POST'])
def rate_product():
    # get the product id and start id from request
    # rate the product for user logged in
    # return returnValue 0 in json format if successful.

    if request.method == "POST":
        # logger
        current_app.logger.info("post request from ajax /api/product/stars/rate")

        product_id = request.form["product_id"]
        star_id = request.form["star_id"]

        if product_id and star_id:

            # check if the user logged in
            if session.get("username"):
                # get the user object
                current_user = get_user_by_name(session.get("username"))

                # convert star id to according number (rate)
                if star_id == "star1":
                    rate = 1
                elif star_id == "star2":
                    rate = 2
                elif star_id == "star3":
                    rate = 3
                elif star_id == "star4":
                    rate = 4
                elif star_id == "star5":
                    rate = 5
                else:
                    return jsonify({'returnValue': 1})

                # cast the rate from str to float, so that it can be calculated
                rate = float(rate)

                # find the product by id
                product = Product.query.get(product_id)

                '''
                    record the n to n relationship between user and the product rank
                    record the current product is ranked by current user
                    ! Also record the rate that this user ranked this product
                '''
                pu_relation = UserProductRank(user=current_user, product=product, rank=rate)
                db.session.add(pu_relation)

                '''
                    calculate the average rank, 
                    (current total rank + this rank) / (current rank times + 1)
                '''
                product.rank = ((product.rank * product.rank_count) + rate) / (product.rank_count + 1)
                product.rank_count += 1

                db.session.add(product)
                db.session.commit()

                '''
                    If there exist the comment of this user with this product, 
                    we have to update the star_num this this comment
                '''
                comment = Comment.query.filter(and_(Comment.author == current_user, Comment.product == product)).first()
                if comment:
                    comment.star_num = int(rate)
                    db.session.add(comment)
                    db.session.commit()
                else:
                    # logger
                    current_app.logger.error("no such comment")

                flash("Submitted! Thanks for your feedback!")

                return jsonify({'returnValue': 0})


            # for the anonymous users
            else:
                print("user not log in")
                # logger
                current_app.logger.warning("user not log in")

                return redirect(url_for('auth.login'))
                # return redirect(url_for('product.upload_product'))

        else:
            # logger
            current_app.logger.error("post request from ajax /api/product/stars/rate - no product id or star id")
            return jsonify({'returnValue': 1})
    return jsonify({'returnValue': 1})


@product.route('/api/product/add-to-cart', methods=['POST'])
def add_to_cart():
    """
        add the product into the user shopping cart
    """
    if request.method == "POST":
        # logger
        current_app.logger.info("post request from ajax /api/product/add-to-cart")

        # get the product_id and "how many to add" from ajax
        product_id = request.form["product_id"]
        product_count = int(request.form["product_count"])

        p = Product.query.get(product_id)
        # check if the input is acceptable
        if p is not None and (product_count > 0):
            # get current user instance (if the user has not logged in, he should be redirect to the login page (in frontend))
            current_user = get_user_by_name(session.get("username"))

            # check if the cart relation already exists
            cart_relation = Cart.query.filter_by(product_id=product_id, user_id=current_user.id).first()

            if cart_relation:
                cart_relation.product_count += product_count
                db.session.commit()
            else:
                # create a new cart relation between this user and product
                new_cart = Cart(product_id=product_id, user_id=current_user.id, product_count=product_count)
                db.session.add(new_cart)
                db.session.commit()

            return jsonify({'returnValue': 0})
        else:
            # logger
            current_app.logger.warning("post request from ajax /api/product/add-to-cart - input is not acceptable")
            return jsonify({'returnValue': 1})
    else:
        return jsonify({'returnValue': 1})

