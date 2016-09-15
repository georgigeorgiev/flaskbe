from flask import Blueprint

oauth_provider = Blueprint('oauth_provider', __name__)

from . import main
