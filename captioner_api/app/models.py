from flask_login import UserMixin

from . import db

class BaseModel():
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=None, server_onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, server_default=None)
    updated_by = db.Column(db.String, server_default=None)
    created_by = db.Column(db.String, server_default=None)

    def __init__(self, created_by) -> None:
        self.created_by = created_by
        super().__init__()

class User(BaseModel, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    access_token = db.Column(db.String(256))

    def __init__(self, email, role_id, access_token, created_by) -> None:
        self.email = email
        self.role_id = role_id
        self.access_token = access_token
        super().__init__(created_by)

class Role(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, name, created_by) -> None:
        self.name = name
        super().__init__(created_by)

class Config(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dispatch_email = db.Column(db.String(100), unique=True)
    dispatch_email_password = db.Column(db.String(100), unique=True)

    def __init__(self, dispatch_email=None, dispatch_email_password=None, created_by='SYSTEM') -> None:
        self.dispatch_email = dispatch_email
        self.dispatch_email_password = dispatch_email_password
        super().__init__(created_by)