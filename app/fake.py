import os
from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker


def users(count=100):
    """
    Generate fake users into database randomly
    This should be used be calling the function 'products'
    :param count: The number of users we want (default is 100)
    """
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='123',
                 start_datetime=fake.past_datetime(),
                 role_id=[1, 2][randint(0, 1)])

        db.session.add(u)

        # Although it happens rarely, it has the risk of the replicated information
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def products(count=100):
    """
    Generate fake products into database randomly
    This should be used after called the function 'users'
    :param count:   The number of products we want (default is 100)
    """
    fake = Faker()
    user_count = User.query.filter_by(role_id=2).count()  # the number of users with retailer role
    for i in range(user_count):
        # get a user as the seller randomly (u must be the Retailer (role))
        u = User.query.filter_by(role_id=2).offset(randint(0, user_count - 1)).first()

        p = Product(name='MacBookPro 14',
                    description="The most powerful MacBook Pro ever is here. With the blazing-fast M1 Pro or M1 Max chip — the first Apple silicon designed for pros — you get groundbreaking performance and amazing battery life. Add to that a stunning Liquid Retina XDR display, the best camera and audio ever in a Mac notebook, and all the ports you need. The first notebook of its kind, this MacBook Pro is a beast.From $1999",
                    price=18999,
                    release_time=fake.past_datetime(),
                    seller=u)

        db.session.add(p)
        db.session.commit()

        # insert the pictures for this product
        insert_pictures(p.id)


def insert_pictures(product_id):
    """
        This is a method for inserting the picture information into the database,
        which are the pictures for fake products.
        This should be called after calling the products(100)
    """
    # the path to store the pictures
    path = 'upload/product'
    # the name of the default picture names
    product_pic_name_list = ['macbook1.png', 'macbook2.jpg', 'macbook3.jpg']

    '''
        we have inserted the fake products first, here we just go for inserting the picture for this products
    '''
    # loop through the picture group
    for pic_name in product_pic_name_list:
        # generate the picture address by joining the directory and the picture name
        pic_address = os.path.join(path, pic_name).replace('\\', '/')

        new_pic = ProductPic(address=pic_address, product_id=product_id)

        db.session.add(new_pic)
    db.session.commit()



# to avoid circular import, we should do this here.
from . import db
from .models import User, Product, ProductPic
