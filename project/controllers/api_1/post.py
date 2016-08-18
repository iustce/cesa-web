# -*- coding: utf-8 -*-

# project imports
from flask import request, jsonify, abort
from project import app
from project.extensions import db
from project.models import Post


@app.api_route('/post', methods=['GET'])
@app.paginate('posts', 10)
def get_posts():
    """
    GetAllPosts
    ---
    tags:
      - post
    parameters:
      - name: body
        in: body
        description: get all posts sorted by date and degree of importance
    responses:
      200:
        description: posts info
        schema:
          type: object
          properties:
            posts:
              type: object
              properties:
                id :
                  type : integer
                title:
                  type : string
                body:
                  type : string
                last_modified:
                  type : string
                importance:
                  type : integer
                files:
                  type : object
                  properties:
                      id:
                        type : integer
                      url:
                        type : string
                      path:
                        type : string
                      kind:
                        type : integer
    """
    return Post.query.order_by('last_modified')


@app.api_route('/post/<int:post_id>', methods=['GET'])
def post_details(post_id):
    """
    PostDetail
    ---
    tags:
      - post
    parameters:
      - name: body
        in: body
        description: get a post detail
    responses:
      200:
        description: posts info
        schema:
          type: object
          properties:
            id :
              type : integer
            title:
              type : string
            body:
              type : string
            last_modified:
              type : string
            importance:
              type : integer
            files:
              type : object
              properties:
                  id:
                    type : integer
                  url:
                    type : string
                  path:
                    type : string
                  kind:
                    type : integer
      404:
        description: Post does not exist

    """

    post_obj = Post.query.get(post_id)
    if not post_obj:
        return abort(404)
    return jsonify(post_obj.to_json()), 200
