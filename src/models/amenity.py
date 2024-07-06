from src import db

class Amenity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Amenity {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
