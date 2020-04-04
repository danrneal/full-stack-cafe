"""Test objects used to test the behavior of endpoints in api.py

Classes:
    DrinkTestCase()
"""

import os
import unittest
from src.api import app
from src.database.models import PROJECT_DIR, setup_db, Drink


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
        self.assertIsNone(response.json['drinks'][0]['recipe'][0].get('name'))

    def test_get_drinks_detail_success(self):
        """Test successful retrieval of drinks detail"""

        response = self.client().get('/drinks-detail')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('success'), True)
        self.assertTrue(response.json.get('drinks'))
        self.assertIsNotNone(
            response.json['drinks'][0]['recipe'][0].get('name')
        )

    def test_create_drink_success(self):
        """Test successful creation of drink"""

        new_drink = {
            'title': 'Water',
            'recipe': [{
                'name': 'Water',
                'parts': 1,
                'color': 'blue',
            }]
        }

        response = self.client().post('/drinks', json=new_drink)

        created_drink_id = response.json.get('created_drink_id')
        drink = Drink.query.get(created_drink_id)
        new_drink['id'] = created_drink_id

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('success'), True)
        self.assertEqual(drink.long_format(), new_drink)

    def test_create_drink_no_info_fail(self):
        """Test failed drink creation when info is missing"""

        response = self.client().post('/drinks')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json.get('success'), False)
        self.assertEqual(response.json.get('message'), 'Bad Request')


if __name__ == '__main__':
    unittest.main()
