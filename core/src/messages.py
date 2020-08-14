from datetime import datetime
from flask import request, json
from flask_restful import Resource
from core import db
from flask_jwt_extended import jwt_required
from core.models.message_type import MessageType, MessageTypeSchema
from core.models.category import Category, CategorySchema
from core.models.message import Message, MessageSchema
from core.exceptions import (InternalServerError, NoInputReceivedError,
SchemaValidationError)
from marshmallow import ValidationError
from .utils.app_helpers import save_video_picture, save_audio_picture, allowed_file



class MessageCategoriesApi(Resource):
    @jwt_required
    def get(self):
        categories_schema = CategorySchema(many=True)

        try:
            db_categories = Category.query.all()
            dump_categories = categories_schema.dump(db_categories)
            return {"message": "Categories loaded successfully", "data": dump_categories}, 200
        except Exception:
            raise InternalServerError



class MessageTypesApi(Resource):
    @jwt_required
    def get(self):
        ms_type_schema = MessageTypeSchema(many=True)
        try:
            type_list = MessageType.query.all()
            dump_types = ms_type_schema.dump(type_list)
            return {"message": "Types loaded successfully", "data": dump_types}, 200
        except Exception:
            raise InternalServerError


class MessagesApi(Resource):
    @jwt_required
    def post(self):
        message_schema = MessageSchema()
        ms_type_schema = MessageTypeSchema()
        ms_category_schema = CategorySchema()

        json_data = json.loads(request.form['data'])

        if not json_data:
            raise NoInputReceivedError

        try:
            val_message = message_schema.load(json_data)
        except ValidationError:
            raise SchemaValidationError

        if 'file' in request.files:
            file = request.files['file']

            if file and allowed_file(file.filename):
                file_path = save_video_picture(file)

        try:
            media_type_id = int(json_data.get('m_type')['id'])
            category_ids = [int(val['id']) for val in json_data.get('m_categories')]

            media_type_obj = MessageType.query.get(media_type_id)
            category_objs = db.session.query(Category).filter(Category.id.in_(category_ids)).all()

            message_obj = Message(
                m_title=json_data.get('m_title'),
                m_description=json_data.get('m_description'),
                m_link=json_data.get('m_link'),
                is_video=json_data.get('is_video'),
                m_duration=json_data.get('m_duration'),
                m_broadcast=json_data.get('m_broadcast'),
                created_at= datetime.now(),
            )

            if 'file_path' in locals() and file_path is not None:
                message_obj.m_thumbnail = file_path

            message_obj.m_type = media_type_obj
            message_obj.m_categories = [category for category in category_objs]

            db.session.add(message_obj)
            db.session.commit()
            result = message_schema.dump(message_obj)

            return {"message": "Message created successfully", "data": result}, 201
        except Exception:
            db.session.rollback()
            dir(Exception)
            return {"data":"ERROR ERROR ERROR ERROR"}, 500


    @jwt_required
    def get(self):
        message_schema = MessageSchema(many=True)
        message_type = request.args.get('is_video')
        all_messages = Message.query.filter_by(is_video=message_type).all()

        result = message_schema.dump(all_messages)
        return {"message": "Messages loaded successfully", "data": result}, 200



class MessageApi(Resource):
    pass

