# hbnb.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from src.routes.users import register

load_dotenv()

env = os.getenv('ENV', 'development')

if env == 'production':
    from src.config import Production as Config
else:
    from src.config import Development as Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

app.register_blueprint(register(), url_prefix='/users')

if Config.SQLALCHEMY_DATABASE_URI.startswith('sqlite:///'):
    database_path = Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
    if not os.path.exists(database_path):
        print(f"Creating SQLite database at {database_path}")
        with app.app_context():
            db.create_all()

if __name__ == '__main__':
    app.run()
