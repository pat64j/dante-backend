import datetime
from flask import request, Response
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    create_refresh_token,
    jwt_refresh_token_required
)
from core import db
from flask_restful import Resource
from core.models.user import User, UserSchema, LoginSchema
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


class LoginApi(Resource):
    def post(self):
        login_schema = LoginSchema()
        json_data = request.get_json()

        if not json_data:
            return {"error": "Email and password field not provided."} , 400

        try:
            login_user = login_schema.load(json_data)
        except ValidationError as err:
            return {"error": "Validation error", "data": err.messages}, 422

        db_user = User.query.filter_by(email=str(json_data.get('email'))).first()

        if db_user is not None:
            authorized = db_user.verify_password(json_data.get('password'))
            if not authorized:
                return {"error":"Email or password invalid", "data": ""}, 401

            expires = datetime.timedelta(minutes=1)
            access_token = create_access_token(identity=db_user.id, expires_delta=expires, fresh=True)
            refresh_token = create_refresh_token(identity=db_user.id)

            return {"message":"Login successful", "data":{"token": access_token, "refresh_token": refresh_token}}, 200
        elif db_user is None:
            return {"error":"There is no account with this email", "data": ""}, 404

        return {"error":"Server error", "data": ""}, 500


class RefreshTokenApi(Resource):
    @jwt_refresh_token_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            expires = datetime.timedelta(minutes=1)
            new_token = create_access_token(identity=current_user, expires_delta=expires, fresh=False)
            return {"message": "Token refreshed successfully", "data":{"access_token": new_token}}
        except:
            return {"error": "An error occurred", "data":""}

