# -*- coding: utf-8 -*-
from datetime import datetime

from project.extensions import db


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=True)
    kind = db.Column(db.Enum('image', 'pdf', 'file', 'music', 'other', name='file_type'))

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'url': self.url,
            'path': self.path,
            'kind': self.kind
        }
