import os
from app import create_app, db, fake
from app.models import User, Role, Tools, Product, Permission, ProductPic, CommentPic, Comment, ReplyComment
from flask_migrate import Migrate

# create an object of our app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# initialize the Flask-Migrate
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    """
    When using the flask shell command, there is no needs to import db, User, Role...anymore.
    """
    return dict(db=db,
                Tools=Tools,
                fake=fake,
                Permission=Permission,
                User=User,
                Role=Role,
                Product=Product,
                ProductPic=ProductPic,
                CommentPic=CommentPic,
                Comment=Comment,
                ReplyComment=ReplyComment)
