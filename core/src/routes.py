from .index import HomeApi
from .groups import GroupsApi
from .auth import SignupApi, LoginApi, AuthTokenApi, UserApi
from .categories import CategoryApi, CategoriesApi
from core import api

api.add_resource(HomeApi, '/')
api.add_resource(SignupApi, '/auth/signup')
api.add_resource(LoginApi, '/auth/login')
api.add_resource(AuthTokenApi, '/auth/token-api')
api.add_resource(UserApi, '/user')
api.add_resource(CategoryApi, '/category')
api.add_resource(CategoriesApi, '/categories')
api.add_resource(GroupsApi, '/groups')