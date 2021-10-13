from flask import render_template, redirect, url_for
from . import main
from .. import db


@main.route('/')
@main.route('/index')
def index():

    return render_template('main/index.html')
