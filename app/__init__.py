"""
    The basic idea of this file is learned from a book called
    'Flask Web Development: Developing Web Applications with Python, Second Edition'
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

# load the extensions we need
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'     # when anonymous users trying to access the protected routes（@login_required），FLask-Login will redirect it to the login page


def create_app(config_name):
    app = Flask(__name__)
    # load the config from the Config class according to the config name
    app.config.from_object(config[config_name])
    # choose the specific config class by using the config_name as the key in the dict
    config[config_name].init_app(app)

    # initialize the extensions we need
    db.init_app(app)
    login_manager.init_app(app)

    # register blueprint - main
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # register blueprint - auth
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # register blueprint - product
    from .product import product as product_blueprint
    app.register_blueprint(product_blueprint)

    # register blueprint - comment
    from .comment import comment as comment_blueprint
    app.register_blueprint(comment_blueprint)

    return app

