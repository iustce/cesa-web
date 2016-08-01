# -*- coding: utf-8 -*-

# project imports
from project import app

# flask imports
from flask import render_template


@app.route('/')
def index():
	return render_template('index.html')
