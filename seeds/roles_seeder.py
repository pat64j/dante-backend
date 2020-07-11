from flask_seeder import Seeder, Faker, generator
from app.models.role import Role

class RoleSeeder(Seeder):

    def run(self):

        role1 = Role(name="admin")
        role2 =  Role(name="user")

        self.db.session.add_all([role1, role2])
        self.db.session.commit()
