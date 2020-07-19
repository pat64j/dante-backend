import click
from flask.cli import with_appcontext

from core import db
from core.models.user import User
from core.models.role import Role
from core.models.group import Group



@click.command(name="create_tables")
@with_appcontext
def create_tables():
    """Create initial db tables."""
    db.create_all()
    print('***** Datebase Tables Created ****')

@click.command(name="drop_tables")
@with_appcontext
def drop_tables():
    """Drop my db tables."""
    db.drop_all()
    print('***** Datebase Tables Dropped ****')