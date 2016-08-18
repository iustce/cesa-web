# -*- coding: utf-8 -*-

import subprocess

from flask import current_app
from flask.ext.script import Manager, prompt_bool

from project.extensions import db, redis

manager = Manager(usage="Perform database operations")


@manager.command
def drop():
    """Drops database tables"""
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        #redis.flushdb()


@manager.command
def create():
    """Creates database tables from sqlalchemy models"""
    db.create_all()


@manager.command
def recreate():
    """
    Recreates database tables (same as issuing 'drop' and then 'create')
    """
    drop()
    create()

@manager.command
def backup():
    """
    create backup file in db.backup
    """
    subprocess.call(['pg_dump %s > db.backup' % current_app.config['DATABASE_NAME']], shell=True)


@manager.command
def restore():
    """
    restore backup file from db.backup
    """
    drop()
    if subprocess.call(['psql %s < db.backup' % current_app.config['DATABASE_NAME']], shell=True):
        print "\n" + "*" * 22 + " ERROR " + "*" * 22
        print "*" * 51 + "\n"
        print "please create db.backup file like db_backup.example"
        print "if you want restore from db_backup.example run this"
        print "database restore_example"
        print "\n" + "*" * 51 + "\n"


@manager.command
def restore_example():
    """
    restore backup file from db_backup.example
    """
    drop()
    subprocess.call(['psql myteam < db_backup.example'], shell=True)


@manager.command
def populate():
    pass


@manager.command
def test():
    """Use it for test purpose"""
    pass
