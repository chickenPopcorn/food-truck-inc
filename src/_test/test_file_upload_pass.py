import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from blueprint_test_case import BaseTestCase
from StringIO import StringIO
import filecmp

class FlaskTestCase(BaseTestCase):

    # Ensure login behaves correctly with incorrect credentials
    def test_file_upload(self):

        # Remove test file first if exist
        try:
            os.remove('uploads/test.jpg')
        except OSError:
            pass

        with open('static/test.jpg') as test:
            imgStringIO = StringIO(test.read())
            response = self.client.post(
                '/upload/',
                data={'file': (imgStringIO, 'test.jpg')}
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(filecmp.cmp('uploads/test.jpg', 'static/test.jpg'), True )