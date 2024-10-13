import sys
import os

# Add the src folder to the system path so that we can import the src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import your Flask app here
from src import app

class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use an in-memory database
    TESTING = True
    SECRET_KEY = 'test-secret-key'

# Test setup function
def setUpApp():
    app.config.from_object(TestConfig)
    return app