"""
City related functionality
"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src import db
from src.models.country import Country

class City(db.Model):
    """City representation"""

    __tablename__ = 'cities'

    id = Column(db.String(36), primary_key=True)
    name = Column(String(120), nullable=False)
    country_code = Column(String(3), nullable=False)
    created_at = Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __init__(self, name: str, country_code: str, **kwargs) -> None:
        """Initialization"""
        super().__init__(**kwargs)
        self.name = name
        self.country_code = country_code

    def __repr__(self) -> str:
        """Representation"""
        return f"<City {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "country_code": self.country_code,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "City":
        """Create a new city"""
        country = Country.get(data["country_code"])
        if not country:
            raise ValueError("Country not found")

        city = City(**data)
        db.session.add(city)
        db.session.commit()
        return city

    @staticmethod
    def update(city_id: str, data: dict) -> "City":
        """Update an existing city"""
        city = City.query.get(city_id)
        if not city:
            raise ValueError("City not found")

        for key, value in data.items():
            setattr(city, key, value)
        db.session.commit()

        return city

