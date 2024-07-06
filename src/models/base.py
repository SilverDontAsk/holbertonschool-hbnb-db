from datetime import datetime
from typing import Any, Optional
import uuid
from src import db

class Base(db.Model):
    """
    Base class for all models.
    """

    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(
        self,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs,
    ) -> None:
        """
        Base class constructor.
        If kwargs are provided, set them as attributes.
        """
        super().__init__(**kwargs)
        self.id = str(id or uuid.uuid4())
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    @classmethod
    def get(cls, id) -> Optional[Any]:
        """
        Common method to get a specific object of a class by its id.
        """
        return cls.query.get(id)

    @classmethod
    def get_all(cls) -> list[Any]:
        """
        Common method to get all objects of a class.
        """
        return cls.query.all()

    @classmethod
    def delete(cls, id) -> bool:
        """
        Common method to delete a specific object of a class by its id.
        """
        obj = cls.get(id)
        if not obj:
            return False
        db.session.delete(obj)
        db.session.commit()
        return True

    def to_dict(self) -> dict:
        """
        Returns the dictionary representation of the object.
        This should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    def create(data: dict) -> Any:
        """
        Creates a new object of the class.
        This should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    def update(entity_id: str, data: dict) -> Optional[Any]:
        """
        Updates an object of the class.
        This should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")
