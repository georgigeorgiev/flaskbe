from datetime import datetime, timedelta
from flaskbe.models.main import User
import oauthlib
from flask import jsonify
from flaskbe.models.oauth_provider import Client, Grant, Token
from flaskbe.oauth_provider import oauth_provider
from .. import db, oauth


@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()


@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=request.user,
        expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    return grant


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()

from datetime import datetime, timedelta


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query.filter_by(client_id=request.client.client_id,
                                 user_id=request.user.id)
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)

    expires_in = token.get('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    db.session.add(tok)
    db.session.commit()
    return tok


@oauth.usergetter
def get_user(username, password, *args, **kwargs):
    user = User.query.filter_by(email=username).first()
    return user


@oauth.authorize_handler
def authorize(*args, **kwargs):
    return True


@oauth_provider.route('/token')
@oauth.token_handler
def access_token():
    return None


@oauth_provider.route('/start', methods=['GET'])
@oauth.require_oauth()
def start():
    return jsonify({'message': 'hello from oauth'})
