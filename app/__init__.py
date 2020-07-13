from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from flask_seeder import FlaskSeeder
from flask_login import LoginManager


db = SQLAlchemy()
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
    migrate.init_app(app,db)
    seeder.init_app(app,db)
    login_manager.init_app(app)


    from app.recipes.index import index as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.recipes.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app