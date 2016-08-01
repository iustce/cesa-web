# -*- coding: utf-8 -*-

# python imports
from functools import wraps
from good import Invalid
import collections

# project imports
from project import app

# flask imports
from flask import request, jsonify


def validate_schema(schema_name, api=False):
	def wrapper(f):
		@wraps(f)
		def decorated(*args, **kwargs):
			api_dir = ''
			if api:
				api_dir = f.__module__.split('.')[2] + '.'
			schema = app.schemas[api_dir + schema_name]
			#########################
			json = request.json or {}
			try:
				schema(json)
			except Invalid as ee:

				def update(d, u):
					for k, v in u.iteritems():
						if isinstance(v, collections.Mapping):
							r = update(d.get(k, {}), v)
							d[k] = r
						else:
							d[k] = u[k]
					return d

				def get_errors():
					errors = {}
					for e in ee:
						main = each = {}
						for p in e.path:
							prev = each
							each[p] = {}
							each = each[p]
						prev[prev.keys()[0]] = e.message
						update(errors, main)
					return errors

				if app.config['TESTING']:
					return jsonify(errors=get_errors()), 406
				return '', 406

			return f(*args, **kwargs)
		return decorated
	return wrapper


def api_validate_schema(schema_name):
	return validate_schema(schema_name, True)

