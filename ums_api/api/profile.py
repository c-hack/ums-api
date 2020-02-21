"""
This module contains all API endpoints for the namespace 'profile'
"""
from typing import Dict

from flask import request
from flask_restplus import Resource, abort

from flask_jwt_extended import jwt_required

from . import API
from .api_models import PROFILE_DATA_GET, PROFILE_DATA_PUT, PROFILE_ROUTES

from .. import JWT
from ..logging import AUTH_LOGGER
from ..logic import profile

PROFILE_NS = API.namespace('profile', description='The profile of the logged in user.', path='/profile')

@PROFILE_NS.route('/')
class ProfileRoutes(Resource):
    """Profile routes resource."""

    @API.marshal_with(PROFILE_ROUTES)
    # pylint: disable=R0201
    def get(self):
        """Get the profile routes."""
        return {}

@PROFILE_NS.route('/data/')
class ProfileData(Resource):
    """Profile data resource."""

    @jwt_required
    @API.marshal_with(PROFILE_DATA_GET)
    # pylint: disable=R0201
    def get(self):
        """
        Get the current users profile data.
        """
        #TODO get login token
        return None