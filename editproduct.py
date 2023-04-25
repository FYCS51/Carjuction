from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, FileField,IntegerField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, FileField
class EditForm(FlaskForm):
    name = StringField("company", validators=[DataRequired()])
    model = StringField("model", validators=[DataRequired()])
    year = FloatField("year",validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Optional()])
    image1=FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')], render_kw={"class": "form-control"})