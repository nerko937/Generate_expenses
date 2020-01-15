from .secret import SECRET_KEY, SQLALCHEMY_DATABASE_URI



class Config:
    CSRF_ENABLED = True
    DEBUG = False
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
