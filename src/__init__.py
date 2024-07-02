from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
from src.config import config_by_name

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
load_dotenv()

def create_app(config_name=None):
    app = Flask(__name__)

    config_name = config_name or 'development'

    if config_name in config_by_name:
        app.config.from_object(config_by_name[config_name])
    else:
        raise ValueError(f"Invalid configuration name: {config_name}")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints
    from src.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/')

    return app
