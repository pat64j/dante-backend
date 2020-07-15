from .groups import GroupsApi
from .auth import SignupApi
from app import api

api.add_resource(SignupApi, '/signup')
api.add_resource(GroupsApi, '/groups')