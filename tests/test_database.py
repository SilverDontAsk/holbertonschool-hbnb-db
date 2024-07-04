from src.models.user import User

def test_sqlite_connection(test_app, init_database):
    """Test connection to SQLite database."""
    assert 'sqlite' in test_app.config['SQLALCHEMY_DATABASE_URI']

def test_postgresql_connection(test_app, init_database):
    """Test connection to PostgreSQL database."""
    assert 'postgresql' in test_app.config['SQLALCHEMY_DATABASE_URI']

def test_create_user(test_app, init_database):
    """Test creating a new user."""
    user = User(username='testuser', email='test@example.com')
    db = init_database

    db.session.add(user)
    db.session.commit()

    assert user in db.session

def test_read_user(test_app, init_database):
    """Test reading a user."""
    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.username == 'testuser'

def test_update_user(test_app, init_database):
    """Test updating a user."""
    user = User.query.filter_by(username='testuser').first()
    user.email = 'newemail@example.com'
    db = init_database

    db.session.commit()

    updated_user = User.query.filter_by(username='testuser').first()
    assert updated_user.email == 'newemail@example.com'

def test_delete_user(test_app, init_database):
    """Test deleting a user."""
    user = User.query.filter_by(username='testuser').first()
    db = init_database

    db.session.delete(user)
    db.session.commit()

    deleted_user = User.query.filter_by(username='testuser').first()
    assert deleted_user is None
