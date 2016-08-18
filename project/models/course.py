# -*- coding: utf-8 -*-
from datetime import datetime

from project.extensions import db


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode, nullable=False)
    body = db.Column(db.UnicodeText, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    end_date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)

    payment = db.relationship('PaymentStatus', backref='course', lazy='dynamic', cascade='all,delete')

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'price': self.price
        }
