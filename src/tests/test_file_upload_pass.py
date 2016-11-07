import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from blueprint_test_case import BaseTestCase
from StringIO import StringIO
import filecmp
import shutil

class FlaskTestCase(BaseTestCase):

    # Ensure login behaves correctly with incorrect credentials
    def test_file_upload(self):

        # login first
        response = self.client.post(
            '/login/vendor',
            data=dict(username="testing", password="testing")
        )
        self.assertEqual(response.status_code, 200)

        # Remove test file first if exist
        try:
            os.remove('uploads/testing/test.jpg')
        except OSError:
            pass

        with open('static/test.jpg', "rb") as test:
            response = self.client.post(
                '/upload/',
                data={'file': (StringIO(test.read()), 'test.jpg')}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(filecmp.cmp('uploads/testing/test.jpg', 'static/test.jpg'), True )

        # Clean up
        try:
            shutil.rmtree('uploads/testing')
        except OSError:
            pass