"""
Copyright: Copyright 2020 Anton Zelenov

This file is subject to the terms and conditions defined in
file 'LICENSE', which is part of this source code package.
"""

from web.api.blueprint import api_blueprint
from flask import current_app, redirect
from urllib.parse import urlencode
from flask import request
from flask.json import jsonify
import requests
from common.queue import RedisQueue


# Google API URLs
GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
ACCESS_TOKEN_URL = 'https://oauth2.googleapis.com/token '
# And scope
GOOGLE_API_SCOPE = 'https://www.googleapis.com/auth/photoslibrary'

# Define auth callback here in case it used in multiple places
AUTH_CALLBACK_URL = 'auth_callback'
TOKEN_CALLBACK_URL = 'token_callback'


@api_blueprint.route('/auth', methods=['GET'])
def auth():
    """
    Return redirect to Google servers with following parameters:
    * client_id - client ID from Google console
    * redirect_uri - redirect to current service after auth
    * prompt - consent,select_account - ask user about consent and allow to select account
    * access_type - offline - we may refresh token without user
    * scope - https://www.googleapis.com/auth/photoslibrary - we need access to photos
    """
    parameters = urlencode(dict(
        client_id=current_app.config['GOOGLE_PHOTOS_CLIENT_ID'],
        redirect_uri=f'https://{current_app.config["DOMAIN"]}/api/{AUTH_CALLBACK_URL}',
        prompt='consent,select_account',
        access_type='offline',
        scope=GOOGLE_API_SCOPE,
    ))

    return redirect(f'{GOOGLE_AUTH_URL}?{parameters}')


@api_blueprint.route(f'/{AUTH_CALLBACK_URL}', methods=['GET'])
def auth_callback():
    error = request.args.get('error')

    # TODO: Add proper error handling
    if error is not None:
        return jsonify(dict(message=f'Received an error {error}')), 400

    scope = request.args.get('scope')

    # TODO: Add proper error handling
    if scope != GOOGLE_API_SCOPE:
        return jsonify(dict(message=f'The scope is invalid {scope}')), 400

    code = request.args.get('code')

    parameters = urlencode(dict(
        code=code,
        client_id=current_app.config['GOOGLE_PHOTOS_CLIENT_ID'],
        client_secret=current_app.config['GOOGLE_PHOTOS_SECRET'],
        grant_type='authorization_code',
        redirect_uri=f'https://{current_app.config["DOMAIN"]}/{TOKEN_CALLBACK_URL}',
    ))

    # TODO: Make this call to Google API async
    result = requests.post(f'{ACCESS_TOKEN_URL}?{parameters}')

    # TODO: error handling
    access_token = result.json()['access_token']
    refresh_token = result.json()['refresh_token']

    queue = RedisQueue('jobs')
    queue.push(dict(
            access_token=access_token,
            refresh_token=refresh_token
        ))

    return jsonify(message='ok'), 200

