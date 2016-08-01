# -*- coding: utf-8 -*-

from good import Schema, Required


signup_schema = Schema({
						Required('username'): unicode,
						Required('password'): unicode
					   })
