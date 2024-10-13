import unittest
from flask_bcrypt import Bcrypt
import sys
import os

# Add the src folder to the system path so that we can import the src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import your Flask app here
from testing import setUpApp
from src import app
from model import db
from model.usermodel import User


class UserAuthTests(unittest.TestCase):

    def setUp(self):
        # Set up test app
        self.app = setUpApp()
        self.client = self.app.test_client()  # Create a test client
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Initialize the database and bcrypt
        with self.app_context:
            db.create_all()
            
        self.bcrypt = Bcrypt(self.app)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_registration(self):
        # Simulate a POST request to register a new user
        response = self.client.post('/register', json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        })

        # Check if the response status code is 201 (Created)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'user created!', response.data)

        # Verify that the user was added to the database
        user = User.query.filter_by(email='testuser@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')

    def test_duplicate_registration(self):
        # First, register a user
        self.client.post('/register', json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        })

        # Try registering the same user again
        response = self.client.post('/register', json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        })

        # Check if the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

    def test_registration_invalid_email(self):
        # Simulate a POST request with an invalid email
        response = self.client.post('/register', json={
            'username': 'testuser',
            'email': 'invalid-email',
            'password': 'password123'
        })

        # Check for proper validation and response code
        self.assertEqual(response.status_code, 400)

    def test_login_and_access_protected_route(self):
    # Register the user first
        self.client.post('/register', json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        })

        # Simulate logging in
        response = self.client.post('/login', json={
            'email': 'testuser@example.com',
            'password': 'password123'
        })

        # Check if login was successful
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'user logged in successfully!', response.data)

        # Access a protected route
        with self.client:
            response = self.client.get('/protected')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'This is a protected route', response.data)
    

    def test_login_invalid_email(self):
        # Simulate a POST request to log in with an invalid email
        response = self.client.post('/login', json={
            'email': 'invaliduser@example.com',
            'password': 'password123'
        })

        # Check for the proper error response
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No account associated with this email address!', response.data)

    def test_login_wrong_password(self):
        # First, register a user
        self.client.post('/register', json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        })

        # Try logging in with the wrong password
        response = self.client.post('/login', json={
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        })

        # Check for the proper error response
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'password is wrong!', response.data)

    def test_protected_logout(self):
        # Register and log in the user
        self.client.post('/register', json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        })
        self.client.post('/login', json={
            'email': 'testuser@example.com',
            'password': 'password123'
        })

        # Access the logout endpoint
        response = self.client.get('/logout')

        # Check if the logout was successful
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged out successfully', response.data)
       
        response = self.client.get('/protected') 
  
        self.assertEqual(response.status_code, 401)
    
if __name__ == '__main__':
    unittest.main()
