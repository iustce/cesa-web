# -*- coding: utf-8 -*-

# python imports
import random
import string
import os


data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')


class DefaultConfig(object):
	DEFAULT_APP_NAME = 'project'
	DEBUG = True
	TESTING = True
	SECRET_KEY = 'babyknight'
	TOKEN_EXPIRE_TIME = 3600 * 24 * 3

	# CACHE
	CACHE_TYPE = 'filesystem'
	CACHE_DEFAULT_TIMEOUT = 10
	CACHE_THRESHOLD = 100
	CACHE_DIR = os.path.join(data_dir, 'cache')
	CACHE_NO_NULL_WARNING = True


class DevelopmentConfig(DefaultConfig):
	SECRET_KEY = 'Sm9obiBTY2hyb20ga2lja3MgYXNz'
	TESTING = False


class ProductionConfig(DevelopmentConfig):
	DEBUG = False
