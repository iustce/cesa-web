# -*- coding: utf-8 -*-

# project imports
from project import app
from project.utils.validators import api_validate_schema


@app.api_route('/user/')
def get_user():
    """
    Get user info
    This endpoint does nothing
    Only returns "1"
    ---
    tags:
      - user
    responses:
      200:
        description: User info
        schema:
          properties:
            result:
              type: string
              description: The user info
              default: '1'
    """

    return '1', 200


@app.api_route('/user/', methods=['POST'])
@api_validate_schema('user.signup_schema')
def signup():
    """
    Signup
    ---
    tags:
      - user
    parameters:
      - name: body
        in: body
        type: object
        description: username and password for signup
        required: true
        schema:
          id: Signup
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: username of user
            password:
              type: string
              description: password of user
    responses:
      201:
        description: Created
      406:
        description: Invalid input
    """

    return '', 201
