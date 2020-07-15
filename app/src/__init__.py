from flask import Blueprint


dante_api = Blueprint('dante_api', __name__)

from . import routes