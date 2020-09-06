from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)