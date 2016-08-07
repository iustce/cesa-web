# -*- coding: utf-8 -*-
from datetime import datetime

from flask import request, abort
from project.extensions import db, redis
from sqlalchemy_utils import PasswordType, force_auto_coercion

force_auto_coercion()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(254), nullable=True)
    student_id = db.Column(db.String(8), nulllabe=False, unique=True)
    phone = db.Column(db.String(11), nullable=True, unique=True)
    national_code = db.Column(db.String(10), nullable=True, unique=True)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512', 'md5_crypt'], deprecated=['md5_crypt']), nullable=True)
    active = db.Column(db.Boolean, default=False, nullable=False)
    registered_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    university = db.Column(db.Enum, ('iust', 'sharif', 'tehran', 'other'))

    tokens = db.relationship('Token', backref='user', lazy='dynamic', cascade='all,delete')

    @classmethod
    def authenticate(cls, populate=True):
        """
        If user authenticated correctly then g.user value will be filled with user sql alchemy
        other wise it will abort request with 401 unauthorised http response code
        :param populate: if False user is user_id and if True user is user_obj from database. use populate=False for perfomance
        """

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                try:
                    # NOTE:
                    #  In most cases user_id is None so it's better
                    #  instead of connecting to database and check None value
                    # check data in program

                    access_token_id = request.headers.get('Access-Token')
                    assert access_token_id

                    user_id = redis.get('uat:%s' % access_token_id)
                    assert user_id

                    g.user = cls.query.get(user_id) if populate else user_id
                    assert g.user

                    return f(*args, **kwargs)
                except AssertionError:
                    return abort(401)

            return wrapper

        return decorator
