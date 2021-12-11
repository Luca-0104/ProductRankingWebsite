from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, MultipleFileField, FloatField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, number_range, ValidationError


class ProductUploadForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(1, 128)])
    description = StringField('Product Description', validators=[DataRequired()])
    price = FloatField('Set the Price', validators=[DataRequired(), number_range(0, 99999999)])
    pictures = MultipleFileField('Upload pictures for exhibition', validators=[DataRequired(), Length(2, 5, 'You must give 2-5 pictures')])
    submit = SubmitField('Confirm')


    def validate_pictures(self, field):
        """
        validate whether the length of the names of pictures are out of bound
        This function will be called on picture field automatically
        :param field: pictures
        :return:
        """
        for pic in self.pictures.data:
            if len(pic.filename) > 214:
                raise ValidationError('Picture name cannot longer than 216 chars!')
