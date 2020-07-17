import os
from core import db, create_app
from core.config import TestingConfig
from sqlalchemy.orm.session import close_all_sessions
import unittest
import tempfile


class BaseTestCase(unittest.TestCase):
    """ A base test case """
    def setUp(self):
        app = create_app(TestingConfig)
        self.test_db_file = tempfile.mkstemp()[1]
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.test_db_file
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        with app.app_context():
            db.create_all()

        app.app_context().push()
        self.app = app.test_client()

    def tearDown(self):
        close_all_sessions()
        db.drop_all()
        self.app_context().pop()


