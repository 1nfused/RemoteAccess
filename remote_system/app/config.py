import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    SECRET_KEY = 'Se, cr, et!'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SITE_WIDTH = 800

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True