"""
Review related functionality
"""

from src.models.place import Place
from src.models.user import User
from src import db


class Review(db.Model):
    """Review representation"""

    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    place = db.relationship('Place', backref=db.backref('reviews', lazy=True))
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))

    def __init__(self, place_id: str, user_id: str, comment: str, rating: float, **kw) -> None:
        """Initialization"""
        super().__init__(**kw)
        self.place_id = place_id
        self.user_id = user_id
        self.comment = comment
        self.rating = rating

    def __repr__(self) -> str:
        """Representation"""
        return f"<Review {self.id} - '{self.comment[:25]}...'>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "comment": self.comment,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Review":
        """Create a new review"""
        user = User.query.get(data["user_id"])
        place = Place.query.get(data["place_id"])

        if not user:
            raise ValueError(f"User with ID {data['user_id']} not found")

        if not place:
            raise ValueError(f"Place with ID {data['place_id']} not found")

        new_review = Review(**data)
        db.session.add(new_review)
        db.session.commit()
        return new_review

    @staticmethod
    def update(review_id: str, data: dict) -> "Review | None":
        """Update an existing review"""
        review = Review.query.get(review_id)

        if not review:
            raise ValueError("Review not found")

        for key, value in data.items():
            setattr(review, key, value)

        db.session.commit()
        return review

