from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask import Blueprint,render_template,request,flash,g,redirect, session, url_for
from .models import *
from .models import Product
from .models import Custsell
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
#from website import photos
from flask_login import login_user, login_required, logout_user, current_user
from flask_cors import CORS,cross_origin
from flask_login import login_user, login_required, logout_user, current_user
from adminproduct import ProductForm
from editproduct import EditForm
from sqlalchemy.ext.declarative import declarative_base

import os
from PIL import Image

from flask_sqlalchemy import SQLAlchemy

import secrets

import re
import pickle
import pandas as pd
import numpy.core.multiarray
import numpy as np
import sklearn

Base = declarative_base()#base directory for storing images
model=pickle.load(open('./website/LinearRegressionModel.pkl','rb'))
car=pd.read_csv('./website/Cleaned_Car_data.csv')
eregex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

name_pattern = re.compile(r"^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$")

# Regular expression pattern for a phone number
phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
auth = Blueprint('auth',__name__)
@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('Semail')
        password = request.form.get('Spassword')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html",user=current_user)

@auth.route('/adminlogin', methods=['GET','POST'])
def adminlogin():
    if request.method == 'POST':
        username = request.form.get('Semail')
        password = request.form.get('Spassword')
        if username=="Naresh9890" and password=="9890460253":
            flash('Logged in successfully!', category='success')
            #login_user(username, remember=True)
            return redirect(url_for('auth.adminhome'))
        else:
            flash('Invalid Crediential .', category='error')
    return render_template("adminlogin.html",user=current_user)

@auth.route('/adminhome')
def adminhome():
    products = Product.query.all()
    return render_template("adminhome.html",user = current_user,products=products )



@auth.route('/carseller')
def carseller():
    custselling = Custsell.query.all()
    return render_template("carseller.html",user = current_user,custselling=custselling )



@auth.route('/predictioncar',methods=['GET','POST'])
def predictioncar():
    if request.method == 'POST' or 'GET':
        companies=sorted(car['company'].unique())
        car_models=sorted(car['name'].unique())
        year=sorted(car['year'].unique(),reverse=True)
        fuel_type=car['fuel_type'].unique()
        companies.insert(0,'Select Company')
        return render_template('predictioncar.html',companies=companies, car_models=car_models, years=year,fuel_types=fuel_type,user=current_user)


@auth.route('/predict',methods=['POST'])
@cross_origin()
def predict():
    company=request.form.get('company')
   
    car_model=request.form.get('car_models')
    
    year=request.form.get('year')
    
    fuel_type=request.form.get('fuel_type')
    
    driven=request.form.get('kilo_driven')
    car = {'company':company, 'car_model':car_model, 'year':year, 'fuel_type':fuel_type, 'driven':driven}
    session['company'] = company
    session['car_model']=car_model
    session['year']=year
    session['fuel_type']=fuel_type
    session['driven']=driven
    print(car_model,company,year,driven,fuel_type)
   

    prediction=model.predict(pd.DataFrame( [[car_model,company,year,driven,fuel_type]],columns=['name', 'company', 'year', 'kms_driven', 'fuel_type']))
    print(prediction)
    session['prediction']=str(np.round(prediction[0],2))
    return str(np.round(prediction[0],2))
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign_up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('Semail')
        firstName = request.form.get('Sname')
        password1 = request.form.get('Spassword1')
        password2 = request.form.get('Spassword2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif(False ==(re.fullmatch(eregex, email))):
            flash("Please enter the correct email",category='error')
        elif len(firstName)<3:
            flash("Please enter the correct name",category='error')
        elif len(password1)<7:
            flash("Password must be at least 7 character",category='error')
        elif password1 != password2:
            flash("Password don\'t match",category='error')
        else:
            new_user = User(email=email,first_name=firstName, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))
            flash("Account created! ", category='success')
    return render_template("sign_up.html",user=current_user)
@auth.route('/addproducts', methods=['POST','GET'] )
def addproducts():
    form = ProductForm(request.form)
    if request.method=="POST":
        name = form.name.data
        model=form.model.data
        year=form.year.data
        price=form.price.data
        description=form.description.data
        image1=(request.files.get("image1"))
        print(type(image1))
        #image1=form.image1.data
        
        print(image1)
       
        filename = secure_filename(image1.filename)
        image1.save(os.path.join("website/static/images", filename))
        if not image1:
         return "No file selected"
        #filename = secure_filename(image1.filename)
        #image1.save(os.path.join("static/images", filename))
        #image2=photos.save(request.files.get("image2"),name=secrets.token_hex(10)+".")
        image2=request.files.get("image2")
        #image3=photos.save(request.files.get("image3"),name=secrets.token_hex(10)+".")
        filename2 = secure_filename(image2.filename)
        image2.save(os.path.join("website/static/images", filename2))
        image3=request.files.get("image3")
        filename3 = secure_filename(image3.filename)
        image3.save(os.path.join("website/static/images", filename3))
        addp = Product(com=name,mod=model,year=year,price=price,desc=description,img1=filename,img2=filename2,img3=filename3)
        db.session.add(addp)
        db.session.commit()
        flash(f'Company {name} added successfully')
        return redirect(url_for('auth.adminhome'))
    return render_template("addproducts.html",title='add product',form=form)
@auth.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect("/adminhome")
@auth.route("/delete_sell/<int:sell_id>")
def delete_sell(sell_id):
    sell = Custsell.query.get(sell_id)
    db.session.delete(sell)
    db.session.commit()
    return redirect("/carseller")
@auth.route("/editproduct/<int:product_id>", methods=["GET", "POST"])
def editproduct(product_id):
    eprod = Product.query.get(product_id)
    form = EditForm(request.form)
    if request.method=="POST":
        eprod.com = form.name.data
        eprod.mod=form.model.data
        eprod.year=form.year.data
        eprod.price=form.price.data
        eprod.desc=form.description.data
        #image1=photos.save(request.files.get("image1"),name=secrets.token_hex(10)+".")
        eprod.img1=form.image1.data
        db.session.commit()
        flash(f'Product {product_id} update successfully ')
        return redirect(url_for('auth.adminhome'))
    form.name.data = eprod.com
    form.model.data = eprod.mod
    form.year.data = eprod.year
    form.price.data = eprod.price
    form.description.data = eprod.desc
    form.image1.data = eprod.img1
    return render_template('editproduct.html', form=form)
@auth.route('/customerselling', methods=["GET", "POST"])
def customerselling():
    company = session.get('company', None)
    model = session.get('car_model', None)
    year = session.get('year', None)
    fuel = session.get('fuel_type', None)
    driven = session.get('driven',None)
    prediction = session.get('prediction',None)
    if request.method == 'POST':
        name = request.form.get('fname')
        phone = request.form.get('phone')
        address = request.form.get('address')
        cus = Custsell.query.filter_by(phone=phone).first()
        if cus:
             flash('Phone number already exists.', category='error')
        elif not re.match(name_pattern, name):
            return flash("Please enter the correct name",category='error') 
        elif not re.match(name_pattern, name):
            return flash("Please enter the correct last name",category='error') 
        elif not re.match(phone_pattern, phone):
             return flash("Please enter the correct phone number",category='error')
        else:
            cus_sell = Custsell(phone=phone,name=name,address=address,price=session.get('prediction',None))
            db.session.add(cus_sell)
            db.session.commit()
            flash('we will call you soon ', category='success')
            return redirect(url_for('auth.predictioncar'))    
    return render_template('customerselling.html',company=company,model=model,year=year,fuel=fuel,driven=driven,prediction=prediction,user=current_user)