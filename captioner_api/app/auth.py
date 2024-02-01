import os
from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from app.models import User
import cryptocode

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user:
        flash('Email not found. Please check your login details and try again.')
        return redirect(url_for('auth.login')) 
    elif password != cryptocode.decrypt(user.access_token, os.environ.get('SECRET_KEY')):
        flash('Wrong password. Please check your login details and try again.')
        return redirect(url_for('auth.login')) 
    
    login_user(user, remember=remember)

    user = current_user

    if user.role.name == "USER":
        flash('''Sorry, your account role is not allowed to access this. 
        If you were supposed to access this area, please contact 
        the tool suport team.''')
        logout_user()
        return redirect(url_for('auth.login')) 
    elif user.deleted_at is not None:
        flash('Your account is currently deactivated. Contact the tool suport team for more informations.')
        logout_user()
        return redirect(url_for('auth.login')) 
    
    return redirect(url_for('users.users_list'))

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 