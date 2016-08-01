# -*- coding: utf-8 -*-

import os
import glob
import pkgutil


__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py")]
__all__ += [os.path.basename(f) for f in glob.glob(os.path.dirname(__file__) + "/api_*")]



def find_schemas():
	from good import Schema
	schemas = {}
	for loader, name, is_pkg in pkgutil.walk_packages(__path__):
		module = loader.find_module(name).load_module(name)
		for each in dir(module):
			attr = getattr(module, each)
			if isinstance(attr, Schema):
				schema_name = name + '.' + each
				schemas[schema_name] = attr
	return schemas
