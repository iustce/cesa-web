# python imports
from datetime import datetime

# project imports
from project.extensions import db, redis
from project.models import User


class Token(db.Model):
    __tablename__ = 'tokens'

    refresh = db.Column(db.String(36), primary_key=True)
    last_refresh = db.Column(db.DateTime, nullable=False, default=datetime.now())
    access = db.Column(db.String(36), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    def consume_access_code(self, access):
        """
        :type access str
        """

        if self.access == access:
            redis.delete('uat:%s' % access)
            return True
        return False

    @classmethod
    def revoke(cls, access):
        """
        :type access str
        """

        cls.query.filter_by(access=access).delete()
        redis.delete('uat:%s' % access)

    @classmethod
    def revoke_all(cls, user_obj):
        """
        :type user_obj User
        """
        tokens_obj = cls.query.filter_by(user=user_obj)
        for token_obj in tokens_obj:
            redis.delete('uat:%s' % token_obj.access)
        tokens_obj.delete()
