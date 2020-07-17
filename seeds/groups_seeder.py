from flask_seeder import Seeder
from core.models.user import User
from core.models.group import Group

class GroupSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 3

    def run(self):

        user1 = User.query.filter_by(email="pat64j@gmail.com").first()
        youth_group = Group(group_name="Youth Felowship", group_description="members of ages ranging from 13 to 35", creator=user1)
        women_group = Group(group_name="Women Felowship", group_description="females with children or 20 years and above", creator=user1)

        self.db.session.add_all([youth_group,women_group])
        self.db.session.commit()