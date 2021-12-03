import os
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin

from app import db, login_manager
from app.tableInfo import user_list, product_list, product_category_list, category_list, product_picture_list

import random


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
        Role.insert_roles()  # roles of users
        User.insert_users()  # the constant user accounts for test
        # users(100)  # 100 fake users
        Category.insert_categories()  # the product categories
        Product.insert_products()  # the constant products for show
        ProductPic.insert_pictures()  # the pictures of the constant products
        # products(100)  # 100 fake products


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


'''
    This is a table for containing the 'n to n' relationship of Product model and Category model 
'''
classifications = db.Table('classifications',
                           db.Column('product_id', db.Integer, db.ForeignKey('products.id')),
                           db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
                           )


class UserProductRank(db.Model):
    """
        This is a table for containing the 'n to n' relationship of Product model and User model
        1 product can be ranked by n users
        1 user can rank n products
        This table also records the grade that the user rated this product, which is called 'rank'
    """
    __tablename__ = 'user_product_ranks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    rank = db.Column(db.Float)

    def __repr__(self):
        return '<UserProductRank %r ranked %r as %r>' % (self.user, self.product, self.rank)


class Category(db.Model):
    """
        a table for storing all the categories of products in our website.
        1 product --> n categories;
        1 category --> n products
    """
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name

    @staticmethod
    def insert_categories():
        """
            This is a method for inserting the categories into the database.
            This should be used a single time in the terminal.
            This should be called before calling the Product.insert_products()
        """
        for cate_name in category_list:
            new_category = Category(name=cate_name)
            db.session.add(new_category)
        db.session.commit()


class ReplyComment(db.Model):
    """
    a table for storing the replies of the comments of products
    """
    __tablename__ = 'comment_replies'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)  # 1 comment --> n replies
    auth_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 1 user --> n replies
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
    pictures = db.relationship('CommentPic', backref='comment', lazy='dynamic')  # 1 comment --> n pictures
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # 1 product --> n comment
    auth_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 1 user --> n comment
    replies = db.relationship('ReplyComment', backref='comment')  # 1 comment --> n replies
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
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))  # 1 comment --> n picture

    def __repr__(self):
        return '<CommentPic %r>' % self.address


class ProductPic(db.Model):
    """
    a table for storing all the pictures related to the products
    """
    __tablename__ = 'product_pictures'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(256), default='upload/product/default.png')
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))  # 1 product --> n picture

    def __repr__(self):
        return '<ProductPic %r>' % self.address

    @staticmethod
    def insert_pictures():
        """
            This is a method for inserting the picture information into the database,
            which are the pictures for the constant products.
            This should be used a single time in the terminal.
            This should be called after calling the Product.insert_products()
        """
        # the path to store the pictures
        path = 'upload/product'

        # we get the index when looping, this can help to get the correspond product, which owns this group of pictures
        for index, pic_group in enumerate(product_picture_list):
            '''
                we have inserted the constant products first, therefore the id of constant product goes from 1.
                Index begins from 0, so that using (index+1) can get the id of the corresponding product id
            '''
            product_id = index + 1

            # loop through the picture group
            for pic_name in pic_group:
                # make sure the name of picture is safe
                # pic_name = generate_safe_pic_name(pic_name)
                # generate the picture address by joining the directory and the picture name
                pic_address = os.path.join(path, pic_name).replace('\\', '/')

                new_pic = ProductPic(address=pic_address, product_id=product_id)

                db.session.add(new_pic)

        db.session.commit()


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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 1 user --> n products
    comments = db.relationship('Comment', backref='product', lazy='dynamic')  # 1 product --> n comments
    # 1 product --> n categories;  1 category --> n products
    categories = db.relationship('Category', secondary=classifications, backref=db.backref('products', lazy='dynamic'),
                                 lazy='dynamic')
    # 1 product --> rated ranked by n users; 1 user --> can rank n products
    ranked_user_relations = db.relationship('UserProductRank', backref='product', lazy='dynamic')
    rank = db.Column(db.Float, default=0)  # the stars rank, 0 - 5
    rank_count = db.Column(db.Integer, default=0)  # How many times is this product being rated
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Product: %r; id: %r>' % (self.name[:20], self.id)

    @staticmethod
    def insert_products():
        """
            This is a method for inserting the constant product information.
            This should be used in the console only a single time.
        """

        # # use Faker to generate the past_datetime for products as the releasing datetime
        # fake = Faker()

        # when looping, we also get the index, this can help to get the correspond category list
        for index, product_info in enumerate(product_list):
            name = product_info[0]
            description = product_info[1]
            price = product_info[2]

            '''
                get a random retailer user as the seller of this product
            '''
            # the number of users with retailer role
            user_count = User.query.filter_by(role_id=2).count()
            # get a user as the seller randomly (u must be the Retailer (role))
            u = User.query.filter_by(role_id=2).offset(random.randint(0, user_count - 1)).first()

            # new_product = Product(name=name, description=description, price=price, release_time=fake.past_datetime(),
            #                       seller=u, rank=random.random() * 5)

            # -------------------------------- change release time to random!!! ------------------------------------------------------------------------------------------------------
            # -------------------------------- change release time to random!!! ------------------------------------------------------------------------------------------------------
            # -------------------------------- change release time to random!!! ------------------------------------------------------------------------------------------------------
            new_product = Product(name=name, description=description, price=price, release_time=datetime.utcnow,
                                  seller=u, rank=random.random() * 5)

            db.session.add(new_product)

            '''
                give the category tags to this product
            '''
            # use the index to get the correspond category list
            for tag in product_category_list[index]:
                # find the category with this name and add it to this product
                cate = Category.query.filter_by(name=tag).first()
                new_product.categories.append(cate)

                db.session.add(new_product)

        db.session.commit()


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)  # we will set the 'customer' as default role
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')  # 1 role --> n users

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        # initialize the permissions
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return '<Role %r>' % self.name

    # ----- functions for permission management (learned from the book) -----
    # book: 'Flask Web Development: Developing Web Applications with Python, Second Edition'
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
            'Customer': [Permission.VIEW_ALL_PRODUCT, Permission.GRADE_STARS, Permission.COMMENT,
                         Permission.VIEW_ALL_COMMENTS],
            'Retailer': [Permission.VIEW_ALL_PRODUCT, Permission.GRADE_STARS, Permission.COMMENT,
                         Permission.VIEW_ALL_COMMENTS, Permission.UPLOAD_PRODUCT],
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
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 1 role --> n users
    released_products = db.relationship('Product', backref='seller', lazy='dynamic')  # 1 user --> n products
    released_comments = db.relationship('Comment', backref='author', lazy='dynamic')  # 1 user --> n comments
    released_comment_replies = db.relationship('ReplyComment', backref='author', lazy='dynamic')  # 1 user --> n replies
    # 1 product --> rated ranked by n users; 1 user --> can rank n products
    ranked_product_relations = db.relationship('UserProductRank', backref='user', lazy='dynamic')

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

    # ----- use Werkzeug to generate and check the password hash of the user password (learned from the book) -----
    # book: 'Flask Web Development: Developing Web Applications with Python, Second Edition'
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # ----- The management of permissions of a user (learned from the book) -----
    # book: 'Flask Web Development: Developing Web Applications with Python, Second Edition'
    def can(self, perm):
        """
        Check whether a user has a specific permission
        :param perm: the permission to be checked
        :return: true means yes while false means no
        """
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)


# (learned from the book)
# book: 'Flask Web Development: Developing Web Applications with Python, Second Edition'
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

# to avoid circular import, we should do this here.
from app.product.views import generate_safe_pic_name
