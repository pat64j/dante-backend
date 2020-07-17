from core import db, ma
from datetime import datetime
from marshmallow import fields

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

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    users = fields.List(fields.Nested('User', only=('first_name','last_name','email','confirmed')), dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)