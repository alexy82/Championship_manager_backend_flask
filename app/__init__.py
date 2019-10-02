"""
Server start up command
"""
from logging.config import dictConfig

from flask import Flask
from flask_restplus import Api
from flask_cors import CORS
from app.core.models import db
import configs
from api import api_namespace
from app.core.models import init_engine, init_db

dictConfig(configs.LOGGING)


def create_app(flask_app=None):
    application = Flask(flask_app if flask_app is not None else __name__)
    application.config.from_object(configs)
    init_engine(application.config['SQLALCHEMY_DATABASE_URI'],
                pool_recycle=configs.DB_POOL_RECYCLE, pool_pre_ping=configs.DB_POOL_PRE_PING)
    init_db()
    api = Api(application)
    api.add_namespace(api_namespace, path='/api/1.0')
    CORS(application, resources=r'/api/*')
    db.init_app(application)
    return application
