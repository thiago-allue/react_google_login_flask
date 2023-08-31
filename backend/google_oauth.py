"""
This module provides OAuth authentication using Google's OAuth2 API.
"""

import os
import requests
from flask import Blueprint, jsonify, redirect, url_for, request, session
from flask_oauthlib.client import OAuth

# Configuration for Google OAuth
GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']

oauth_bp = Blueprint('oauth', __name__)

# OAuth setup
oauth = OAuth()
google = oauth.remote_app(
    'google',
    consumer_key=GOOGLE_CLIENT_ID,
    consumer_secret=os.environ['YOUR_CLIENT_SECRET'],
    request_token_params={
        'scope': 'email profile'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


@oauth_bp.route('/google')
def google_login():
    """
    Redirects the user to Google's OAuth2 authorization page.
    """
    return google.authorize(callback=url_for('oauth.authorized', _external=True))


@oauth_bp.route('/callback')
def authorized():
    """
    Handles the callback after the user has authorized the application.
    """
    response = google.authorized_response()

    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    session['email'] = user_info.data['email']
    session['name'] = user_info.data['name']

    return redirect(url_for('page_homepage'))


@oauth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """
    Verifies the token received from the client with Google.
    """
    token = request.form['idtoken']

    # Verify the token with Google
    google_response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
    response_content = google_response.json()

    # Check if the token is valid for our app
    if response_content['aud'] != GOOGLE_CLIENT_ID:
        return jsonify({"error": "Invalid token"}), 401

    # Store user info in session
    session['user_id'] = response_content['sub']
    session['email'] = response_content['email']
    session['name'] = response_content['name']
    session['picture'] = response_content['picture']

    return jsonify({"message": "Logged in successfully"}), 200


@google.tokengetter
def get_google_oauth_token():
    """
    Returns the Google OAuth token from the session.
    """
    return session.get('google_token')
