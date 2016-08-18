# -*- coding: utf-8 -*-
from flask import request, current_app, url_for, jsonify
from flask.ext.sqlalchemy import BaseQuery
from functools import wraps


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


def create_paginate(app):
    def paginate(key, max_per_page, **key_word_args):
        """
        @apiDefine Paginate
        @apiSuccess {Object} meta Pagination meta data.
        @apiSuccess {Url} meta.first Url for first page of results
        @apiSuccess {Url} meta.last Url for last page of results
        @apiSuccess {Url} meta.next Url for next page of results
        @apiSuccess {Url} meta.prev Url for previous page of results
        @apiSuccess {int} meta.page number of the current page
        @apiSuccess {int} meta.pages all pages count
        @apiSuccess {int} meta.per_page item per each page
        @apiSuccess {int} meta.total count of all items
        """

        def decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                query = f(*args, **kwargs)
                page = request.args.get('page', 1, type=int)

                per_page = min(request.args.get('per_page', app.config['PAGE_SIZE'], type=int),
                               max_per_page)

                if not isinstance(query, BaseQuery):
                    return f(*args, **kwargs)

                pagination_obj = query.paginate(page, per_page)
                meta = {'page': pagination_obj.page, 'per_page': pagination_obj.per_page,
                        'total': pagination_obj.total, 'pages': pagination_obj.pages}

                if pagination_obj.has_prev:
                    meta['prev'] = url_for(request.endpoint, page=pagination_obj.prev_num,
                                           per_page=per_page,
                                           _external=True, **kwargs)
                else:
                    meta['prev'] = None

                if pagination_obj.has_next:
                    meta['next'] = url_for(request.endpoint, page=pagination_obj.next_num,
                                           per_page=per_page,
                                           _external=True, **kwargs)
                else:
                    meta['next'] = None

                meta['first'] = url_for(request.endpoint, page=1,
                                        per_page=per_page, _external=True,
                                        **kwargs)
                meta['last'] = url_for(request.endpoint, page=pagination_obj.pages,
                                       per_page=per_page, _external=True,
                                       **kwargs)

                return jsonify({
                    str(key): [item.to_json(**key_word_args) for item in pagination_obj.items],
                    'meta': meta
                })

            return wrapped

        return decorator

    return paginate
