"""
Module containing models for whole API to use.
"""

from flask_restplus import fields
from . import API
from ..db_models import STD_STRING_SIZE


ID = API.model('Id', {
    'id': fields.Integer(min=1, example=1, readonly=True, title="Internal identifier"),
})

ROOT_MODEL = API.model('RootModel', {
    'registrations': fields.Url('api.registrations_registration_list'),
})

REGISTRATION_POST = API.model('RegistrationPOST', {
    'c_tag': fields.String(max_length=STD_STRING_SIZE, title='C-Tag'),
    'first_name': fields.String(max_length=STD_STRING_SIZE, title='First Name'),
    'last_name': fields.String(max_length=STD_STRING_SIZE, title='Last Name'),
    'e_mail': fields.String(max_length=STD_STRING_SIZE, title='E-Mail Address'),
})

REGISTRATION_PUT = API.inherit('RegistrationPUT', REGISTRATION_POST, {})

REGISTRATION_GET = API.inherit('RegistrationGET', REGISTRATION_PUT, ID)
