from app import db, ma
from datetime import datetime

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User', backref='role')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f"Role('{self.name}', '{self.created_at}')"


class RoleSchema(ma.Schema):
    class Meta:
        model = 'Role'
        include_relationships = True
        load_instance = True