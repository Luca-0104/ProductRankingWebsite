from flask import render_template, redirect, url_for
from flask_login import login_required

from . import main
from .. import db


@main.route('/')
@main.route('/index')
def index():

    return render_template('main/index.html')


# for test
@main.route('/secret')
@login_required
def secret():
    return 'nothing here ~'
