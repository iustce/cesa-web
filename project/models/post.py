# -*- coding: utf-8 -*-
from datetime import datetime

from project.extensions import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode, nullable=True, unique=True)
    body = db.Column(db.UnicodeText, nullable=True, unique=True)
    active = db.Column(db.Boolean, default=False, nullable=False)
    last_modified = db.Column(db.DateTime, nullable=False, default=datetime.now())
    importance = db.Column(db.SmallInteger, nullable=False, default=0)

    files = db.relationship('File', backref='post', lazy='dynamic', cascade='all,delete')
