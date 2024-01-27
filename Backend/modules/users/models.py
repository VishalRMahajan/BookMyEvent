from app import db
from flask_login import UserMixin


class Student(db.Model, UserMixin):
    pid = db.Column(db.Integer, nullable=False, unique=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name= db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='User')
    email = db.Column(db.String(20), nullable=False, primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, default=False)

    def get_id(self):
        return (self.role)
    
class Committee(db.Model, UserMixin):
    pid = db.Column(db.Integer, nullable=False, unique=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name= db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Committee')
    email = db.Column(db.String(20), nullable=False, primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, default=False)

    def get_id(self):
        return (self.role)

