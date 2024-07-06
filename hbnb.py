# hbnb.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

env = os.getenv('ENV', 'development')

# Determine configuration based on environment
if env == 'production':
    from src.config import ProductionConfig as Config
else:
    from src.config import DevelopmentConfig as Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Import routes to register them with the app
from src.routes import users
app.register_blueprint(users)

if Config.SQLALCHEMY_DATABASE_URI.startswith('sqlite:///'):
    database_path = Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
    if not os.path.exists(database_path):
        print(f"Creating SQLite database at {database_path}")
        with app.app_context():
            db.create_all()

if __name__ == '__main__':
    app.run()
