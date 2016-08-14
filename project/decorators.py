# -*- coding: utf-8 -*-


def create_api_route(app):
    def api_route(rule, **options):
        def decorator(f):
            mod = f.__module__.split('.')[:3]
            api_version = '_'.join(mod[2].split('_')[1:])
            ####################
            new_rule = '/api/' + ('v%s' % api_version) + rule
            endpoint = options.pop('endpoint', None)
            if not endpoint:
                endpoint = '.'.join(f.__module__.split('.')[2:]) + '.' + f.__name__
            app.add_url_rule(new_rule, endpoint, f, **options)
            return f

        return decorator

    return api_route
