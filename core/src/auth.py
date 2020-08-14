import secrets
import json
from datetime import datetime, date
from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    create_refresh_token,
    jwt_refresh_token_required,
    jwt_required,
    get_raw_jwt
)
from flask_jwt_extended.exceptions import WrongTokenError
from core import db
from flask_restful import Resource
from core.models.user import User, UserSchema, LoginSchema
from core.models.token_blacklist import TokenBlacklistSchema
from marshmallow import ValidationError, EXCLUDE
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from core.exceptions import (TokenNotFound,
                             SchemaValidationError, EmailAlreadyExistsError, FreshTokenRequiredError,
                             InternalServerError, AccountNotFoundError, UpdatingAccountError,
                             NoInputReceivedError
                             )
from .utils.blacklist_helpers import (
    is_token_revoked, add_token_to_database, get_user_tokens,
    revoke_token, unrevoke_token, prune_database
)
from .utils.app_helpers import allowed_file, save_picture


class SignupApi(Resource):
    def post(self):
        user_schema = UserSchema(unknown=EXCLUDE)
        json_data = request.form['data']

        if not json_data:
            return {"error": "No input data provided."}, 400

        try:
            new_user = user_schema.load(json_data)
        except ValidationError as err:
            raise SchemaValidationError

        try:
            db_user = User(**new_user)
            db.session.add(db_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise EmailAlreadyExistsError

        result = user_schema.dump(User.query.get(db_user.id))
        return {"message": "Account created successfully", "data": result}, 201


class LoginApi(Resource):
    def post(self):
        login_schema = LoginSchema(unknown=EXCLUDE)
        user_schema = UserSchema(unknown=EXCLUDE)
        json_data = request.form['data']

        if not json_data:
            return {"error": "Email and password field not provided."}, 400

        try:
            login_user = login_schema.load(json.loads(json_data))
        except ValidationError:
            raise SchemaValidationError

        db_user = User.query.filter_by(
            email=str(login_user.get('email'))).first()

        if db_user is not None:
            authorized = db_user.verify_password(login_user.get('password'))
            if not authorized:
                return {"error": "Email or password invalid", "data": ""}, 401

            access_token = create_access_token(
                identity=db_user.email, fresh=True)
            refresh_token = create_refresh_token(identity=db_user.email)
            export_user = user_schema.dump(db_user)

            # Store the tokens in our store with a status of not currently revoked.
            add_token_to_database(access_token, db_user.email)
            add_token_to_database(refresh_token, db_user.email)

            result = {
                "message": "Login successful",
                "data": {
                    "token": access_token,
                    "refresh_token": refresh_token
                },
                "owner": export_user
            }

            return result, 200
        elif db_user is None:
            return {"error": "There is no account with this email", "data": ""}, 404

        return {"error": "Server error", "data": ""}, 500


class AuthTokenApi(Resource):
    @jwt_refresh_token_required
    def post(self):
        try:
            current_user = get_jwt_identity()

            new_token = create_access_token(identity=current_user, fresh=False)
            add_token_to_database(new_token, current_user)
            return {"message": "Token refreshed successfully", "data": {"access_token": new_token}}, 201
        except WrongTokenError:
            raise FreshTokenRequiredError
        except Exception:
            raise InternalServerError

    @jwt_required
    def get(self):

        token_bl_schema = TokenBlacklistSchema()
        user_identity = get_jwt_identity()
        all_tokens = get_user_tokens(user_identity)
        tokens_dict = [token_bl_schema.dump(token) for token in all_tokens]
        return {"message": "tokens acquired successfully", "data": tokens_dict}, 200

    @jwt_required
    def delete(self):
        token_id = get_raw_jwt()['jti']
        # Revoke the token
        user_identity = get_jwt_identity()
        try:
            revoke_token(token_id, user_identity)
            return {'msg': 'Token revoked'}, 200
        except TokenNotFound:
            raise TokenNotFound


class UserApi(Resource):
    @jwt_required
    def put(self):
        user_schema = UserSchema(unknown=EXCLUDE)
        json_data = request.form['data']
        user_id = get_jwt_identity()

        if not json_data:
            raise NoInputReceivedError

        try:
            validated_user_json = user_schema.load(json.loads(json_data))
        except ValidationError as err:
            raise SchemaValidationError

        if 'file' in request.files:
            file = request.files['file']

            if file and allowed_file(file.filename):
                file_path = save_picture(file)
        db_user = User.query.filter_by(email=user_id).first()
        if db_user is not None:
            db_user.first_name = validated_user_json.get('first_name')
            db_user.last_name = validated_user_json.get('last_name')
            db_user.bday = validated_user_json.get('bday') or date(1988, 10, 30)
            if 'file_path' in locals() and file_path is not None:
                db_user.avatar = file_path
            db.session.commit()
            result = user_schema.dump(db_user)
            return {"message": "Account updated successfully", "data": result}, 200

        # try:
        #     db_user = User.query.filter_by(email=user_id).first()
        #     if db_user is not None:
        #         db_user.first_name = validated_user_json.get('first_name')
        #         db_user.last_name = validated_user_json.get('last_name')
        #         db_user.bday = validated_user_json.get('bday') or date(1988, 10, 30)
        #         if 'file_path' in locals() and file_path is not None:
        #             db_user.avatar = file_path
        #         db.session.commit()
        #         result = user_schema.dump(db_user)
        #         return {"message": "Account updated successfully", "data": result}, 200
        # except NoResultFound:
        #     db.session.rollback()
        #     raise AccountNotFoundError
        # except Exception:
        #     raise UpdatingAccountError
