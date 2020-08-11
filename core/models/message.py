from datetime import datetime
from core import db, ma
from marshmallow import fields

messages_categories = db.Table('messages_categories',\
    db.Column('message_id', db.Integer, db.ForeignKey('messages.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
    )


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    m_title = db.Column(db.String(100), nullable=True)
    m_description = db.Column(db.String(200))
    type_id = db.Column(db.Integer, db.ForeignKey('message_types.id'), nullable=False)
    m_type = db.relationship('MessageType')
    m_categories = db.relationship('Category', secondary=messages_categories, lazy='joined', backref=db.backref('messages', lazy=True))
    is_video = db.Column(db.Boolean, default=True, nullable=False)

    m_thumbnail = db.Column(db.String(100))
    m_link = db.Column(db.String(200))
    m_duration = db.Column(db.String(50))
    m_broadcast = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class MessageSchema(ma.Schema):
    class Meta:
        model = 'Message'
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    m_title = fields.String(required=True)
    m_description = fields.String()
    m_type = fields.Nested('MessageTypeSchema', only=('id','t_name', 't_description',))
    m_categories = fields.Nested('CategorySchema', many=True, only=('id', 'c_name','c_description','c_thumbnail'))
    is_video = fields.Boolean(required=True)
    m_thumbnail = fields.String(allow_none=True)
    m_link = fields.String(required=True)
    m_duration = fields.String(required=True)
    m_broadcast = fields.Boolean(default=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)