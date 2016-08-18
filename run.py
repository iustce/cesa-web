# -*- coding: utf-8 -*-

# python imports
import os
import subprocess
import sys, traceback
from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager
from database import manager as database_manager

try:
    from project import app
    from project.application import configure_app
    from project.config import DefaultConfig, DevelopmentConfig, ProductionConfig
except ImportError:
    print ' *** please install/update requirements or fix the problem ***'
    traceback.print_exc(file=sys.stdout)
    exit(0)

manager = Manager(app)
manager.add_command('database', database_manager)
manager.add_command('migration', MigrateCommand)

fwpath = os.path.abspath(os.path.dirname(__file__))
venv_dir = os.path.join(fwpath, 'venv')


@manager.command
def run():
    configure_app(app, DevelopmentConfig())

    app.run(host='0.0.0.0', port=5000)


@manager.command
def import_local_config_file(filename):
    if not os.path.isabs(filename):
        filename = os.path.join(os.getcwd(), filename)
    configure_app(app, filename, is_pyfile=True)
    app.run(host='0.0.0.0', port=5000)


@manager.command
def test():
    pass

@manager.command
def update_requirements():
    subprocess.call([os.path.join(venv_dir, 'bin/pip'), 'install', '-r', os.path.join(fwpath, 'requirements')])


if __name__ == '__main__':
    manager.run()
