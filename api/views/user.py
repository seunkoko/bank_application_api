import os
import datetime

from flask import g, request, jsonify
from flask_restful import Resource
from flask_jwt import jwt

try:
    from api.models import User
    from api.helper.authorization import token_required
    from api.helper.helper import (
        validate_request_keys, validate_request_type, 
        validate_request_json, bapp_errors, 
        generate_unique_account_number
    )
except ImportError:
    from bank_application_api.api.models import User
    from bank_application_api.api.helper.authorization import token_required
    from bank_application_api.api.helper.helper import (
        validate_request_keys, validate_request_type, 
        validate_request_json, bapp_errors, 
        generate_unique_account_number
    )


class UserSignupResource(Resource):

    @validate_request_json
    def post(self):
        json_input = request.get_json()

        fields = '(account_amount, firstname, lastname, middlename, email and password)'
        if not validate_request_keys(json_input, ['account_amount', 'firstname', 'lastname', 'middlename', 'email', 'password']):
            return bapp_errors(
                'These fields are required on signup {0}'.format(fields), 
                400
            )

        # handling more exceptions
        try:
            _account_amount = float(json_input['account_amount'])
        except:
            return bapp_errors("Your account amount must be a number", 400)
        if _account_amount < 500:
                return bapp_errors(
                    "Sorry, you cannot open an account with less than \u20A6 500.00",
                    400
                )
        _firstname = str(json_input["firstname"])
        _lastname = str(json_input["lastname"])
        _middlename = str(json_input["middlename"])
        _email = str(json_input["email"])
        _password = str(json_input["password"])

        json_input.pop('account_amount', None)
        if not validate_request_type(str, json_input):
            return bapp_errors(
                'None of these fields {0} are allowed to be empty'.format(fields), 
                400
            )

        if User.is_user_data_taken(_email):
            return bapp_errors(
                'Sorry, this email is already taken', 
                400
            )

        new_user = User(
            firstname=_firstname,
            middlename=_middlename,
            lastname=_lastname,
            email=_email,
            password=_password,
            account_amount=_account_amount,
            account_number=generate_unique_account_number()
        )
        new_user.save()

        payload = {
                    "id": new_user.id
                }
        _token = jwt.encode(payload, os.getenv("TOKEN_KEY"), algorithm='HS256').decode("utf-8") 

        return {
            'status': 'success',
            'data': {
                'user': new_user.serialize(), 
                'message': 'User created succesfully',
                'token': _token
            }
        }, 201


class UserLoginResource(Resource):
    
    @validate_request_json
    def post(self):
        json_input = request.get_json()

        fields = '(email and password)'
        if not validate_request_keys(json_input, ['email', 'password']):
            return bapp_errors(
                'These fields are required on login {0}'.format(fields), 
                400
            )

        _email = str(json_input["email"])
        _password = str(json_input["password"])
        if not validate_request_type(str, json_input):
            return bapp_errors(
                'None of these fields {0} are allowed to be empty'.format(fields), 
                400
            )
        
        _user = User.query.filter(User.email==_email).first()
        if not _user:
            return bapp_errors(
                'User does not exist', 
                404
            )

        if not _user.check_password(_password):
            return bapp_errors("Your password is incorrect, please try again", 401)

        payload = {
                    "id": _user.id
                }
        _token = jwt.encode(payload, os.getenv("TOKEN_KEY"), algorithm='HS256').decode("utf-8") 

        return {
            'status': 'success',
            'data': {
                'user': _user.serialize(), 
                'message': 'User login succesfull',
                'token': _token
            }
        }, 200


class UserResource(Resource):
    
    @token_required
    def get(self):
        # to prevent tokens with string ids from breaking the app
        try:
            _user_id = int(g.current_user.id)
        except:
            return bapp_errors("User does not exist", 404)

        _user = User.query.get(int(g.current_user.id))
        if not _user:
            return bapp_errors("User does not exist", 404)

        return {
            'status': 'success',
            'data': {
                'user': _user.serialize(),
                'message': 'User information retrieved succesfully',
            }
        }, 200
        
    
    @token_required
    @validate_request_json
    def put(self):
        json_input = request.get_json()
        
        for key in json_input.keys():
            if key in ["email", "account_amount", "account_number"]:
                return bapp_errors(
                    'Sorry, emails, amounts and account numbers cannot be updated', 
                    400
                )

        if not validate_request_type(str, json_input):
            return bapp_errors(
                'Request body should not contain null values', 
                400
            )

        # to prevent tokens with string ids from breaking the app
        try:
            _user_id = int(g.current_user.id)
        except:
            return bapp_errors("User does not exist", 404)

        _user = User.query.get(int(g.current_user.id))
        if not _user:
            return bapp_errors("User does not exist", 404)

        # update user information
        for key in json_input.keys():
            if key == 'password':
                if _user.check_password(json_input['password']):
                    return bapp_errors(
                        'Unauthorized, you cannot update with the same password', 
                        401
                    )
            _user.__setitem__(key, json_input[key])
        _user.save()

        return {
            'status': 'success',
            'data': {
                'user': _user.serialize(),
                'message': 'User information updated succesfully',
            }
        }, 200
