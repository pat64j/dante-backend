from flask import request
from core.models.category import Category, CategorySchema
from core import db
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from core.exceptions import (NoInputReceivedError,
                             InternalServerError, SchemaValidationError)


class CategoriesApi(Resource):
    @jwt_required
    def get(self):
        categories_schema = CategorySchema(many=True)
        try:
            db_categories = Category.query.all()
            dump_categories = categories_schema.dumps(db_categories)
            return {"message": "Categories loaded successfully", "data": dump_categories}, 200
        except Exception:
            raise InternalServerError


class CategoryApi(Resource):
    @jwt_required
    def post(self):
        category_schema = CategorySchema()
        json_data = request.form['data']

        if not json_data:
            raise NoInputReceivedError

        try:
            new_category = category_schema.load(json_data)
        except ValidationError:
            raise SchemaValidationError

        if 'file' in request.files:
            file = request.files['file']

            if file and allowed_file(file.filename):
                file_path = save_category_picture(file)
        try:
            db_category = Category(**new_category)
            if 'file_path' in locals() and file_path is not None:
                db_category.c_thumbnail = file_path
            db.session.add(db_category)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise InternalServerError
