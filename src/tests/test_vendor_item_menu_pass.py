import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from blueprint_test_case import BaseTestCase
from StringIO import StringIO
import filecmp
import shutil

class FlaskTestCase(BaseTestCase):

    # Ensure login behaves correctly with incorrect credentials
    def test_add_menu_item(self):

        # login first
        response = self.client.post(
            '/login/vendor',
            data=dict(username="testing", password="testing")
        )
        self.assertEqual(response.status_code, 200)


        # add one item
        response = self.client.post(
            '/addMenuItem',
            data=dict(
                itemname="Chickenpopcorn",
                price=99.99,
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"item added successfully to menu", response.data)

        # add one item
        response = self.client.post(
            '/addMenuItem',
            data=dict(
                itemname="Chicken",
                price=9.99,
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"item added successfully to menu", response.data)

        # add one item
        response = self.client.post(
            '/addMenuItem',
            data=dict(
                itemname="Popcorn",
                price=9.99,
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"item added successfully to menu", response.data)

        # add duplicated menu items
        response = self.client.post(
            '/addMenuItem',
            data=dict(
                itemname="Chickenpopcorn",
                price=99.99,
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"item already exist in the menu", response.data)


    # Ensure login behaves correctly with incorrect credentials
    def test_invalid_price_add(self):

        # login first
        response = self.client.post(
            '/login/vendor',
            data=dict(username="testing", password="testing")
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/addMenuItem',
            data=dict(
                itemname="PopcornChicken",
                price=-99.99,
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"invalid form input", response.data)

    def test_delete_items(self):
        # login first
        response = self.client.post(
            '/login/vendor',
            data=dict(username="testing", password="testing")
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/deleteMenuItem',
            data=dict(
                itemname="Chickenpopcorn",
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"item deleted successfully from menu", response.data)

        response = self.client.post(
            '/deleteMenuItem',
            data=dict(
                itemname="Chicken",
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"item deleted successfully from menu", response.data)

        response = self.client.post(
            '/deleteMenuItem',
            data=dict(
                itemname="Popcorn",
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"item deleted successfully from menu", response.data)

        response = self.client.post(
            '/deleteMenuItem',
            data=dict(
                itemname="Popcorn",
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"item doesn't exit in menu", response.data)
