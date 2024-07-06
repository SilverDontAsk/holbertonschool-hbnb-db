import os
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Determine which configuration to use
env = os.getenv('ENV', 'development')

if env == 'production':
    from src.config import ProductionConfig as Config
else:
    from src.config import DevelopmentConfig as Config

# Initialize SQLAlchemy outside of fixtures
app = Flask(__name__)
app.config.from_object(Config)
app.config['TESTING'] = True
db = SQLAlchemy(app)

# Ensure database exists for SQLite
if Config.SQLALCHEMY_DATABASE_URI.startswith('sqlite:///'):
    database_path = Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
    if not os.path.exists(database_path):
        with app.app_context():
            db.create_all()

@pytest.fixture(scope='module')
def test_app():
    """Return the Flask app instance."""
    return app

@pytest.fixture(scope='module')
def test_client(test_app):
    """A test client for the app."""
    return test_app.test_client()

@pytest.fixture(scope='module')
def init_database(test_app):
    """Create a clean database for testing."""
    with test_app.app_context():
        db.create_all()

    yield db

    # Drop all tables after each test
    with test_app.app_context():
        db.drop_all()
