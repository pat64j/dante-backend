from datetime import datetime
from core import db, ma
from marshmallow import fields

class TokenBlacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'token_id': self.id,
            'jti': self.jti,
            'token_type': self.token_type,
            'user_identity': self.user_identity,
            'revoked': self.revoked,
            'expires': self.expires
        }

    def __repr__(self):
        return f"TokenBlacklist('jti : {self.jti}', 'token_type: {self.token_type}','user_identity: {self.user_identity}', 'revoked: {self.revoked}', 'expires: {self.expires}', 'created_at: {self.created_at}')"



class TokenBlacklistSchema(ma.Schema):
    class Mata:
        model = 'TokenBlacklist'
        load_instance = True


    id = fields.Integer(dump_only=True)
    jti = fields.String()
    token_type = fields.String()
    user_identity = fields.String()
    revoked = fields.Boolean()
    expires = fields.DateTime()
    created_at = fields.DateTime(dump_only=True)

