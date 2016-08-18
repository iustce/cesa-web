# -*- coding: utf-8 -*-

from flask import Flask
from project.extensions import admin, db


def create_app(config):
    app = Flask(config.DEFAULT_APP_NAME)
    configure_app(app, config)
    configure_extensions(app)
    append_decorators(app)
    load_schemas(app)
    configure_apidoc(app)
    configure_admin(app)
    return app


def configure_app(app, config, is_pyfile=False):
    if is_pyfile:
        app.config.from_pyfile(config)
    else:
        app.config.from_object(config)

    app.config.from_pyfile('environ.py', silent=True)


def configure_extensions(app):
    from project import extensions

    for extension in extensions.__all__:
        try:
            getattr(extensions, extension).init_app(app)
        except AttributeError as e:
            print e, 646864
    extensions.redis.init_app(app, strict=True)
    extensions.migrate.init_app(app, extensions.db)


def append_decorators(app):
    from decorators import create_api_route
    from decorators import create_paginate

    app.api_route = create_api_route(app)
    app.paginate = create_paginate(app)


def load_schemas(app):
    from project.schemas import find_schemas
    app.schemas = find_schemas()


def configure_apidoc(app):
    def get_specs():
        def get_spec_config(api):
            ver = '_'.join(api.split('_')[1:])
            return dict(version=ver,
                        title='Api v' + ver,
                        endpoint='spec_' + api,
                        route='/docs/api/v%s' % ver,
                        rule_filter=lambda rule: rule.endpoint.startswith(api))

        from project.controllers import find_apis
        return [get_spec_config(api) for api in find_apis()]

    from flasgger import Swagger
    app.config['SWAGGER'] = {"swagger_version": "2.0", "specs": get_specs()}
    Swagger(app)


def configure_admin(app):
    import project.models

    from project.admin import AdminFile
    from project.admin import UserModelView
    from project.admin.posts import PostModelView
    from project.admin.courses import CourseModelView

    admin.add_view(UserModelView(project.models.User, db.session, name='Users',
                                 endpoint='admin.users', url='/admin/users'))

    admin.add_view(PostModelView(project.models.Post, db.session, name='Posts',
                                 endpoint='admin.posts', url='/admin/posts'))

    admin.add_view(CourseModelView(project.models.Course, db.session, name='Courses',
                                 endpoint='admin.courses', url='/admin/courses'))

    #admin.add_view(AdminFile(app.config['MEDIA_DIR'], endpoint="admin.media", url='/admin/media', name='MediaFiles'))
