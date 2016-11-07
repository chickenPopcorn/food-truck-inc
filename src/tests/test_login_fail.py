import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from blueprint_test_case import BaseTestCase

class FlaskTestCase(BaseTestCase):

    # Ensure login behaves correctly with incorrect credentials
    def test_incorrect_customer_login(self):
        response = self.client.post(
            '/login/customer',
            data=dict(username="wrong!", password="wrong!"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'The username and password does not match!', response.data)

    # Ensure login behaves correctly with incorrect credentials
    def test_incorrect_vendor_login(self):
        response = self.client.post(
            '/login/vendor',
            data=dict(username="wrong!", password="wrong!"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'The username and password does not match!', response.data)
