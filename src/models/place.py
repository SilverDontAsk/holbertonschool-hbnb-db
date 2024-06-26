"""
Place related functionality
"""

from src.models.city import City
from src.models.user import User
from src import db
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Place(db.Model):
    """Place representation"""

    __tablename__ = 'places'

    id = Column(db.String(36), primary_key=True)
    name = Column(String(120), nullable=False)
    description = Column(String(500), nullable=True)
    address = Column(String(250), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    host_id = Column(String, ForeignKey('users.id'), nullable=False)
    city_id = Column(String, ForeignKey('cities.id'), nullable=False)
    price_per_night = Column(Integer, nullable=False)
    number_of_rooms = Column(Integer, nullable=False)
    number_of_bathrooms = Column(Integer, nullable=False)
    max_guests = Column(Integer, nullable=False)
    created_at = Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = Column(db.DateTime, onupdate=db.func.current_timestamp())

    host = relationship('User', back_populates='places')
    city = relationship('City', back_populates='places')

    def __init__(self, data: dict | None = None, **kwargs) -> None:
        """Initialization"""
        super().__init__(**kwargs)

        if data:
            self.name = data.get("name", "")
            self.description = data.get("description", "")
            self.address = data.get("address", "")
            self.city_id = data["city_id"]
            self.latitude = float(data.get("latitude", 0.0))
            self.longitude = float(data.get("longitude", 0.0))
            self.host_id = data["host_id"]
            self.price_per_night = int(data.get("price_per_night", 0))
            self.number_of_rooms = int(data.get("number_of_rooms", 0))
            self.number_of_bathrooms = int(data.get("number_of_bathrooms", 0))
            self.max_guests = int(data.get("max_guests", 0))

    def __repr__(self) -> str:
        """Representation"""
        return f"<Place {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "city_id": self.city_id,
            "host_id": self.host_id,
            "price_per_night": self.price_per_night,
            "number_of_rooms": self.number_of_rooms,
            "number_of_bathrooms": self.number_of_bathrooms,
            "max_guests": self.max_guests,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Place":
        """Create a new place"""
        user: User | None = User.query.get(data["host_id"])
        if not user:
            raise ValueError(f"User with ID {data['host_id']} not found")

        city: City | None = City.query.get(data["city_id"])
        if not city:
            raise ValueError(f"City with ID {data['city_id']} not found")

        new_place = Place(data=data)
        db.session.add(new_place)
        db.session.commit()

        return new_place

    @staticmethod
    def update(place_id: str, data: dict) -> "Place | None":
        """Update an existing place"""
        place: Place | None = Place.query.get(place_id)
        if not place:
            return None

        for key, value in data.items():
            setattr(place, key, value)
        db.session.commit()

        return place

