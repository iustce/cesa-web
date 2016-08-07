# -*- coding: utf-8 -*-
from datetime import datetime

from project.extensions import db

class PaymentStatus(db.Model):
    __tablename__ = 'payment_status'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    payment_status = db.Column(db.Enum('done', 'failed', 'waiting', 'undone'))

    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=True)