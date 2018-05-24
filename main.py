import os

from flask import Flask, jsonify
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

try:
    from config import app_configuration
except ImportError:
    from bank_application_api.config import app_configuration

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

    environment = os.getenv('FLASK_CONFIG')

    # Landing route
    @app.route('/')
    def index():
        return "Welcome to the Banking Application Api"

    return app

# starts the flask application
app = create_flask_app(os.getenv('FLASK_CONFIG'))
if __name__ == "__main__":
    app.run()
