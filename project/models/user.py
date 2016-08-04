# -*- coding: utf-8 -*-
from datetime import datetime

from project.extensions import db
from sqlalchemy_utils import PasswordType, force_auto_coercion

force_auto_coercion()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Unicode(254), nullable=True, unique=True)
    student_number = db.Column(db.String(8), nulllabe=False, unique=True)
    phone = db.Column(db.String(11), nullable=True, unique=True)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512', 'md5_crypt'], deprecated=['md5_crypt']), nullable=True)
    active = db.Column(db.Boolean, default=False, nullable=False)
    registered_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    tokens = db.relationship('Token', backref='user', lazy='dynamic', cascade='all,delete')
    logs = db.relationship('Log', backref='user', lazy='dynamic', cascade='all,delete')
