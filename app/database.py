from app import db
from flask_login import UserMixin


class UserDatabase(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(1000), nullable=False, unique=True)
    password = db.Column(db.String(1000), nullable=False)

class PortalDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    student_number = db.Column(db.String(8), nullable=True)
    portal_password = db.Column(db.String(1000), nullable=True)
    matrix_A = db.Column(db.String(13), nullable=True)
    matrix_B = db.Column(db.String(13), nullable=True)
    matrix_C = db.Column(db.String(13), nullable=True)
    matrix_D = db.Column(db.String(13), nullable=True)
    matrix_E = db.Column(db.String(13), nullable=True)
    matrix_F = db.Column(db.String(13), nullable=True)
    matrix_G = db.Column(db.String(13), nullable=True)
    matrix_H = db.Column(db.String(13), nullable=True)
    matrix_I = db.Column(db.String(13), nullable=True)
    matrix_J = db.Column(db.String(13), nullable=True)


db.create_all()
