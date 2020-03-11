"""
Module containing models for whole API to use.
"""

from flask_restplus import fields
from . import API
from ..db_models import STD_STRING_SIZE
from .. import PROFILE_ADAPTER


ID = API.model('Id', {
    'id': fields.Integer(min=1, example=1, readonly=True, title="Internal identifier"),
})

ROOT_MODEL = API.model('RootModel', {
    'registrations': fields.Url('api.registrations_registration_list'),
    'login': fields.Url('api.login_login_routes'),
    'profile': fields.Url('api.profile_profile_routes'),
    'doc': fields.Url('api.doc'),
    'spec': fields.Url('api.specs'),
})

REGISTRATION_DATA = API.model('RegistrationDATA', PROFILE_ADAPTER.get_api_definition_registration(STD_STRING_SIZE))

REGISTRATION_POST = API.model('RegistrationPOST', {
    'data': fields.Nested(REGISTRATION_DATA),
    'email_verification_url': fields.String(
        description=('URL for the email verification link. '
                     'A base64 encoded json will be added as the data url parameter.'))
})

REGISTRATION_GET = API.inherit('RegistrationGET', ID, {
    'data': fields.Nested(REGISTRATION_DATA, attribute=lambda x: x.get_data_json()),
    'username': fields.String(max_length=STD_STRING_SIZE, title='Username', readonly=True),
    'mail_confirmed': fields.Boolean(readonly=True)
})

EMAIL_VERIFICATION_POST = API.model('EmailVerificationPOST', {
    'token': fields.String(max_length=STD_STRING_SIZE, title='Token',
                           description='the email verification token send to the user')
})

LOGIN_ROUTES = API.model('LoginRoutes', {
    'full': fields.Url('api.login_full_login'),
    'basic': fields.Url('api.login_basic_login'),
    'refresh': fields.Url('api.login_refresh'),
})

LOGIN_POST = API.model('LoginPOST', {
    'username': fields.String(title='Username'),
    'password': fields.String(title='Password'),
})

JWT_RESPONSE_BASIC = API.model('JWT', {
    'access_token': fields.String(required=True)
})

JWT_RESPONSE_FULL = API.inherit('JWT_FULL', JWT_RESPONSE_BASIC, {
    'refresh_token': fields.String(reqired=True)
})

PROFILE_ROUTES = API.model('ProfileRoutes', {
    'data': fields.Url('api.profile_profile_data'),
    'password': fields.Url('api.profile_profile_password'),
})

PROFILE_DATA_PUT = API.model('ProfileDataPUT', {
    'first_name': fields.String(max_length=STD_STRING_SIZE, title='First Name'),
    'last_name': fields.String(max_length=STD_STRING_SIZE, title='Last Name'),
    'e_mail': fields.String(max_length=STD_STRING_SIZE, title='E-Mail Address'),
    'display_name': fields.String(max_length=STD_STRING_SIZE, title='Display Name'),
    'login_shell': fields.String(max_length=STD_STRING_SIZE, title='Login Shell'),
})

PROFILE_DATA_GET = API.model('ProfileDataGET', PROFILE_DATA_PUT, {
    'c-tag': fields.String(max_length=STD_STRING_SIZE, title='C-Tag (C-Hack Nickname)'),
})
