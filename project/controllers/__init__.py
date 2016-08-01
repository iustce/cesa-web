# -*- coding: utf-8 -*-

import os
import glob


__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py")]
__all__ += [os.path.basename(f) for f in glob.glob(os.path.dirname(__file__) + "/api_*")]



def find_apis():
	path = __path__[0]
	return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) and name.startswith('api')]
