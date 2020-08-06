from core import db, ma
from marshmallow import fields, EXCLUDE
from datetime import datetime, date
from flask import current_app
from flask_bcrypt import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from .group import memberships


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    avatar = db.Column(db.String(50))
    bday = db.Column(db.Date, default=date(1988,10,30))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=2)
    my_role = db.relationship('Role')
    created_groups = db.relationship('Group', backref='creator')
    # memberships = db.relationship('Group', secondary=memberships, lazy='subquery', backref=db.backref('users', lazy=True))
    confirmed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')


    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf8')


    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def generate_auth_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')


    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except:
            return None

        return User.query.get(data['id'])


    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        self.confirmed = True
        db.session.add(self)
        return True



    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}','{self.email}', '{self.bday}', '{self.avatar}')"


class UserSchema(ma.Schema):
    class Meta:
        model = 'User'
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(load_only=True)
    bday = fields.Date()
    avatar = fields.String(dump_only=True)
    role = fields.Nested('RoleSchema', only=('name',), dump_only=True)
    confirmed = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class LoginSchema(ma.Schema):

    class Meta:
        model = 'User'

    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)