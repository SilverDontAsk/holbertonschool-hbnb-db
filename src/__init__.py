#!/usr/bin/python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Load configuration from environment variables
app.config.from_object('src.config.' + os.getenv('FLASK_ENV', 'Development').capitalize())

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

from src.routes.auth import auth_bp
from src.routes.amenities import amenities_bp
from src.routes.cities import cities_bp
from src.routes.countries import countries_bp
from src.routes.places import places_bp
from src.routes.reviews import reviews_bp
from src.routes.users import register
    
app.register_blueprint(register, url_prefix='/')
app.register_blueprint(reviews_bp, url_prefix='/')
app.register_blueprint(auth_bp, url_prefix='/')
app.register_blueprint(amenities_bp, url_prefix='/')
app.register_blueprint(cities_bp, url_prefix='/')
app.register_blueprint(countries_bp, url_prefix='/')
app.register_blueprint(places_bp, url_prefix='/')

if __name__ == '__main__':
    app.run()
