from .index import HomeApi
from .groups import GroupsApi
from .auth import SignupApi, LoginApi, RefreshTokenApi
from core import api

api.add_resource(HomeApi, '/home')
api.add_resource(SignupApi, '/auth/signup')
api.add_resource(LoginApi, '/auth/login')
api.add_resource(RefreshTokenApi, '/auth/refresh-token')
api.add_resource(GroupsApi, '/groups')