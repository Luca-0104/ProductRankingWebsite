import os

from flask import session, redirect, url_for, flash, render_template, current_app
from sqlalchemy import and_

from app import db
from app.comment import comment
from app.comment.forms import CommentForm
from app.decorators import permission_required
from app.models import Permission, Comment, CommentPic, Product, UserProductRank
from app.product.views import generate_safe_pic_name
from app.public_tools import get_user_by_name
from config import Config


@comment.route('/upload-comment/<int:product_id>', methods=['GET', 'POST'])
@permission_required(Permission.COMMENT)
def upload_comment(product_id):
    """
    function for a user to comment a product
    :param product_id: the id of the product
    """
    # logger
    current_app.logger.info("come in /upload-comment/<int:product_id>")

    form = CommentForm()

    # check if the user logged in
    if session.get("username"):
        # get the instance of the current user
        current_user = get_user_by_name(session.get("username"))
        # get the instance of the current product, which is being commented
        current_product = Product.query.get(product_id)

        if form.validate_on_submit():
            # filter out the rating relation be tween user and product
            pu_relation = UserProductRank.query.filter(
                and_(UserProductRank.user == current_user, UserProductRank.product == current_product)).first()

            # if no rating relation
            if pu_relation is None:
                star_num = -1   # default is -1, which means does not rate this product yet

            # if there is a rating relation
            else:
                # query the star number this user have given to this product
                star_num = int(pu_relation.rank)

            # create a new comment and add it into the database
            new_comment = Comment(content=form.text.data, product_id=product_id, auth_id=current_user.id, star_num=star_num)
            db.session.add(new_comment)
            db.session.commit()

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
                        path = 'upload/comment'

                        # make sure the name of picture is safe
                        pic_name = generate_safe_pic_name(pic_name)

                        """
                            save the picture in the local directory
                        """
                        # get the path to store the picture (dir + pic_name)
                        file_path = os.path.join(Config.comment_dir, pic_name).replace('\\', '/')

                        # save the picture
                        pic.save(file_path)

                        """
                            save the picture in the database
                        """
                        pic_address = os.path.join(path, pic_name).replace('\\', '/')
                        pic_object = CommentPic(address=pic_address, comment_id=new_comment.id)

                        db.session.add(pic_object)
                        db.session.commit()

                        flash('Picture "' + pic_name_origin + '" uploaded successfully!')

                    else:
                        flash(
                            "Fail to uploaded picture, the suffix should be only 'jpg', 'png', 'gif', 'bmp', 'webp', 'pcx', 'tif', 'jpeg', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo', 'eps', 'al', 'hdri', 'raw', 'wmf', 'flic', 'emf', 'ico', 'avif', 'apng'")

            else:
                flash("No pictures uploaded!")

            return redirect(url_for('main.index'))

        return render_template('comment/upload.html', form=form, product=current_product)


    # for the anonymous users
    else:
        return redirect(url_for('auth.login'))


# @comment.route('/view-all-comments')
# @permission_required(Permission.VIEW_ALL_COMMENTS)
# def view_all():
#     pass
#
#
# @comment.route('/comment-detail')
# def view_detail():
#     pass
#
#
# @comment.route('/reply-comment', methods=['GET', 'POST'])
# def reply_comment():
#     pass
