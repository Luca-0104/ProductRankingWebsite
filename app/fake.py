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

        p = Product(name=['iPhone13', 'Orange', 'A Table', 'IELTS 4-16', 'Gibson', 'Arai Helmet'][randint(0, 5)],
                    description=fake.text(),
                    price=fake.random_int(),
                    release_time=fake.past_datetime(),
                    seller=u)

        db.session.add(p)
    db.session.commit()


# to avoid circular import, we should do this here.
from . import db
from .models import User, Product

