import os

SERVER_NAME = os.getenv('SERVER_NAME')
FLASK_ENV = os.getenv('FLASK_ENV')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False # silence the deprecation warning



