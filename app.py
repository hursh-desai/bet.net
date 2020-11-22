from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from commands import create_tables
from flask.cli import with_appcontext


app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# app.cli.add_command(create_tables)

from views import *



if __name__ == '__main__':
    app.run()