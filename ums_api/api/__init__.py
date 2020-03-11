"""
Main API Module
"""
from flask import Blueprint
from flask_restplus import Api
from .. import APP

AUTHORIZATIONS = {
    'jwt': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Standard JWT access token.'
    },
    'jwt-refresh': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT refresh token.'
    }
}

API_BLUEPRINT = Blueprint('api', __name__)

API = Api(API_BLUEPRINT, version='0.1', title='UMS API', doc='/doc/',
          description='The C-Hack User Management System API.', authorizations=AUTHORIZATIONS, security='jwt')

# pylint: disable=C0413
from . import auth_helper, root, registration, login, profile

APP.register_blueprint(API_BLUEPRINT)
