from functools import wraps

from flask import g, request, jsonify
from flask_jwt import jwt


# define a user class
class CurrentUser(object):
    def __init__(self, user_id):
        self.id = user_id

    def __repr__(self):
        return ("<CurrentUser \n"
                "id - {0} \n>").format(self.id)

# authorization decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # check that the Authorization header is set
        authorization_token = request.headers.get('Authorization')
        if not authorization_token:
            response = jsonify({
                "status": "fail",
                "data": {
                    "message": "Bad request. Header does not contain"
                            " authorization token"
                }
            })
            response.status_code = 400
            return response

        # validates the word bearer is in the token
        if 'bearer ' not in authorization_token.lower():
            response = jsonify({
                "status": "fail",
                "data": {
                    "message": "Invalid Token. The token should begin with"
                            " 'Bearer '"
                }
            })
            response.status_code = 400
            return response

        # predefining unauthorized_response
        unauthorized_response = jsonify({
            "status": "fail",
            "data": {
                "message": "Unauthorized. The authorization token supplied"
                        " is invalid"
            }
        })
        unauthorized_response.status_code = 401

        try:
            # extracts token by removing bearer
            authorization_token = authorization_token.split(' ')[1]

            # decode token
            payload = jwt.decode(authorization_token, 'secret',
                                 options={"verify_signature": False})
        except jwt.InvalidTokenError:
            return unauthorized_response
        
        # convert payload keys from unicode to string
        payload_keys = [str(key) for key in payload.keys()]
        
        # confirm that payload has required keys
        if not {"id"}.issubset(payload_keys):
            return unauthorized_response
        else:
            # instantiate user object
            current_user = CurrentUser(
                    str(payload["id"])
                )

            # set current user in flask global variable, g
            g.current_user = current_user

            # now return wrapped function
            return f(*args, **kwargs)
    return decorated
