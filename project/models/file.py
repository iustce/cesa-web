# -*- coding: utf-8 -*-
from datetime import datetime

from project.extensions import db


class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode, nullable=False)
    body = db.Column(db.UnicodeText, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    end_date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)

    payment = db.relationship('PaymentStatus', backref='class', lazy='dynamic', cascade='all,delete')