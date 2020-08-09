from flask import request, json, jsonify
from core.models.category import Category, CategorySchema
from core.models import PaginationSchema
from core import db
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError, EXCLUDE
from .utils.app_helpers import save_category_picture, allowed_file
from core.exceptions import (NoInputReceivedError,
                             InternalServerError, SchemaValidationError)


class CategoriesApi(Resource):
    @jwt_required
    def get(self):
        categories_schema = CategorySchema(many=True)
        pagination_schema = PaginationSchema()
        page = request.args.get('page',1, type=int)

        try:
            db_categories = Category.query.order_by(Category.updated_at.desc()).paginate(page=page, per_page=5)
            dump_categories = categories_schema.dump(db_categories.items)
            pagination = pagination_schema.dump(db_categories)
            return {"message": "Categories loaded successfully", "data": dump_categories, "pagination": pagination}, 200
        except Exception:
            raise InternalServerError


class CategoryApi(Resource):
    @jwt_required
    def post(self):
        category_schema = CategorySchema(unknown=EXCLUDE)
        json_data = request.form['data']

        if not json_data:
            raise NoInputReceivedError

        try:
            new_category = category_schema.load(json.loads(json_data))
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
            result = category_schema.dump(db_category)
            return {"message": "Category created successfully", "data": result}, 201
        except Exception:
            db.session.rollback()
            raise InternalServerError
