# -*- coding: utf-8 -*-

# project imports
from project import app
from project.utils.validators import api_validate_schema


@app.api_route('/user/')
def get_user():
	"""
    Get user info
    This ednpoint does nothing
    Only returns "2"
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
              default: '2'
    """
	return '2', 200


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
        description: username, email and password for signup
        required: true
        schema:
          id: Signup
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
              pattern: ^[\w.]+$
              example: babyknight
            email:
              type: string
              example: baby@knight.com
            password:
              type: string
              example: baby123
              minLength: 5
    responses:
      201:
        description: Created
      406:
      	description: Invalid input
    """
	return '', 201
