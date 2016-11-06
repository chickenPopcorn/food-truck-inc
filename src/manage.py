import unittest
import os
import coverage
from flask_script import Manager
from app import app
import shutil

manager = Manager(app)

@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=5).run(tests)

@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(branch=True,
                            include='*', omit=[
                                            '*/site-packages/*',
                                            '*test*.py',
                                            '*/python2.7/*'
                                            ])
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=5).run(tests)
    cov.stop()
    cov.save()
    print 'Coverage Summary:'

    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))

    covdir = os.path.join(basedir, 'coverage')
    try:
        shutil.rmtree(covdir)
    except OSError:
        pass

    cov.html_report(directory=covdir)
    cov.erase()


if __name__ == '__main__':
    manager.run()
