import os
from datetime import datetime
import random

from flask import request, url_for, redirect, flash, render_template
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app import db
from config import Config
from . import product
from app.product.forms import ProductUploadForm
from ..decorators import permission_required
from ..models import Permission, Product, ProductPic
from .forms import ProductUploadForm


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

        # loop through the list getting and storing each picture
        for pic in picture_list:

            # get the name of the picture
            pic_name = pic.filename
            pic_name_origin = pic_name
            # get the suffix of the picture
            suffix = pic_name.rsplit('.')[-1]

            if suffix in Config.ALLOWED_PIC_SUFFIXES:
                path = 'upload/product'

                """
                    to avoid the replicated picture name in our web, we append the current date time and a random int into the file name
                """
                # due to ':' and space cannot be contained in the picture name, we replace them with '.' and '_'
                datetime_suffix = str(datetime.utcnow()).replace(" ", "_").replace(":", ".")

                # get a random int
                random_num_suffix = random.randint(0, 9999999999)

                # call the secure_filename function in the werkzeug, this can make the filename safe (for example, replace the blank space with '_', and so on)
                pic_name = secure_filename(pic_name)

                # append the datetime and random int into the pic_name, at the end but before the suffix (.png, .jpg ...)
                pic_name = pic_name[:pic_name.rfind(".")] + '_' + str(random_num_suffix) + '_' + datetime_suffix + pic_name[pic_name.rfind("."):]

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

        return redirect(url_for('main.index'))



    return render_template('product/upload.html', form=form)



@product.route('/remove-product')
@login_required
@permission_required(Permission.REMOVE_PRODUCT)
def remove_product():
    pass


@product.route('/product-details/<product_id>')
def product_details(product_id):
    pass


@product.route('/edit-product')
@login_required
def edit_product():
    pass





