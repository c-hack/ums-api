"""
Main API Module
"""
from flask import Blueprint
from flask_restplus import Api
from .. import APP

API_BLUEPRINT = Blueprint('api', __name__)

API = Api(API_BLUEPRINT, version='0.1', title='UMS API', doc='/doc/',
          description='The C-Hack User Management System API.')

from . import root, registration

APP.register_blueprint(API_BLUEPRINT)
