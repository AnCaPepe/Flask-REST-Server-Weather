# Set the path
import sys, pathlib
sys.path.append( str(pathlib.Path(__file__).parents[1]) )

import pytest
from app import create_app, db

@pytest.fixture
def get_client():
    test_app = create_app()

    # Create a test client using the Flask application configured for testing
    with test_app.test_client() as testing_client:
        # Establish an application context
        with test_app.app_context():
            yield testing_client  # this is where the testing happens!

@pytest.fixture
def get_db( get_client ):
    # Create the database and the database table
    db.drop_all()
    db.create_all()

    return db # this is where the testing happens!