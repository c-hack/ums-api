"""
This module contains all API endpoints for the namespace 'registrations'
"""
from flask import request
from flask_restplus import Resource, marshal

from . import API
from .api_models import REGISTRATION_GET, REGISTRATION_POST

from flask_jwt_extended import jwt_required

from .. import DB
from ..db_models.registration import Registration


REGISTRATION_NS = API.namespace('registrations', description='Registrations for the UMS', path='/registrations')

@REGISTRATION_NS.route('/')
class RegistrationList(Resource):
    """
    All current registrations
    """

    @API.marshal_list_with(REGISTRATION_GET)
    # pylint: disable=R0201
    def get(self):
        """
        Get a list of all registrations currently in the system
        """
        return Registration.query.all()

    @REGISTRATION_NS.doc(model=REGISTRATION_GET, body=REGISTRATION_POST)
    @REGISTRATION_NS.response(201, 'Created.')
    # pylint: disable=R0201
    def post(self):
        """
        Add a new registrations to the database
        """
        new = Registration(**request.get_json())

        DB.session.add(new)
        DB.session.commit()
        return marshal(new, REGISTRATION_GET), 201
