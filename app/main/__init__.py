from flask import Blueprint

from ..models import Permission

# Create a Blueprint class object called main, set the blueprint name as 'main'
main = Blueprint('main', __name__)

from . import views


@main.app_context_processor
def inject_permissions():
    """
        put the 'Permission' class into the template context
        so that we can access the constants in Permission class in the templates

    :return: A dict of parameters that should be added to the template context
    """
    return dict(Permission=Permission)
