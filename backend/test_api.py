"""Test objects used to test the behavior of endpoints in api.py

Classes:
    DrinkTestCase()
"""

import os
import unittest
from src.api import app
from src.database.models import (
    PROJECT_DIR, setup_db
)


class DrinkTestCase(unittest.TestCase):
    """This class represents the test cases for the drink endpoints

    Attributes:
        app: A flask app from the flaskr app
        client: A test client for the flask app to while testing
        db_name: A str representing the name of the test database
        db_path: A str representing the location of the test database
    """

    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.db_name = 'test.db'
        self.db_path = f'sqlite:///{os.path.join(PROJECT_DIR, self.db_name)}'
        setup_db(self.app, self.db_path)

    def tearDown(self):
        """Executed after each test"""

    def test_get_drinks_success(self):
        """Test successful retrieval of drinks"""

        response = self.client().get('/drinks')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('success'), True)
        self.assertTrue(response.json.get('drinks'))


if __name__ == '__main__':
    unittest.main()
