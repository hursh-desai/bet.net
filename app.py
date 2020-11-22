from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from commands import create_tables

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from views import *

app.cli.add_command(create_tables)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)