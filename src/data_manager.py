from flask_sqlalchemy import SQLAlchemy
from src.models.user import User

class DataManager:
    def __init__(self, app):
        self.app = app
        self.db = SQLAlchemy(app)

    def save_user(self, user):
        if self.app.config['USE_DATABASE']:
            self.db.session.add(user)
            self.db.session.commit()
        else:
            with open('users.txt', 'a') as f:
                f.write(f"{user.username},{user.email}\n")

    def get_user(self, username):
        if self.app.config['USE_DATABASE']:
            return self.db.session.query(User).filter_by(username=username).first()
        else:
            with open('users.txt', 'r') as f:
                for line in f.readlines():
                    user_data = line.strip().split(',')
                    if user_data[0] == username:
                        return User(username=user_data[0], email=user_data[1])
                return None
