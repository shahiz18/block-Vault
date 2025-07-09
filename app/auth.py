from flask import Blueprint, flash , render_template , request , redirect , url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from .models import User,db

auth = Blueprint('auth',__name__)

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup', methods=['POST'])

def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # Validate input
    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email already exists!', 'danger')
        return redirect(url_for('auth.signup'))
    
    new_user= User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/login' , methods= ['POST'])
def login_post():

    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password , password): #check pass hash is an in built funtion 
        flash('Invalid username or password!', 'danger')
        return redirect(url_for('auth.login'))
    
    login_user(user)
    return redirect(url_for('main.upload'))

@auth.route('/logout')
@login_required

def logout():
    logout_user()
    return redirect(url_for('auth.login'))