from config import config
from flask import Flask
from flask.ext.mongoalchemy import MongoAlchemy
import os

db = MongoAlchemy()
from . import models


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASKBE_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from .flaskbe import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api_v1_0 import api_v1_0 as api_v1_0_blueprint
    app.register_blueprint(api_v1_0_blueprint, url_prefix='/api/v1.0')

    return app
