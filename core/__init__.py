from flask import Flask, Blueprint
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from core.config import Config
from flask_seeder import FlaskSeeder


db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
migrate = Migrate()
jwt = JWTManager()
seeder = FlaskSeeder()
api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix='/api/v1')



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from core.models.user import User
    from core.models.role import Role
    from core.models.group import Group

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app,db)
    seeder.init_app(app,db)


    from core.src import dante_api
    app.register_blueprint(dante_api)
    app.register_blueprint(api_bp)

    return app