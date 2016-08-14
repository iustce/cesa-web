# -*- coding: utf-8 -*-

# project imports
from datetime import datetime
from uuid import uuid4

from flask import request, jsonify, abort
from project import app
from project.extensions import db
from project.models import User, Token
from project.utils.validators import api_validate_schema
from sqlalchemy.exc import IntegrityError


@app.api_route('/user')
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


@app.api_route('/user/login', methods=['POST'])
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
        description: student_id and password for login
        required: true
        schema:
          id: UserLogin
          required:
            - student_id
            - password
          properties:
            student_id:
              type: string
              example: "93522222"
              description: student_id
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
    student_id = data['student_id']
    password = data['password']

    user_obj = User.query.filter_by(student_id=student_id).one()

    if not user_obj:
        return jsonify(errors='user does not exist'), 404

    if user_obj.password == password:
        access_token = user_obj.generate_access_token()
        token_obj = Token(user=user_obj, access=access_token, refresh=str(uuid4()))
        db.session.add(token_obj)
        db.session.commit()
        return jsonify(access_token=access_token, refresh=token_obj.refresh), 200
    return jsonify(errors='wrong password'), 406


@app.api_route('/user/signup', methods=['POST'])
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
        description: info for signup
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
              Length: 11
              example: 09371234567
              pattern: ^09[0-9]{9}$
            student_id:
              type: string
              Length: 8
              example: 93522222
            university:
              type: string
              enum: ['iust', 'sharif', 'tehran', 'other']
              example: iust
            national_code:
              type: string
              Length: 10
              example: 4361234567

    responses:
      201:
        description: Successfully registered
      400:
          description: Bad request
      406:
          description: unique info already exists
    """

    json = request.json
    email = json['email']

    if User.query.filter_by(email=email).first():
        return jsonify(errors='email already exists'), 406

    try:
        user_obj = User()
        user_obj.populate(json)
        db.session.add(user_obj)
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        if "name" in str(err.orig):
            print "name already exists"
            return "name already exists", 406
        elif "phone" in str(err.orig):
            print "phone already exists"
            return "phone already exists", 406
        elif "student_id" in str(err.orig):
            print "student_id already exists"
            return "student_id already exists", 406

    return jsonify(), 201


@app.api_route('/user/refresh', methods=['POST'])
@api_validate_schema('user.refresh_schema')
def refresh():
    """
    Refresh
    ---
    tags:
      - user
    parameters:
      - name: body
        in: body
        description: generate another access-token
        required: true
        schema:
          id: refresh
          required: true
          properties:
            access:
              type: string
              Length: 36
            refresh:
              type: string
              Length: 36

    responses:
      200:
        description: Successfully generated
        schema:
          properties:
            access:
              type: string
              description: The user access token
      400:
          description: Bad request
      404:
          description: refresh not found
      401:
          description: wrong access
    """

    json = request.json
    token_obj = Token.query.get(json['refresh'])
    if not token_obj:
        abort(404)

    if token_obj.consume_access_code(json['access']):
        token_obj.last_refresh = datetime.now()
        access_token = token_obj.user.generate_access_token()
        token_obj.access = access_token
        db.session.commit()

        return jsonify(access=access_token), 200

    return abort(401)
