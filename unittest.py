# test_models.py
import unittest
from src import create_app, db
from src.models import User

class TestCRUDOperations(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        user = User(username='john', email='john@example.com')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(User.query.count(), 1)

    def test_read_user(self):
        user = User(username='jane', email='jane@example.com')
        db.session.add(user)
        db.session.commit()
        retrieved_user = User.query.filter_by(username='jane').first()
        self.assertEqual(retrieved_user.email, 'jane@example.com')

    def test_update_user(self):
        user = User(username='bob', email='bob@example.com')
        db.session.add(user)
        db.session.commit()
        user.email = 'bob2@example.com'
        db.session.commit()
        retrieved_user = User.query.filter_by(username='bob').first()
        self.assertEqual(retrieved_user.email, 'bob2@example.com')

    def test_delete_user(self):
        user = User(username='alice', email='alice@example.com')
        db.session.add(user)
        db.session.commit()
        db.session.delete(user)
        db.session.commit()
        self.assertEqual(User.query.count(), 0)

if __name__ == '__main__':
    unittest.main()
