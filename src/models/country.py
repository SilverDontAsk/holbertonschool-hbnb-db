from src import db

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    cities = db.relationship('City', back_populates='country', cascade='all, delete-orphan')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Country {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cities': [city.to_dict() for city in self.cities]
        }
