from src import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    place = db.relationship('Place', backref=db.backref('reviews', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'text': self.comment,
            'rating': self.rating
        }
