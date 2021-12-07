from app.models import User


def get_user_by_name(username):
    """
    This function is used to get a user object by their username
    :param username: the username of the user
    :return: a user object
    """
    return User.query.filter_by(username=username).first()


def get_user_by_id(uid):
    """
    This function is used to get a user object by their id
    :param uid: the id of the user
    :return: a user object
    """
    return User.query.get(uid)
