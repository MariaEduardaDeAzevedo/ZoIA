import cryptocode
import os
from flask import Blueprint, get_flashed_messages, redirect, render_template, flash, request, url_for
from flask_login import current_user, AnonymousUserMixin

from cryptography.fernet import Fernet

from app.models import Role, User, Config
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    user = current_user
    
    if isinstance(current_user, AnonymousUserMixin):
        return redirect(url_for('auth.login'))
    
    return redirect(url_for('users.users_list'))

@main.route('/configuration')
def configuration():

    user = current_user
    config = Config.query.get(1)

    if isinstance(current_user, AnonymousUserMixin):
        return redirect(url_for('auth.login'))
    elif current_user.role.name == "USER":
        return render_template('not_allowed.html', user=user)

    return render_template('configuration.html', user=user, config=config)

@main.route('/configuration', methods=['POST'])
def configuration_post():

    if isinstance(current_user, AnonymousUserMixin):
        return redirect(url_for('auth.login'))
    elif current_user.role.name == "USER":
        return render_template('not_allowed.html', user=current_user)
    
    email = request.form.get('email')
    password = request.form.get('password')

    config = Config.query.get(1)
    if email.strip() != '' and password.strip() != '':
        config.dispatch_email = email
        encoded_pass = cryptocode.encrypt(password,os.getenv('SECRET_KEY'))
        config.dispatch_email_password = encoded_pass
        db.session.commit()
    else:
        print("ELLLLSSSSEEEE")
        flash('All fields are required.')
        redirect(request.referrer) 

    return redirect(url_for('main.configuration'))