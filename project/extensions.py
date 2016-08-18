# -*- coding: utf-8 -*-

from flask.ext.cache import Cache
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.redis import FlaskRedis
from flask.ext.admin import Admin

__all__ = ['cache', 'db', 'admin']

cache = Cache()
db = SQLAlchemy()
migrate = Migrate()
redis = FlaskRedis()
admin = Admin(template_mode='bootstrap3', url='/admin')
