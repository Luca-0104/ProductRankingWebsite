import os
from datetime import datetime
import random

from flask import request, url_for, redirect, flash, render_template, session
from flask_login import login_required, current_user
from sqlalchemy import and_
from werkzeug.utils import secure_filename

from app import db
from config import Config
from . import product
from app.product.forms import ProductUploadForm
from ..decorators import permission_required
from ..models import Permission, Product, ProductPic, UserProductRank
from .forms import ProductUploadForm


def generate_safe_pic_name(pic_name):
    """
    To avoid the replicated picture name in our picture repository,
    we append the current date time and a random int into the file name

    :param pic_name: The original picture name
    :return:    A safe picture name contains the datetime of now and a long random integer
    """

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
@login_required
@permission_required(Permission.UPLOAD_PRODUCT)
def upload_product():
    form = ProductUploadForm()

    if form.validate_on_submit():

        """
            store the product object into the database
        """
        product = Product(name=form.name.data,
                          description=form.description.data,
                          price=form.price.data,
                          user_id=current_user.id)

        db.session.add(product)
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
                    flash("Fail to uploaded picture, the suffix should be only 'jpg', 'png', 'gif', 'bmp', 'webp', 'pcx', 'tif', 'jpeg', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo', 'eps', 'al', 'hdri', 'raw', 'wmf', 'flic', 'emf', 'ico', 'avif', 'apng'")

        else:
            flash("No pictures uploaded!")


        return redirect(url_for('main.index'))



    return render_template('product/upload.html', form=form)



@product.route('/remove-product')
@login_required
@permission_required(Permission.REMOVE_PRODUCT)
def remove_product():
    pass


@product.route('/product-details/<int:product_id>')
def product_details(product_id):
    """
    for rendering the template to display the detail information about a specific product
    :param product_id: the id of the selected product that is got from the frontend
    :return:
    """
    product = Product.query.get(product_id)

    '''
        filter out the ranking relation be tween user and product
    '''
    # only the user who has logged in has the ranking relation to the product
    if current_user.is_authenticated:
        pu_relation = current_user.ranked_product_relations.filter(
            and_(UserProductRank.user == current_user, UserProductRank.product == product)).first()
        is_anonymous_user = False

    else:
        # for the anonymous user, we keep the pu_relation as None
        pu_relation = None
        is_anonymous_user = True

    return render_template('product/detail.html', product=product, pu_relation=pu_relation, is_anonymous_user=is_anonymous_user)


@product.route('/edit-product')
@login_required
def edit_product():
    pass


@product.route('/rank/<product_id>-<rank>')
@login_required
@permission_required(Permission.GRADE_STARS)
def rank_product(product_id, rank):

    # cast the rank from str to float, so that it can be calculated
    rank = float(rank)

    # find the product by id
    product = Product.query.get(product_id)

    '''
        record the n to n relationship between user and the product rank
        record the current product is ranked by current user
        ! Also record the rate that this user ranked this product
    '''
    # product.ranked_users.append(current_user)
    pu_relation = UserProductRank(user=current_user, product=product, rank=rank)
    db.session.add(pu_relation)

    '''
        calculate the average rank, 
        (current total rank + this rank) / (current rank times + 1)
    '''
    product.rank = ((product.rank * product.rank_count) + rank) / (product.rank_count + 1)
    product.rank_count += 1

    db.session.add(product)
    db.session.commit()

    flash("Submitted! Thanks for your feedback!")

    return render_template('product/detail.html', product=product, pu_relation=pu_relation, is_anonymous_user=False)





