"""
Country related functionality
"""

from src import db


class Country:
    """
    Country representation

    This class does NOT inherit from Base, you can't delete or update a country

    This class is used to get and list countries
    """

    __tablename__ = 'countries'

    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(3), unique=True, nullable=False)

    def __init__(self, name: str, code: str, **kw) -> None:
        """Dummy init"""
        super().__init__(**kw)
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Country {self.code} ({self.name})>"

    def to_dict(self) -> dict:
        """Returns the dictionary representation of the country"""
        return {
            "name": self.name,
            "code": self.code,
        }

    @staticmethod
    def get_all() -> list["Country"]:
        """Get all countries"""
        return Country.query.all()

    @staticmethod
    def get(code: str) -> "Country | None":
        """Get a country by its code"""
        return Country.query.filter_by(code=code).first()

    @staticmethod
    def create(name: str, code: str) -> "Country":
        """Create a new country"""
        n_country = Country(name=name, code=code)
        db.session.add(n_country)
        db.session.commit()

        return n_country
