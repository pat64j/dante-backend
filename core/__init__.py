from flask import Flask, Blueprint
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from core.config import Config
from flask_seeder import FlaskSeeder
from flask_cors import CORS
from core.exceptions import errors


db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
seeder = FlaskSeeder()
api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix='/api/v1', errors=errors)



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/v1/*": {"origins": "*"}})
    migrate.init_app(app,db)
    seeder.init_app(app,db)


    from core.src import dante_api
    app.register_blueprint(dante_api)
    app.register_blueprint(api_bp)



    return app