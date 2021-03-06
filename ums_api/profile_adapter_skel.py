"""
This module contains the skeleton for the profile adapter class.
The real implementation is loaded at runtime by the profil_adapter_loader
"""
from typing import Dict, Tuple

from flask_restplus import fields

class ProfileAdapter():
    """
    The profile adapter class.
    This class needs to cotain various methods.
    It is loaded dynamically by the UMS during startup.
    Then the methods are used during the runtime.
    """

    def get_api_definition_registration(self, std_string_size: int) -> Dict[str, fields.Raw]:
        """
        Get the api definition for the registration endpoints.
        This should be a dict with string keys.
        The values should be flask_restplus fields like String or Float or Url.
        This dict is passes to API.model()
        """

    def get_relevant_data_registration(self, json: str) -> Tuple[str, str]:
        """
        Get the relevant data the system needs from the json of a registration.
        The relevant data is the username and email address for the new user.
        This method should return a tuple of these two. The email address may be None,
        if verifying email addresses is not supported.
        """

    def is_email_verification_supported(self) -> bool:
        """
        Whether the ability to require email verification for new accounts is supported by this adapter.
        If this returns true, get_relevant_data_registration should return valid email addresses.
        """
