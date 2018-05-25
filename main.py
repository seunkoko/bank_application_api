import os
from os.path import join, dirname

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restful import Api
try:
    from pathlib import Path
    from dotenv import load_dotenv

    env_path = Path('.') / '.env'
except:
    from dotenv import load_dotenv

    env_path = join(dirname(__file__), '.env')

load_dotenv(env_path)


"""
    Import transfer resource 
"""
try:
    from config import app_configuration
    from api.views.user import (
        UserSignupResource, UserLoginResource, UserResource
    )
    from api.views.transaction import (
        DepositResource, WithdrawResource
    )
except ImportError:
    from bank_application_api.config import app_configuration
    from bank_application_api.api.views.user import (
        UserSignupResource, UserLoginResource, UserResource
    )
    from bank_application_api.api.views.transaction import (
        DepositResource, WithdrawResource
    )

# function that creates the flask app, initializes the db and sets the routes
def create_flask_app(environment):
    app = Flask(__name__)
    app.config.from_object(app_configuration[environment])
    app.config['BUNDLE_ERRORS'] = True

    try:
        from api import models
    except ImportError:
        from bank_application_api.api import models

    # initialize SQLAlchemy
    models.db.init_app(app)

    # initilize migration commands
    migrate = Migrate(app, models.db)

    # initilize api resources
    api = Api(app)

    environment = os.getenv('FLASK_CONFIG')

    # Landing route
    @app.route('/')
    def index():
        return "Welcome to the Banking Application Api"

    ##
    ## Api endpoints with flask-restful 
    api.add_resource(UserSignupResource, '/signup', '/signup/', endpoint='user_signup')
    api.add_resource(UserLoginResource, '/login', '/login/', endpoint='user_login')
    api.add_resource(UserResource, '/user', '/user/', endpoint='user')
    api.add_resource(DepositResource, '/deposit', '/deposit/', endpoint='user_deposit')
    api.add_resource(WithdrawResource, '/withdraw', '/withdraw/', endpoint='user_withdraw')
    """
    Add transfer resource endpoint
    """

    # handle default 404 exceptions with a custom response
    @app.errorhandler(404)
    def resource_not_found(error):
        response = jsonify(dict(status='fail', data={
                    'error':'Not found', 
                    'message':'The requested URL was not found on the server.'
                }))
        response.status_code = 404
        return response

    # handle default 500 exceptions with a custom response
    @app.errorhandler(500)
    def internal_server_error(error):
        response = jsonify(dict(status=error, data={
                    'error':'Internal Server Error', 
                    'message':'The server encountered an internal error and was unable to complete your request.'
                }))
        response.status_code = 500
        return response

    return app

# creates the flask application
app = create_flask_app(os.getenv('FLASK_CONFIG'))

# starts the flask application
if __name__ == "__main__":
    app.run()
