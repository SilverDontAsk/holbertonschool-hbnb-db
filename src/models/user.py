from src import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """User representation"""

    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    is_admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String, nullable=False)

    def __init__(self, email: str, first_name: str, last_name: str, password: str, **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = generate_password_hash(password)

    def __repr__(self) -> str:
        return f"<User {self.id} ({self.email})>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_admin": self.is_admin,
        }

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get(user_id):
        return User.query.get(user_id)

    @staticmethod
    def create(data):
        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=data['password'],
            is_admin=data.get('is_admin', False)
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(user_id, data):
        user = User.query.get(user_id)
        if user:
            for key, value in data.items():
                if key == 'password':
                    user.password = value
                else:
                    setattr(user, key, value)
            db.session.commit()
        return user

    @staticmethod
    def delete(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
