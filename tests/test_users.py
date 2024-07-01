import unittest
import json
from src import create_app, db
from src.models.user import User

class TestUserEndpoints(unittest.TestCase):
    
    def setUp(self):
        """Set up Flask test client and initialize database"""
        self.app = create_app('test')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up database after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        """Test creating a new user"""
        data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password'
        }
        response = self.client.post('/users/', json=data)
        self.assertEqual(response.status_code, 201)
        created_user = json.loads(response.data)
        self.assertEqual(created_user['email'], data['email'])
        # Add more assertions as needed

    def test_get_user_by_id(self):
        """Test retrieving a user by ID"""
        # First, create a user to test retrieval
        new_user = User(email='test@example.com', first_name='John', last_name='Doe', password='password')
        with self.app.app_context():
            db.session.add(new_user)
            db.session.commit()
        
        response = self.client.get(f'/users/{new_user.id}')
        self.assertEqual(response.status_code, 200)
        retrieved_user = json.loads(response.data)
        self.assertEqual(retrieved_user['email'], new_user.email)
        # Add more assertions as needed

    def test_update_user(self):
        """Test updating a user"""
        # First, create a user to test update
        new_user = User(email='test@example.com', first_name='John', last_name='Doe', password='password')
        with self.app.app_context():
            db.session.add(new_user)
            db.session.commit()
        
        updated_data = {
            'first_name': 'Jane',
            'last_name': 'Smith'
        }
        response = self.client.put(f'/users/{new_user.id}', json=updated_data)
        self.assertEqual(response.status_code, 200)
        updated_user = json.loads(response.data)
        self.assertEqual(updated_user['first_name'], updated_data['first_name'])
        self.assertEqual(updated_user['last_name'], updated_data['last_name'])
        # Add more assertions as needed

    def test_delete_user(self):
        """Test deleting a user"""
        # First, create a user to test deletion
        new_user = User(email='test@example.com', first_name='John', last_name='Doe', password='password')
        with self.app.app_context():
            db.session.add(new_user)
            db.session.commit()
        
        response = self.client.delete(f'/users/{new_user.id}')
        self.assertEqual(response.status_code, 204)
        # Verify user is deleted
        deleted_user = User.query.get(new_user.id)
        self.assertIsNone(deleted_user)

if __name__ == '__main__':
    unittest.main()
