from datetime import datetime
from functools import wraps
import os
import time
from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import AnonymousUserMixin, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app.models import User
import cryptocode
import jwt
from flask_login import current_user

auth = Blueprint('auth', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "Authorization" in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
            if not token:
                return {
                    "message": 'authentication token is missing.',
                    "data": None,
                    "error": {
                        "code": 401,
                        "error": 'Unauthorized'
                    }
                }, 401
            
            try:
                data = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=[os.environ.get('DECODE_ALGORITHM')])
                user = User.query.get(data['id'])

                login_time = data["timestamp"]
                login_time = datetime.fromtimestamp(login_time)
                diff = datetime.now() - login_time

                if diff.days > 365:
                    return {
                        "message": 'your session expired.',
                        "data": None,
                        "error": {
                            "code": 401,
                            "error": 'Unauthorized'
                        }
                    }, 401
                    logout_user()
                if not user:
                    return {
                        "message": 'invalid authorization token.',
                        "data": None,
                        "error": {
                            "code": 401,
                            "error": 'Unauthorized'
                        }
                    }, 401
                if user.deleted_at:
                    return {
                        "message": 'your account is inactive. If you think this is a problem, please contact the tool support team.',
                        "data": None,
                        "error": {
                            "code": 401,
                            "error": 'Unauthorized'
                        }
                    }, 401
            except Exception as e:
                return {
                    "message": 'it seems like an internal error. Please, report the support team.',
                    "data": None,
                        "error": {
                            "code": 500,
                            "error": str(e)
                        }
                    }, 500
            return f(user, *args, **kwargs)
        
        else:
            return {
                    "message": 'authentication token is missing.',
                    "data": None,
                    "error": {
                        "code": 401,
                        "error": 'Unauthorized'
                    }
                }, 401
        
    return decorated


@auth.route('/api/login', methods=['POST'])
def login_app():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        remember = True if request.json.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user:
            return {
                    "message": "Could not finish login: e-mail provided is not registered.",
                    "data": None,
                    "error": {'error':"Bad request", 'code': 400}
                }, 400
        elif password != cryptocode.decrypt(user.access_token, os.environ.get('SECRET_KEY')):
            return {
                    "message": "Could not finish login: access token provided is invalid.",
                    "data": None,
                    "error": {'error':"Bad request", 'code': 400}
                }, 400
        elif user.deleted_at:
            return {
                    "message": 'Could not finish login: your account is inactive. If you think this is a problem, please contact the tool support team.',
                    "data": None,
                    "error": {
                                "code": 401,
                                "error": 'Unauthorized'
                            }
                }, 401
        

        try:
            token = jwt.encode({
                'id': user.id,
                'timestamp': time.time()
            }, os.environ.get('SECRET_KEY'), os.environ.get('DECODE_ALGORITHM'))

            print(token)

            login_user(user, remember=remember)
            return {
                        "message": "Successfully fetched auth token",
                        "data": {
                            'token': token
                        }
                    }, 200
        except Exception as e:
            return {
                    "error": 'Could not finish login: it seems like an internal error. Please, report the support team.',
                    "message": str(e)
                }, 500
    except Exception as e:
        return {
                "error": 'Could not finish login: it seems like an internal error. Please, report the support team.',
                "message": str(e)
            }, 500

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

@login_required
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 