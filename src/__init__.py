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

# Import routes
from src.routes import users, auth, amenities, cities, countries, places, reviews

app.register_blueprint(users.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(amenities.bp)
app.register_blueprint(cities.bp)
app.register_blueprint(countries.bp)
app.register_blueprint(places.bp)
app.register_blueprint(reviews.bp)

if __name__ == '__main__':
    app.run()
