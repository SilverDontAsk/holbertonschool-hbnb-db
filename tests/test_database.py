def test_sqlite_connection(init_database):
    assert init_database.engine.url.drivername == 'sqlite'

def test_postgresql_connection(init_database):
    assert init_database.engine.url.drivername == 'postgresql'

def test_create_user(init_database):
    from src.models import User  # Ensure your User model is imported correctly
    new_user = User(email='test@example.com', first_name='Test', last_name='User')
    init_database.session.add(new_user)
    init_database.session.commit()
    assert new_user.id is not None

def test_read_user(init_database):
    from src.models import User  # Ensure your User model is imported correctly
    user = init_database.session.query(User).filter_by(email='test@example.com').first()
    assert user is not None
    assert user.email == 'test@example.com'

def test_update_user(init_database):
    from src.models import User  # Ensure your User model is imported correctly
    user = init_database.session.query(User).filter_by(email='test@example.com').first()
    user.first_name = 'Updated'
    init_database.session.commit()
    updated_user = init_database.session.query(User).filter_by(email='test@example.com').first()
    assert updated_user.first_name == 'Updated'

def test_delete_user(init_database):
    from src.models import User  # Ensure your User model is imported correctly
    user = init_database.session.query(User).filter_by(email='test@example.com').first()
    init_database.session.delete(user)
    init_database.session.commit()
    deleted_user = init_database.session.query(User).filter_by(email='test@example.com').first()
    assert deleted_user is None
