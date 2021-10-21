from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin

from app import db, login_manager
from app.tableInfo import user_list


@login_manager.user_loader
def load_user(user_id):
    """
        Flask-Login extension required this
    """
    return User.query.get(int(user_id))


class Tools:
    """
    All the tool methods for creating the tables
    """

    @staticmethod
    def update_db():
        db.drop_all()
        db.create_all()
        Tools.fill_all_tables()

    @staticmethod
    def fill_all_tables():
        """
        Fill all the tables in an specific order.
        This should be used in the console only a single time.
        """
        Role.insert_roles()
        User.insert_users()


class Permission:
    """
    Using integers to represent different permissions
    all the number are 2^n
    so that the sum of a group of permission numbers
    can represent a sole group of permissions.
    This means when we get a sum number, we can know which permissions the user owns.
    """
    UPLOAD_PRODUCT = 1
    VIEW_ALL_PRODUCT = 2
    GRADE_STARS = 4
    COMMENT = 8
    VIEW_ALL_COMMENTS = 16
    ADMIN = 32
    REMOVE_PRODUCT = 64


class ReplyComment(db.Model):
    """
    a table for storing the replies of the comments of products
    """
    __tablename__ = 'comment_replies'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)    # 1 comment --> n replies
    auth_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)          # 1 user --> n replies
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<ReplyComment %r>' % self.content[:10]


class Comment(db.Model):
    """
    a table for storing the comments of products
    """
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    pictures = db.relationship('CommentPic', backref='comment', lazy='dynamic')         # 1 comment --> n pictures
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)    # 1 product --> n comment
    auth_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)          # 1 user --> n comment
    replies = db.relationship('ReplyComment', backref='comment')                        # 1 comment --> n replies
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Comment %r>' % self.content[:10]



class CommentPic(db.Model):
    """
    a table for storing all the pictures of the comments of the products
    """
    __tablename__ = 'comment_pictures'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(256), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))    # 1 comment --> n picture

    def __repr__(self):
        return '<CommentPic %r>' % self.address


class ProductPic(db.Model):
    """
    a table for storing all the pictures related to the products
    """
    __tablename__ = 'product_pictures'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(256), default='upload/product/default.png')
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))    # 1 product --> n picture

    def __repr__(self):
        return '<ProductPic %r>' % self.address


class Product(db.Model):
    """
    a table for storing all the products in our website
    """
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text())
    price = db.Column(db.Float)
    release_time = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    pictures = db.relationship('ProductPic', backref='product', lazy='dynamic')  # 1 product --> n pictures
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))                   # 1 user --> n products
    comments = db.relationship('Comment', backref='product', lazy='dynamic')     # 1 product --> n comments
    rank = db.Column(db.Float, default=0)         # the stars rank, 0 - 5
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Product %r>' % self.name[:20]


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)  # we will set the 'customer' as default role
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')     # 1 role --> n users

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        # initialize the permissions
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return '<Role %r>' % self.name

    # ----- functions for permission management -----
    def has_permission(self, perm):
        return self.permissions & perm == perm

    def reset_permission(self):
        self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    @staticmethod
    def insert_roles():
        """
            a static method for creating the roles into the db (use this in the flask shell!!)
        """
        # a roles dict, keys are roles, values are permission of the role
        roles = {
            'Customer': [Permission.VIEW_ALL_PRODUCT, Permission.GRADE_STARS, Permission.COMMENT, Permission.VIEW_ALL_COMMENTS],
            'Retailer': [Permission.VIEW_ALL_PRODUCT, Permission.GRADE_STARS, Permission.COMMENT, Permission.VIEW_ALL_COMMENTS, Permission.UPLOAD_PRODUCT],
            'Administrator': [Permission.VIEW_ALL_PRODUCT, Permission.VIEW_ALL_COMMENTS, Permission.ADMIN]
        }

        # set the default role as 'customer'
        default_role = 'Customer'

        # loop through the roles dict
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            # if the user object is not in db yet, we will create one
            if role is None:
                role = Role(name=r)

            # loop through the permissions of this role
            for perm in roles[r]:
                # give those permissions to this role
                role.add_permission(perm)

            # if this role is the default role (Customer), we set the field of "default" as True
            role.default = (role.name == default_role)

            # add this object to the database session
            db.session.add(role)

        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    start_datetime = db.Column(db.DateTime(), default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))                      # 1 role --> n users
    released_products = db.relationship('Product', backref='seller', lazy='dynamic')  # 1 user --> n products
    released_comments = db.relationship('Comment', backref='author', lazy='dynamic')  # 1 user --> n comments
    released_comment_replies = db.relationship('ReplyComment', backref='author', lazy='dynamic')  # 1 user --> n replies

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def insert_users():
        """
        This is a method for inserting the testing user information, which means fulling the User table.
        This should be used in the console only a single time.
        """
        for user_info in user_list:
            email = user_info[0]
            username = user_info[1]
            password = user_info[2]
            role_id = user_info[3]

            new_user = User(email=email, username=username, password=password, role_id=role_id)

            db.session.add(new_user)
            db.session.commit()

    # ----- use Werkzeug to generate and check the password hash of the user password -----
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # ----- The management of permissions of a user -----
    def can(self, perm):
        """
        Check whether a user has a specific permission
        :param perm: the permission to be checked
        :return: true means yes while false means no
        """
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)


class AnonymousUser(AnonymousUserMixin):
    """
        With this AnonymousUser class, we can access the following functions as well
        even if the user is not logged in
    """

    def can(self, perm):
        return False

    def is_administrator(self):
        return False


# tell Flask-Login that we use the AnonymousUser class that we defined by ourselves
login_manager.anonymous_user = AnonymousUser
