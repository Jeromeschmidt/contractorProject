# First we need to import our app.
# This test file should be in the same folder as your app.py file
from app import app
import unittest

class AppTests(unittest.TestCase):

    # This runs implicitly before any tests are run
    # We use this to set up our app before we test on it
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_store_index(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_checkout(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/shopping_cart/checkout')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_edit_item(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/owner/5d9d49513f18efe4541627c1/edit')

        # assert the status code of the response
        # 405 since user hasnt selected owner yet
        self.assertEqual(result.status_code, 405)

    def test_error(self):
        pass

    def test_item_new(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/owner/add_item')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


    def test_owner_item_show(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/owner/5d9d49513f18efe4541627c1')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_item_show(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/5d9d49513f18efe4541627c1')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_owner(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/owner')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_shopping_cart(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/shopping_cart')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_thanks(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/shopping_cart/checkout/thanks')

        # assert the status code of the response
        #405 because card payment was not entered
        self.assertEqual(result.status_code, 405)
