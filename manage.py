""" Entry point for the application. """

from flask.cli import FlaskGroup
from src import create_app
from src.data_manager import DataManager

cli = FlaskGroup(create_app=create_app)

def create_data_manager(app):
    return DataManager(app)

@cli.command()
def init_db():
    """ Initialize the database. """
    app = create_app()
    data_manager = create_data_manager(app)
    # Initialize the database schema
    data_manager.db.create_all()

@cli.command()
def save_user(username, email):
    """ Save a user to the database or file. """
    app = create_app()
    data_manager = create_data_manager(app)
    user = User(username=username, email=email)
    data_manager.save_user(user)

if __name__ == "__main__":
    cli()
