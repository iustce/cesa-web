
from datetime import datetime
from application.extensions import db


class Log(db.Model):
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    description = db.Column(db.String, default="")
    status = db.Column(db.Enum('in progress', 'done', 'failed', 'not checked', name='status'))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_json(self):
        return {
            'date': str(self.date),
            'status': self.status,
            'description': self.description,
        }