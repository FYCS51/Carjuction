from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, FileField,IntegerField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Optional
from wtforms import StringField, FileField

class ProductForm(FlaskForm):
    name = StringField("company", validators=[DataRequired()])
    model = StringField("model", validators=[DataRequired()])
    year = IntegerField("year",validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Optional()])
    image1=FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')], render_kw={"class": "form-control"})
    image2 = FileField("Image", validators=[Optional()])
    image3 = FileField("Image", validators=[Optional()])
   