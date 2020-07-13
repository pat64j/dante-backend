from datetime import datetime
from app import db


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
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)