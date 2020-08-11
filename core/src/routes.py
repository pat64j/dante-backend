from .index import HomeApi
from .groups import GroupsApi
from .auth import SignupApi, LoginApi, AuthTokenApi, UserApi
from .categories import CategoryApi, CategoriesApi
from .messages import MessageTypesApi, MessageCategoriesApi, MessageApi, MessagesApi
from core import api

api.add_resource(HomeApi, '/')
api.add_resource(SignupApi, '/auth/signup')
api.add_resource(LoginApi, '/auth/login')
api.add_resource(AuthTokenApi, '/auth/token-api')
api.add_resource(UserApi, '/user')
api.add_resource(CategoryApi, '/category/<int:category_id>')
api.add_resource(CategoriesApi, '/categories')
api.add_resource(MessageTypesApi, '/message_types')
api.add_resource(MessageCategoriesApi, '/message_categories')
api.add_resource(MessageApi, '/message')
api.add_resource(MessagesApi, '/messages')
api.add_resource(GroupsApi, '/groups')