from flask import Blueprint, jsonify
from core.src.utils.blacklist_helpers import is_token_revoked
from core import jwt
from core.models.user import User

@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)


@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401


@jwt.invalid_token_loader
def my_invalid_token_callback(expired_token):
    return jsonify({
        'status': 422,
        'sub_status': 42,
        'msg': expired_token
    }), 422

dante_api = Blueprint('dante_api', __name__)

from . import routes