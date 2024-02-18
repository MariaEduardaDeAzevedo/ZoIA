from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
import cryptocode

from app.services.CaptionerService.captioner import Captioner

from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

captioner_model = Captioner()
db = SQLAlchemy()
from .models import Config, Role, User

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI")
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    @app.route('/api/docs')
    def get_swagger():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "My API"
        return jsonify(swag)

    # Swagger UI route
    SWAGGER_URL = '/api/docs/ui'
    API_URL = '/api/docs'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "ZoIA API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

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
