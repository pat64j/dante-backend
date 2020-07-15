from flask import request, jsonify
from app import db
from flask_restful import Resource
from app.models.user import User, UserSchema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError


class SignupApi(Resource):
    def post(self):
        user_schema = UserSchema()
        json_data = request.get_json()

        if not json_data:
            return {"error": "No input data provided."}, 400

        try:
            new_user = user_schema.load(json_data)
        except ValidationError as err:
            return {"error": "Validation error", "data": err.messages}, 422

        try:
            db_user = User(**new_user)
            db.session.add(db_user)
            db.session.commit()
        except IntegrityError as err:
            db.session.rollback()
            return {"error": "This email address has been taken"}, 502

        result = user_schema.dump(User.query.get(db_user.id))
        return {"message": "Account created successfully", "data": result}, 201

