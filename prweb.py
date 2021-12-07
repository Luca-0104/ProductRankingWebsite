import os

from flask import session

from app import create_app, db
from app.models import User, Role, Tools, Product, Permission, ProductPic, CommentPic, Comment, ReplyComment, Category, \
    UserProductRank

# create an object of our app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    """
    When using the flask shell command, there is no needs to import db, User, Role...anymore.
    """
    return dict(db=db,
                Tools=Tools,
                Permission=Permission,
                User=User,
                Role=Role,
                Product=Product,
                ProductPic=ProductPic,
                CommentPic=CommentPic,
                Comment=Comment,
                ReplyComment=ReplyComment,
                Category=Category,
                UserProductRank=UserProductRank)
