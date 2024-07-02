import os

class Config:
    """This would be the base config"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'supersecretkey' or 'idkdontask'
    
class DevelopmentConfig(Config):
    """Dev config"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    
class TestingConfig(Config):
    """Testing config"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = False
    WTF_CSRF_ENABLED = False
    
class ProductionConfig(Config):
    """Production config"""
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///prod.db'
    
    
config_by_name = dict(
    development=DevelopmentConfig,
    test=TestingConfig,
    production=ProductionConfig
)