# -*- coding: utf-8 -*-

from application import create_app
from config import DefaultConfig

app = create_app(DefaultConfig())

from project.controllers import *
