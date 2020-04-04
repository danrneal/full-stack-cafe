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

    def test_patch_drink_success(self):
        """Test successful changing of a drink"""

        old_drink = Drink.query.order_by(Drink.id.desc()).first().long_format()
        drink_id = old_drink['id']

        new_drink = {
            'title': 'Whiskey',
            'recipe': [{
                'name': 'Whisky',
                'parts': 1,
                'color': 'brown',
            }]
        }

        response = self.client().patch(
            f'/drinks/{drink_id}',
            json=new_drink
        )

        new_drink['id'] = drink_id
        drink = Drink.query.get(drink_id).long_format()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('success'), True)
        self.assertEqual(response.json.get('updated_drink_id'), drink_id)
        self.assertEqual(response.json.get('old_drink'), old_drink)
        self.assertEqual(response.json.get('new_drink'), new_drink)
        self.assertEqual(drink, new_drink)

    def test_patch_drink_out_of_range_fail(self):
        """Test failed drink change when drink does not exist"""

        drink_id = Drink.query.order_by(Drink.id.desc()).first().id

        new_drink = {
            'title': 'Whiskey',
            'recipe': [{
                'name': 'Whisky',
                'parts': 1,
                'color': 'brown',
            }]
        }

        response = self.client().patch(
            f'/drinks/{drink_id+1}',
            json=new_drink
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json.get('success'), False)
        self.assertEqual(response.json.get('message'), 'Unprocessable Entity')

    def test_patch_drink_no_info_fail(self):
        """Test failed drink change when no info is given"""

        drink_id = Drink.query.order_by(Drink.id.desc()).first().id

        response = self.client().patch(f'/drinks/{drink_id}')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json.get('success'), False)
        self.assertEqual(response.json.get('message'), 'Bad Request')

    def test_delete_drink_success(self):
        """Test successful deletion of drink"""

        drink_id = Drink.query.order_by(Drink.id.desc()).first().id

        response = self.client().delete(f'/drinks/{drink_id}')

        drink = Drink.query.get(drink_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('success'), True)
        self.assertEqual(response.json.get('deleted_drink_id'), drink_id)
        self.assertIsNone(drink)

    def test_delete_drink_out_of_range_fail(self):
        """Test failed drink deletion when drink does not exist"""

        drink_id = Drink.query.order_by(Drink.id.desc()).first().id

        response = self.client().delete(f'/drinks/{drink_id+1}')

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json.get('success'), False)
        self.assertEqual(response.json.get('message'), 'Unprocessable Entity')


if __name__ == '__main__':
    unittest.main()
