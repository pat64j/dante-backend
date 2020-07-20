import os
import datetime
from flask import request, Response, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    create_refresh_token,
    jwt_refresh_token_required,
    jwt_required,
    get_raw_jwt
)
from core import db
from flask_restful import Resource
from core.models.user import User, UserSchema, LoginSchema
from core.models.token_blacklist import TokenBlacklistSchema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from .exceptions import TokenNotFound

from .utils.blacklist_helpers import (
    is_token_revoked, add_token_to_database, get_user_tokens,
    revoke_token, unrevoke_token, prune_database
)



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

            access_token = create_access_token(identity=db_user.email, fresh=True)
            refresh_token = create_refresh_token(identity=db_user.email)

            # Store the tokens in our store with a status of not currently revoked.
            add_token_to_database(access_token, db_user.email)
            add_token_to_database(refresh_token, db_user.email)

            return {"message":"Login successful", "data":{"token": access_token, "refresh_token": refresh_token}}, 200
        elif db_user is None:
            return {"error":"There is no account with this email", "data": ""}, 404

        return {"error":"Server error", "data": ""}, 500


class AuthTokenApi(Resource):
    @jwt_refresh_token_required
    def post(self):
        try:
            current_user = get_jwt_identity()

            new_token = create_access_token(identity=current_user, fresh=False)
            add_token_to_database(new_token, current_user)
            return {"message": "Token refreshed successfully", "data":{"access_token": new_token}}, 200
        except Exception:
            return {"error": "An error occurred", "data":""} , 500


    @jwt_required
    def get(self):

        token_bl_schema = TokenBlacklistSchema()
        user_identity = get_jwt_identity()
        all_tokens = get_user_tokens(user_identity)
        tokens_dict = [token_bl_schema.dump(token) for token in all_tokens]
        return {"message": "tokens acquired successfully", "data":tokens_dict}, 200


    @jwt_required
    def delete(self):
        token_id = get_raw_jwt()['jti']
        # Revoke the token
        user_identity = get_jwt_identity()
        try:
            revoke_token(token_id, user_identity)
            return {'msg': 'Token revoked'}, 200
        except TokenNotFound:
            return {'msg': 'The specified token was not found'}, 404


