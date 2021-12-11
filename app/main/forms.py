from flask import session
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Email, ValidationError

from app.models import User
from app.public_tools import get_user_by_name


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[0-9a-zA-Z_.]{1,}$', 0,
                                                                                         "Username must contain only letters, numbers, dots or underscores")])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    pictures = FileField('Upload pictures for your avatar', validators=[FileRequired()])
    submit = SubmitField('Confirm')

    def validate_email(self, field):
        """
        validate whether the email address is already used
        This function will be called on email field automatically
        :param field: email
        :return:
        """
        current_user = get_user_by_name(session.get("username"))
        if current_user.email != field.data:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('Email already exists!')

    def validate_username(self, field):
        """
        validate whether the username has already been used
        This function will be called on username field automatically
        :param field: username
        :return:
        """
        current_user = get_user_by_name(session.get("username"))
        if current_user.username != field.data:
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('Username already exists!')
