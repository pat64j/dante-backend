from flask_seeder import Seeder, Faker, generator
from core.models.role import Role
from core.models.user import User

class UserSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 2

    def run(self):

        role1 = Role.query.filter_by(name="admin").first()
        admin_user =  User(first_name="Patrick",\
            last_name = "Adonteng", email = "pat64j@gmail.com", password="Password", confirmed=True, role= role1)

        self.db.session.add(admin_user)
        self.db.session.commit()