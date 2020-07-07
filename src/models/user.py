from src import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    avatar = db.Column(db.String(20), default='default_avatar.jpg', nullable=False)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.avatar}')"


