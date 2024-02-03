from datetime import datetime
import os
import random
import time
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import AnonymousUserMixin, current_user, login_required
from werkzeug.security import generate_password_hash
import cryptocode

from app.models import User
from . import db

users = Blueprint('users', __name__)

def decrypt(token):
    return cryptocode.decrypt(token, os.environ.get('SECRET_KEY'))

@login_required
@users.route('/users')
def users_list():

    user = current_user

    if isinstance(current_user, AnonymousUserMixin):
        return redirect(url_for('auth.login'))  
    elif current_user.role.name == "USER":
        return redirect(url_for('main.index'))  

    users = User.query.all()

    return render_template('users.html', user=user, users=users, decrypt=decrypt)

@login_required
@users.route('/user')
def add_user():

    user = current_user

    print(user)

    if isinstance(current_user, AnonymousUserMixin):
        return redirect(url_for('auth.login'))  
    elif current_user.role.name == "USER":
        return redirect(url_for('main.index')) 

    return render_template('user.html', user=user, edit=None, action='/user')

@login_required
@users.route('/user', methods=['POST'])
def add_user_post():
    email = request.form.get('email')
    role_id = int(request.form.get('role_id')) 


    if _validate_user_form(email, role_id, None): 
        access_token = "%032x" % random.getrandbits(128)
        encoded_access_token = cryptocode.encrypt(access_token,os.environ.get('SECRET_KEY'))
        new_user = User(email=email, access_token=encoded_access_token, role_id=role_id, created_by=current_user.email)

        db.session.add(new_user)
        
        db.session.commit()

        return redirect(url_for('users.users_list'))

    return redirect(request.referrer) 


@login_required
@users.route('/user/edit/<int:id>')
def edit_user(id):

    user = current_user


    if isinstance(current_user, AnonymousUserMixin):
        return redirect(url_for('auth.login'))  
    elif current_user.role.name == "USER":
        return redirect(url_for('main.index')) 

    edit_user = User.query.get(id)
    return render_template('user.html', user=user, edit=edit_user, action=f'/user/edit/{id}', decrypt=decrypt)

@login_required
@users.route('/user/edit/<int:id>', methods=['POST'])
def edit_user_post(id):
    email = request.form.get('email')
    role_id = int(request.form.get('role_id')) 

    user = current_user

    if isinstance(current_user, AnonymousUserMixin):
        return redirect(url_for('auth.login'))  
    elif current_user.role.name == "USER":
        return redirect(url_for('main.index')) 
    
    edit_user = User.query.get(id)

    if _validate_user_form(email, role_id, edit_user): 
        edit_user.email = email
        edit_user.role_id = role_id
        edit_user.updated_by = user.email
        edit_user.updated_at = datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

        db.session.commit()
        return redirect(url_for('users.users_list'))

    return render_template('users.user_edit', user=user, edit=edit_user, action=f'/user/edit/{id}')

@login_required
@users.route('/user/activate/<int:id>', methods=['GET'])
def delete_user(id):

    user = User.query.get(id)

    if user and user != current_user and not user.deleted_at:
        user.deleted_at = datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        user.updated_at = datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        user.updated_by = current_user.email
        db.session.commit()
    elif user and user != current_user:
        user.deleted_at = None
        user.updated_at = datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        user.updated_by = current_user.email
        db.session.commit()

    return redirect(request.referrer) 

def _validate_user_form(email, role_id, user):
    if email.strip() == "" or role_id is None:
        flash('All fields are required')
        return False
    elif (user is None or email != user.email) and User.query.filter_by(email=email).first():
        flash('E-mail already registered')
        return False

    return True