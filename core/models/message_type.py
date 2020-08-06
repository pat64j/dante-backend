from datetime import datetime
from core import db, ma
from marshmallow import fields


class MessageType(db.Model):
    __tablename__ = 'message_types'
    id = db.Column(db.Integer, primary_key=True)
    t_name = db.Column(db.String(50), nullable=False)
    t_description = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class MessageTypeSchema(ma.Schema):
    class Meta:
        model = 'MessageType'
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    t_name = fields.String(required=True)
    t_description = fields.String()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)