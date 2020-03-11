"""
The logic for registration
"""
from json import dumps
from base64 import urlsafe_b64encode
from secrets import token_urlsafe
from urllib.parse import urlsplit, urlunsplit

from flask import url_for

from .. import APP, DB
from ..db_models.registration import Registration

from . import email

def get_token_url(registration: Registration, frontend_email_verification_url: str) -> str:
    """
    Generate the url for email address verification mail containing the given token.
    To undo in JS: JSON.parse(atob(new URLSearchParams(window.location.search).get('data'))).token
    """
    data = {
        'token': registration.token,
        'verification_url': url_for("api.registrations_email_verification", registration_id=registration.id, _external=True)
    }
    data_encoded = urlsafe_b64encode(dumps(data, separators=(',', ':')).encode())
    old_url = urlsplit(frontend_email_verification_url)
    new_query = old_url.query
    if len(new_query) != 0:
        new_query += "&"
    new_query += "data=" + data_encoded.decode()
    new_url = [old_url.scheme, old_url.netloc, old_url.path, new_query, old_url.fragment]
    return urlunsplit(new_url)

def generate_token(registration: Registration):
    """
    Generate a new token for the given registration
    """
    registration.token = token_urlsafe()
    DB.session.commit()

def submit_registration(registration: Registration, email_verification_url: str):
    """
    Submit a new registration. Will return the state of the new registration.
    """
    if APP.config["REGISTRATION_VERIFY_EMAILS"]:
        generate_token(registration)
        email.send_registraion_email(registration.email, get_token_url(registration, email_verification_url))
        registration.mail_sent = True
        DB.session.commit()
    else:
        registration.mail_confirmed = True
        DB.session.commit()

def process_token(registration: Registration, token: str) -> bool:
    """
    Process an email verification token.
    Returns whether the token was valid.
    """
    if registration.token != token:
        return False
    registration.mail_confirmed = True
    DB.session.commit()
    return True
