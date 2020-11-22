import click
from flask.cli import with_appcontext
from app import db
from models import Bet, Event, Agreement, User

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()