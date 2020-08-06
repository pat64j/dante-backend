from datetime import datetime
from core import db, ma
from marshmallow import fields


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(50), nullable=False)
    c_descripton = db.Column(db.String(100))
    c_thumbnail = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())




class CategorySchema(ma.Schema):
    class Meta:
        model = 'Category'
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    c_name = fields.String(required=True)
    c_description = fields.String(),
    c_thumbnail = fields.String(),
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
