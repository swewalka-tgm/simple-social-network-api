import unittest
from flask_bcrypt import Bcrypt
from flask_login import login_user
import sys
import os

# Add the src folder to the system path so that we can import the src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import your Flask app here
from testing import setUpApp
from src import app
from model import db
from model.usermodel import User

class UserFollowTests(unittest.TestCase):

    def setUp(self):
        # Set up test app
        self.app = setUpApp()
        self.client = self.app.test_client()  # Create a test client
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Initialize the database 
        with self.app_context:
            db.create_all()
            
        # Create some test users
        for i in range(2):
            existing_user = User.query.filter_by(email=f'user{i}@example.com').first()
            if not existing_user:
                db.session.add(User(username=f'user{i}', email=f'user{i}@example.com', password='hashed_password'))

        db.session.commit()


        self.user1 = User.query.filter_by(email='user1@example.com').first()
        self.user2 = User.query.filter_by(email='user2@example.com').first()

        # Log in user1 for the tests
        #with self.client.session_transaction() as sess:
        #    sess['_user_id'] = str(self.user1.id)
            
        login_user(self.user1)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_follow_user_success(self):
        # Test following a valid user
        response = self.client.post('/follow', json={
            'user_followed': self.user2.id
        })

        # Ensure the follow was successful
        self.assertEqual(response.status_code, 200)

        # Check that user1 is following user2
        with self.app_context:
            self.assertTrue(self.user1.is_following(self.user2))

    def test_follow_non_existent_user(self):
        # Test following a user that doesn't exist
        response = self.client.post('/follow', json={
            'user_followed': 999  # Non-existent user ID
        })

        # Ensure a 400 error is returned
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'User does not exist!', response.data)

    def test_unfollow_user_success(self):
        # First, have user1 follow user2
        self.user1.follow(self.user2)
        db.session.commit()

        # Test unfollowing user2
        response = self.client.post('/unfollow', json={
            'user_followed': self.user2.id
        })

        # Ensure the unfollow was successful
        self.assertEqual(response.status_code, 200)

        # Check that user1 is no longer following user2
        with self.app_context:
            self.assertFalse(self.user1.is_following(self.user2))

    def test_unfollow_non_existent_user(self):
        # Test unfollowing a user that doesn't exist
        response = self.client.post('/unfollow', json={
            'user_followed': 999  # Non-existent user ID
        })

        # Ensure a 400 error is returned
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'User does not exist!', response.data)

if __name__ == '__main__':
    unittest.main() 