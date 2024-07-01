from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from src.config import DevelopmentConfig, TestingConfig, ProductionConfig

db = SQLAlchemy()
load_dotenv()

def create_app(config_name=None):
    app = Flask(__name__)

    if config_name == "development":
        app.config.from_object(DevelopmentConfig)
    elif config_name == "test":
        app.config.from_object(TestingConfig)
    elif config_name == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'
        app.config['DEBUG'] = True
    
    config_classes = {
        "development": DevelopmentConfig,
        "test": TestingConfig,
        "production": ProductionConfig
    }

    if config_name in config_classes:
        app.config.from_object(config_classes[config_name])
    else:
        raise ValueError("Invalid configuration name")

    db.init_app(app)
    return app

