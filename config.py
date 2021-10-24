"""
    The basic idea of this file is learned from a book called
    'Flask Web Development: Developing Web Applications with Python, Second Edition'
"""

import os

# The directory of this project
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'no one will guess'  # a secret key for the wtf forms
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # The allowed suffixes type of the picture that is uploaded
    ALLOWED_PIC_SUFFIXES = ['jpg', 'png', 'gif', 'bmp', 'webp', 'pcx', 'tif', 'jpeg', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo', 'eps', 'al', 'hdri', 'raw', 'wmf', 'flic', 'emf', 'ico', 'avif', 'apng']

    """ Following define the directories used in this project """
    app_dir = os.path.join(basedir, 'app')
    static_dir = os.path.join(app_dir, 'static')
    upload_dir = os.path.join(static_dir, 'upload')
    product_dir = os.path.join(upload_dir, 'product')       # The directory for storing the photos of products in this website
    comment_dir = os.path.join(upload_dir, 'comment')       # The directory for storing the photos of the comments of products in this website
    avatar_dir = os.path.join(upload_dir, 'avatar')         # The directory for storing the avatars of users


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

