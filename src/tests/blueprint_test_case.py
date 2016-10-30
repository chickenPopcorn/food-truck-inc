from flask_testing import TestCase
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('server.config.TestConfig')
        return app
