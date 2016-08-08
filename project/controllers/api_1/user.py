# -*- coding: utf-8 -*-

# project imports
from flask import request, jsonify
from project import app
from project.models import User
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
        description: info for signup
        required: true
        schema:
          id: Signup
          required:
            - name
            - password
            - email
            -
          properties:
            name:
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
    json = request.json

    return '', 201


@app.api_route('/user/login/', methods=['POST'])
@api_validate_schema('user.login_schema')
def login():
    """
    Login
    ---
    tags:
      - user
    parameters:
      - name: body
        in: body
        description: username and password for login
        required: true
        schema:
          id: UserLogin
          required:
            - login
            - password
          properties:
            login:
              type: string
              example: babyknight
              description: Username or Email
            password:
              type: string
              example: baby123
    responses:
      200:
        description: Successfully logged in
        schema:
          type: object
          properties:
            token:
              type: string
              description: Generated RESTful token
      400:
          description: Bad request
      404:
        description: User does not exist
      406:
          description: Wrong password
    """

    data = request.json
    login = data['login']
    password = data['password']

    if '@' in login:
        user_obj = User.query.filter_by(email=login).first()
    else:
        user_obj = User.query.filter_by(username=login).first()

    if not user_obj:
        return jsonify(errors='user does not exist'), 404
    if user_obj.verify_password(password):
        return jsonify(token=generate_token(dict(user_id=user_obj.id))), 200

    return jsonify(errors='wrong password'), 406


@app.api_route('/user/signup/', methods=['POST'])
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
        description: username, email and password for signup
        required: true
        schema:
          id: UserSignup
          required:
            - name
            - email
            - password
            - phone
            - student_id
            - university
            - national_code
          properties:
            name:
              type: string
              example: honey
            email:
              type: string
              example: baby@knight.org
            password:
              type: string
              example: baby123
              minLength: 3
              maxLength: 32
            phone:
              type: string
              length: 11
              pattern: ^09[0-9]{9}$
            student_id

    responses:
      201:
        description: Successfully registered
      400:
          description: Bad request
      406:
          description: Username or email already exists
    """

    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']

    if User.query.filter_by(email=email).first():
        return jsonify(errors='email already exists'), 406

    try:
        user_obj = User(username=username, email=email)
        user_obj.hash_password(password)
        db.session.add(user_obj)
        db.session.commit()
    except IntegrityError:
        return jsonify(errors='username already exists'), 406

    return '', 201