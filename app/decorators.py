"""
    The main idea of this file is learned from a book called
    'Flask Web Development: Developing Web Applications with Python, Second Edition'
"""

from functools import wraps
from flask import abort, session
from .models import Permission, User
from .public_tools import get_user_by_name

'''
This module is used to define decorators
'''


# learned from the book
def permission_required(permission):
    """
    The decorator of the requirement of the 'permission'
    :param permission: The required permission
    :return: The decorator
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # check if the user logged in
            username = session.get("username")
            if username:
                current_user = get_user_by_name(username)
                # check if the user has the permission
                if not current_user.can(permission):
                    # HTTP deny
                    abort(403)
                return f(*args, **kwargs)
            else:
                # HTTP deny
                abort(403)
        return decorated_function
    return decorator


# copied from this book
def admin_required(f):
    """
    The decorator of the requirement of administration permission
    """
    return permission_required(Permission.ADMIN)(f)

