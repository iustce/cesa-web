# -*- coding: utf-8 -*-
from datetime import datetime

from project.extensions import db


class PaymentStatus(db.Model):
    __tablename__ = 'payment_status'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    status = db.Column(db.Enum('done', 'failed', 'waiting', 'undone', name='pay'))

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=True)


class Payment (db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.String, nullable=False)