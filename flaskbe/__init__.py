from config import config
from flask import Flask
from flask_oauthlib.provider import OAuth2Provider
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
oauth = OAuth2Provider()
from . import models


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASKBE_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    oauth.init_app(app)

    from .flaskbe import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .oauth_provider import oauth_provider as oauth_provider_blueprint
    app.register_blueprint(oauth_provider_blueprint, url_prefix='/oauth2')

    from .api_v1_0 import api_v1_0 as api_v1_0_blueprint
    app.register_blueprint(api_v1_0_blueprint, url_prefix='/api/v1.0')

    return app
