from app import app
from flask_testing import TestCase
import unittest
import json

class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('server.config.TestConfig')
        return app
    '''
    def setUp(self):
        db.create_all()
        # db.session.add(User("admin", "ad@min.com", "admin"))
        # db.session.add(
        #    BlogPost("Test post", "This is a test. Only a test.", "admin"))
        # db.session.commit()

    def tearDown(self):
        # db.session.remove()
        db.drop_all()
    '''

class FlaskTestCase(BaseTestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        response = self.client.get('/', content_type='text/plain')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "Hello, World!")

    '''
    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        response = tester.get('/login')
        self.assertIn(b'Please login', response.data)
    '''

    def test_register_login_delete_change_password(self):
        response = self.client.post(
            '/register',
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
        self.assertIn(b'The registration is successful!', json.loads(response.data)["message"])


        response = self.client.post(
            '/login',
            data = dict(username="rxie25", password="zhedouxing")
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful!', json.loads(response.data)["message"])

        response = self.client.post(
            '/changePassword',
            data=dict(
                oldpassword="zhedouxing",
                newpassword="zheyexing?",
                confirm="zheyexing?"
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'Your password has been changed!', json.loads(response.data)["message"])

        response = self.client.post(
            '/delete',
            data=dict(
                username="rxie25",
                password="zheyexing?"
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'Your account has been deleted!', json.loads(response.data)["message"])

    # Ensure login behaves correctly with incorrect credentials
    def test_incorrect_login(self):
        response = self.client.post(
            '/login',
            data=dict(username="wrong!", password="wrong!"),
        )
        self.assertIn(u'The username and password does not match!', json.loads(response.data)["message"])
        self.assertEqual(response.status_code, 200)



    '''
    def test_delete(self):



    # Ensure logout behaves correctly
    def test_logout(self):
        tester = app.test_client()
        tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You were logged out', response.data)

    # Ensure that main page requires user login
    def test_main_route_requires_login(self):
        tester = app.test_client()
        response = tester.get('/', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)

    # Ensure that logout page requires user login
    def test_logout_route_requires_login(self):
        tester = app.test_client()
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)

    # Ensure that posts show up on the main page
    def test_posts_show_up_on_main_page(self):
        tester = app.test_client()
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Hello from the shell', response.data)
    '''

if __name__ == '__main__':
    unittest.main()
