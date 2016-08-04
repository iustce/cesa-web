# -*- coding: utf-8 -*-
from datetime import datetime

from project.extensions import db


class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Unicode(254), nullable=True, unique=True)
    active = db.Column(db.Boolean, default=False, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
