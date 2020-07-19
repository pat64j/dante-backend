from datetime import datetime
from core import db, ma
from marshmallow import fields



memberships = db.Table('memberships',\
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True)
    )

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(60), nullable=False)
    group_description = db.Column(db.String(200))
    members = db.relationship('User', secondary=memberships, lazy='subquery', backref=db.backref('groups', lazy=True))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=1)
    owner = db.relationship('User')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, group_name, group_description, creator):
        self.group_name = group_name
        self.group_description = group_description
        self.creator = creator


class GroupSchema(ma.Schema):
    class Meta:
        model = 'Group'
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    group_name = fields.String(required=True)
    group_description = fields.String()
    owner = fields.Nested('UserSchema', only=('first_name', 'last_name', 'email', 'confirmed'))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
