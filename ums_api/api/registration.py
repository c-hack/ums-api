"""
This module contains all API endpoints for the namespace 'registrations'
"""
from flask import request, url_for
from flask_restplus import Resource, abort

from flask_jwt_extended import jwt_required

from . import API
from .api_models import REGISTRATION_GET, REGISTRATION_POST, EMAIL_VERIFICATION_POST

from .. import DB
from .. import PROFILE_ADAPTER
from ..db_models.registration import Registration
from ..logic import registration as registration_logic

REGISTRATION_NS = API.namespace('registrations', description='Registrations for the UMS', path='/registrations')

@REGISTRATION_NS.route('/')
class RegistrationList(Resource):
    """
    All current registrations
    """
    @jwt_required
    @API.marshal_list_with(REGISTRATION_GET)
    # pylint: disable=R0201
    def get(self):
        """
        Get a list of all registrations currently in the system
        """
        return Registration.query.all()

    @REGISTRATION_NS.doc(body=REGISTRATION_POST)
    @API.marshal_with(REGISTRATION_GET)
    @REGISTRATION_NS.response(201, 'Created.')
    # pylint: disable=R0201
    def post(self):
        """
        Add a new registrations to the database
        """
        json = request.get_json()
        data = json['data']
        email_verification_url = json['email_verification_url']

        username, email = PROFILE_ADAPTER.get_relevant_data_registration(data)
        new = Registration(username, email, data)

        DB.session.add(new)
        DB.session.commit()

        registration_logic.submit_registration(new, email_verification_url)

        return new, 201

@REGISTRATION_NS.route('/emailVerification/')
class EmailVerification(Resource):
    """
    Endpoint for verifying email addresses by posting the token
    """
    @REGISTRATION_NS.doc(body=EMAIL_VERIFICATION_POST)
    @REGISTRATION_NS.response(204, 'Ok.')
    @REGISTRATION_NS.response(400, 'Unknown token.')
    def post(self):
        """
        Verify the email address which the given token was sent to.
        """
        json = request.get_json()
        token = json["token"]
        if registration_logic.process_token(token):
            return None, 204
        abort(400, 'Unknown token.')



