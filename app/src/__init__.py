from .groups import GroupsApi
from flask_restful import Api


api = Api(prefix='/api/v1')
api.add_resource(GroupsApi, '/groups')