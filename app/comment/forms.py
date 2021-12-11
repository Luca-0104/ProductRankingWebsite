from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    """
        The form to upload comment for a product
    """
    text = TextAreaField("Leave your comment here", validators=[DataRequired(), Length(1, 500)])     # comment text
    pictures = MultipleFileField('Upload some pictures', validators=[DataRequired(), Length(2, 5, 'You must give 2-5 pictures')])   # pictures of this product
    submit = SubmitField("Confirm")
