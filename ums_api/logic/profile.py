"""
The logic for user profiles
"""
from typing import Dict

from .auth import get_login_data_from_uid_token

def get_profile(uid_token: str) -> Dict:
    """ Get the profile of the user behind the uid token. """
    username, user_dn, password = get_login_data_from_uid_token(uid_token)
    return {'username': username}

def update_profile(uid_token: str, data: Dict):
    """ Update the profile of the user behind the uid_token. """
    username, user_dn, password = get_login_data_from_uid_token(uid_token)
    #TODO