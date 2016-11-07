import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from blueprint_test_case import BaseTestCase

class FlaskTestCase(BaseTestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        response = self.client.get('/', content_type='text/plain')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "Hello, World!")

    def test_customer_register_login_delete_update(self):
        # register a new user
        response = self.client.post(
            '/register/customer',
            data=dict(
                username="rxie25",
                password="zhedouxing",
                confirm ="zhedouxing",
                firstname="ruicong",
                lastname="xie",
                email="rxie25@gmail.com"
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The registration is successful!', response.data)

        # login as that user
        response = self.client.post(
            '/login/customer',
            data = dict(username="rxie25", password="zhedouxing")
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful!', response.data)

        # change user's password
        response = self.client.post(
            '/changePassword',
            data=dict(
                oldpassword="zhedouxing",
                newpassword="zheyexing?",
                confirm="zheyexing?"
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'Your password has been changed!', response.data)

        # delete that user
        response = self.client.post(
            '/delete',
            data=dict(
                username="rxie25",
                password="zheyexing?"
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'Your account has been deleted!', response.data)


if __name__ == '__main__':
    unittest.main()
