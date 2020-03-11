"""
This module contains all API endpoints for the namespace 'registrations'
"""
from flask import request
from flask_restplus import Resource, abort

from flask_jwt_extended import jwt_required

from . import API
from .api_models import REGISTRATION_GET, REGISTRATION_POST, EMAIL_VERIFICATION_POST
from .auth_helper import requires_user_creator

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
    @requires_user_creator()
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

@REGISTRATION_NS.route('/<int:registration_id>/')
class RegistrationDetail(Resource):
    """
    Single registration
    """
    @jwt_required
    @requires_user_creator()
    @API.marshal_with(REGISTRATION_GET)
    @REGISTRATION_NS.response(404, 'Requested registration not found!')
    # pylint: disable=R0201
    def get(self, registration_id):
        """
        Get the information about this registration
        """
        reg: Registration = Registration.query.filter(Registration.id == registration_id).first()
        if reg is None:
            abort(404, 'Requested registration not found!')
        return reg

    @jwt_required
    @requires_user_creator()
    @REGISTRATION_NS.response(204, 'Success.')
    @REGISTRATION_NS.response(404, 'Requested registration not found!')
    def delete(self, registration_id): 
        """
        Delete this registration
        """
        reg: Registration = Registration.query.filter(Registration.id == registration_id).first()
        if reg is None:
            abort(404, 'Requested registration not found!')
        DB.session.delete(reg)
        DB.session.commit()

        return "", 204

@REGISTRATION_NS.route('/<int:registration_id>/verifyMail/')
class EmailVerification(Resource):
    """
    Endpoint for verifying email addresses by posting the token
    """
    @REGISTRATION_NS.doc(body=EMAIL_VERIFICATION_POST)
    @REGISTRATION_NS.response(204, 'Ok.')
    @REGISTRATION_NS.response(404, 'Requested registration not found!')
    @REGISTRATION_NS.response(400, 'Wrong token.')
    def post(self, registration_id):
        """
        Verify the email address which the given token was sent to.
        """
        reg: Registration = Registration.query.filter(Registration.id == registration_id).first()
        if reg is None:
            abort(404, 'Requested registration not found!')
        
        json = request.get_json()
        token = json["token"]
        if registration_logic.process_token(reg, token):
            return None, 204
        abort(400, 'Wrong token.')


