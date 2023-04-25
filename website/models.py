from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class Custsell(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    address = db.Column(db.String(150))
    price = db.Column(db.String(150))

class Product(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    com = db.Column(db.String(150), nullable=False)
    mod = db.Column(db.String(150),nullable=False)
    year =db.Column(db.Numeric(10,2),nullable=False)
    price =db.Column(db.Numeric(10,2),nullable=False)
    desc = db.Column(db.Text,nullable=False)
    img1 = db.Column(db.String(150),nullable=False,default="image.jpg")
    img2 = db.Column(db.String(150),nullable=False,default="image.jpg")
    img3 = db.Column(db.String(150),nullable=False,default="image.jpg")
    
#db.create_all()