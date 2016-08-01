# -*- coding: utf-8 -*-

from good import Schema, All, Required, Length, Match, Email


signup_schema = Schema({
						Required('username'): All(unicode, Match(r'^[\w.]+$')),
						Required('email'): Email(),
						Required('password'): All(unicode, Length(min=5))
					   })
