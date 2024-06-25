"""
Amenity related functionality
"""
from src import db
from src.models.base import Base


class Amenity(Base, db.Model):
    """Amenity representation"""

    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __init__(self, name: str, **kwargs) -> None:
        """Dummy init"""
        super().__init__(**kwargs)

        self.name = name

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Amenity {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Amenity":
        """Create a new amenity"""
        from src.persistence import repo

        amenity = Amenity(**data)
        db.session.add(amenity)
        db.session.commit()
        return amenity

    @staticmethod
    def update(amenity_id: str, data: dict) -> "Amenity | None":
        """Update an existing amenity"""
        amenity = Amenity.query.get(amenity_id)
        if not amenity:
            return None

        for key, value in data.items():
            setattr(amenity, key, value)
        db.session.commit()

        return amenity


class PlaceAmenity(Base):
    """PlaceAmenity representation"""

    __tablename__ = 'place_amenities'

    id = db.Column(db.String(36), primary_key=True)
    place_id = db.Column(db.String(36), nullable=False)
    amenity_id = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __init__(self, place_id: str, amenity_id: str, **kwargs) -> None:
        """Dummy init"""
        super().__init__(**kwargs)

        self.place_id = place_id
        self.amenity_id = amenity_id

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<PlaceAmenity ({self.place_id} - {self.amenity_id})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "amenity_id": self.amenity_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def get(place_id: str, amenity_id: str) -> "PlaceAmenity | None":
        """Get a PlaceAmenity object by place_id and amenity_id"""

        return PlaceAmenity.query.filter_by(place_id=place_id, amenity_id=amenity_id).first()

    @staticmethod
    def create(data: dict) -> "PlaceAmenity":
        """Create a new PlaceAmenity object"""
        from src.persistence import repo

        new_place_amenity = PlaceAmenity(**data)
        db.session.add(new_place_amenity)
        db.session.commit()

        return new_place_amenity

    @staticmethod
    def delete(place_id: str, amenity_id: str) -> bool:
        """Delete a PlaceAmenity object by place_id and amenity_id"""
        from src.persistence import repo

        place_amenity = PlaceAmenity.get(place_id, amenity_id)

        if not place_amenity:
            return False
        db.session.delete(place_amenity)
        db.session.commit()

        return True

    @staticmethod
    def update(entity_id: str, data: dict):
        """Not implemented, isn't needed"""
        raise NotImplementedError(
            "This method is defined only because of the Base class"
        )
