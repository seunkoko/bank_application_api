from functools import wraps
from random import randint

from flask import request

from ..models import User


# helper functions

def bapp_errors(errors, status_code):
    return {
        'status': 'fail',
        'data': { 'message': errors }
    }, status_code

def validate_request_json(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        if not request.json:
            return {"status": "fail",
                    "data": {"message": "Request must be a valid JSON"}
                    }, 400

        return f(*args, **kwargs)

    return decorated


def validate_request_keys(data, keys):
    for key in keys:
        if key not in data.keys():
            return False

    return True

def validate_request_type(data):
    for key in data.keys():
        # exception added for tests which come in as unicode
        if not isinstance(data[key], str) and not isinstance(data[key], unicode):
            return False

        if str(data[key]).strip() == '':
            return False

    return True

def generate_unique_account_number():
    account_number = None

    # runs until a unique account number is generated
    while not account_number:
        range_start = 10**(9-1)
        range_end = (10**9)-1
        generated_number = '4' + str(randint(range_start, range_end))
        _number_found = User.query.filter(User.account_number==generated_number).first()

        if not _number_found:
            account_number = generated_number

    return account_number
