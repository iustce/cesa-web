# -*- coding: utf-8 -*-

from flask.ext.cache import Cache
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.redis import FlaskRedis

__all__ = ['cache', 'db']

cache = Cache()
db = SQLAlchemy()
migrate = Migrate()
redis = FlaskRedis()