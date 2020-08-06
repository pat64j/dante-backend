import click
from flask.cli import with_appcontext

from core import db
from core.models.user import User
from core.models.role import Role
from core.models.group import Group
from core.src.utils.blacklist_helpers import prune_database



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

@click.command(name="prune_tokens")
@with_appcontext
def prune_tokens():
    """Prune token tables."""
    print('Pruning tokens table...')
    prune_database()
    print('***** Token Table Pruned ****')