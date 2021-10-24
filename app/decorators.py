"""
    The main idea of this file is learned from a book called
    'Flask Web Development: Developing Web Applications with Python, Second Edition'
"""

from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission

'''
This module is used to define decorators
'''


# copied from this book
def permission_required(permission):
    """
    The decorator of the requirement of the 'permission'
    :param permission: The required permission
    :return: The decorator
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                # HTTP deny
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# copied from this book
def admin_required(f):
    """
    The decorator of the requirement of administration permission
    """
    return permission_required(Permission.ADMIN)(f)

