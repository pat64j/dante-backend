from flask_seeder import Seeder
from core.models.role import Role

class RoleSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):

        role1 = Role(name="admin")
        role2 =  Role(name="user")

        self.db.session.add_all([role1, role2])
        self.db.session.commit()
