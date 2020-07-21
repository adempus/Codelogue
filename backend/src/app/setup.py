"""
 code for setting up the app with a database, route blueprints, and other configurations.
"""
import os
from flask import Flask
from pendulum import duration
from dotenv import load_dotenv
from flask_cors import CORS
from flask_migrate import Migrate
from .models import db
from ..routes import *


load_dotenv(verbose=True)


def createApp():
    """ :return a Flask app instance. """
    app = Flask(__name__)
    applyConfigs(app)
    registerBlueprints(app)
    app.app_context().push()
    db.init_app(app)
    Migrate(app, db)
    return app


def registerBlueprints(app):
    app.register_blueprint(index, url_prefix='/')
    app.register_blueprint(user, url_prefix='/user')


def applyConfigs(app):
    app.config.from_object(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = getDatabaseURI()
    app.config['SECRET_KEY'] = os.getenv('APP_KEY')
    setupJWT(app)


def setupJWT(app):
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = duration(minutes=35)
    app.config['JWT_ERROR_MESSAGE_KEY'] = 'error'


def getDatabaseURI():
    """ :return str database URI from parsed .env variables """
    db_driver = os.getenv('DB_DRIVER')
    db_user = os.getenv('DB_USER')
    db_passwd = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    return f"{db_driver}://{db_user}:{db_passwd}@{db_host}:{db_port}/{db_name}"

