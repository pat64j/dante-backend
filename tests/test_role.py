import core
from .test_base import BaseTestCase
from core import db
from core.models.role import Role
import unittest


def create_role():
    role1 = Role(name="admin")
    db.session.add(role1)
    db.session.commit()

class TestRole(BaseTestCase):
    # def setUp(self):
    #     super(TestRole, self).setUp()
    #     create_role()

    def test_home_endpoint(self):
        rv = self.app.get('/api/v1/')
        self.assertEqual(rv.status_code, 200)


if __name__ == "__main__":
    unittest.main()