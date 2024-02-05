from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
import os
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import random
import cryptocode

from app.services.CaptionerService.captioner import Captioner

captioner_model = Captioner()
db = SQLAlchemy()
from .models import Config, Role, User

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI")
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    from .roles import roles as roles_blueprint
    app.register_blueprint(roles_blueprint)

    from .captioner import captioner as captioner_blueprint
    app.register_blueprint(captioner_blueprint)

    with app.app_context():
        db.create_all()
        
        try:
            db.session.add(Role('SUPERADMIN', 'SYSTEM'))
            db.session.add(Role('ADMIN', 'SYSTEM'))
            db.session.add(Role('USER', 'SYSTEM'))
            db.session.commit()
        except:
            pass
        
        try:
            access_token = os.environ.get('DEFAULT_ACCESS_TOKEN')
            encoded_access_token = cryptocode.encrypt(access_token,os.environ.get('SECRET_KEY'))
            db.session.add(User('superadmin@localhost.com', 1, encoded_access_token, 'SYSTEM'))
            db.session.commit()
        except Exception as e:
            pass

        try:
            db.session.add(Config())
            db.session.commit()
        except:
            pass
        
        return app
