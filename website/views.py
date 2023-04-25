from flask import Blueprint,render_template 
from flask_login import login_user, login_required, logout_user, current_user
from .models import Product
from flask import Blueprint,render_template,request,flash,g,redirect, session, url_for
views = Blueprint('views',__name__)
@views.route('/')
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 9
    products = Product.query.paginate(page=page, per_page=per_page)
    return render_template("home.html",user = current_user,products=products )

@views.route("/productDetail/<int:prod_id>")
def productDetail(prod_id):
    products =Product.query.get(prod_id)
    return render_template("productDetail.html",user = current_user,products=products )
    