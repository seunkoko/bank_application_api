import os
from os.path import join, dirname

try:
    from pathlib import Path
    from dotenv import load_dotenv

    env_path = Path('.') / '.env'
    base_dir = Path('.')
except:
    from dotenv import load_dotenv

    env_path = join(dirname(__file__), '.env')
    base_dir = dirname(__file__)

load_dotenv(env_path)


class Config(object):
    BASE_DIR = base_dir
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')


class DevelopmentConfiguration(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')


class TestingConfiguration(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI  = "sqlite:///" + str(Config.BASE_DIR) \
                              + "/test/test_db.sqlite"


app_configuration = {
    'production': Config,
    'development': DevelopmentConfiguration,
    'testing': TestingConfiguration
}
