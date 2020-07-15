from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from app.config import Config
from flask_seeder import FlaskSeeder
from flask_login import LoginManager


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
seeder = FlaskSeeder()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.models.user import User
    from app.models.role import Role
    from app.models.group import Group

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app,db)
    seeder.init_app(app,db)
    login_manager.init_app(app)

    from app.src import api
    api.init_app(app)


    # from app.recipes.index import index as main_blueprint
    # app.register_blueprint(main_blueprint)

    return app