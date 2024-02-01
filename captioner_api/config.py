import os

class Config:
    CORS_HEADERS = 'Content-Type'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')\
        or 'sqlite:///' + os.path.join('app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False