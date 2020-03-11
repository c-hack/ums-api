"""
This module contains all API endpoints for the namespace 'login'
"""
from typing import Dict

from flask import request
from flask_restplus import Resource, abort

from flask_jwt_extended import create_access_token, \
                               get_jwt_identity, create_refresh_token, \
                               get_jwt_claims, jwt_refresh_token_required

from . import API
from .auth_helper import User
from .api_models import LOGIN_POST, JWT_RESPONSE_BASIC, JWT_RESPONSE_FULL, LOGIN_ROUTES

from ..logging import AUTH_LOGGER
from ..logic import auth

LOGIN_NS = API.namespace('login', description='Login to the UMS', path='/login')


def login_from_request() -> User:
    """
    Login with the login data provided by the current request.
    Returns the username and uid token.
    """
    username = request.get_json()['username']
    password = request.get_json()['password']

    uid_token = auth.login(username, password)

    if not uid_token:
        abort(401, 'Wrong username or pasword.')

    return User(username, uid_token)

def get_full_jwt(user: User) -> Dict:
    """
    Get a full jwt response from the username and uid token.
    """
    return {
        'access_token': create_access_token(identity=user, fresh=True),
        'refresh_token': create_refresh_token(identity=user)
    }

def get_basic_jwt_fresh(user: User) -> Dict:
    """
    Get a fresh basic jwt response from the username and uid token.
    """
    return {
        'access_token': create_access_token(identity=user, fresh=True),
    }

def get_basic_jwt_unfresh(user: User) -> Dict:
    """
    Get a unfresh basic jwt response from the username and uid token.
    """
    return {
        'access_token': create_access_token(identity=user, fresh=False),
    }


@LOGIN_NS.route('/')
class LoginRoutes(Resource):
    """Login Routes resource."""

    @API.marshal_with(LOGIN_ROUTES)
    # pylint: disable=R0201
    def get(self):
        """Get the login routes."""
        return {}

@LOGIN_NS.route('/full/')
class FullLogin(Resource):
    """
    Perform a full login
    """

    @LOGIN_NS.doc(body=LOGIN_POST)
    @API.response(401, 'Wrong username or pasword.')
    @API.marshal_with(JWT_RESPONSE_FULL)
    # pylint: disable=R0201
    def post(self):
        """
        Login
        """

        return get_full_jwt(login_from_request())

@LOGIN_NS.route('/basic/')
class BasicLogin(Resource):
    """
    Perform a basic login
    """

    @LOGIN_NS.doc(body=LOGIN_POST)
    @API.response(401, 'Wrong username or pasword.')
    @API.marshal_with(JWT_RESPONSE_BASIC)
    # pylint: disable=R0201
    def post(self):
        """
        Login
        """

        return get_basic_jwt_fresh(login_from_request())

@LOGIN_NS.route('/refresh/')
class Refresh(Resource):
    """
    Get a new access token with the refresh token
    """

    @jwt_refresh_token_required
    @API.marshal_with(JWT_RESPONSE_BASIC)
    # pylint: disable=R0201
    def post(self):
        """
        Create a new access token with a refresh token.
        """
        username = get_jwt_identity()
        uid_token = get_jwt_claims()["uid_token"]
        AUTH_LOGGER.debug('User "%s" asked for a new access token.', username)
        return get_basic_jwt_unfresh(User(username, uid_token))
