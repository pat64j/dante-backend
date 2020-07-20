from flask import Blueprint
from core.src.utils.blacklist_helpers import is_token_revoked
from core import jwt, db
from core.models.user import User

@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)


dante_api = Blueprint('dante_api', __name__)

from . import routes