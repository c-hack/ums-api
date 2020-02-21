"""
Module containing database models for everything concerning Beverages.
"""
from typing import Dict

from json import loads, dumps

import time

from .. import DB
from . import STD_STRING_SIZE

__all__ = ['Registration']


class Registration(DB.Model):
    """
    The representation of a Registration
    """

    __tablename__ = 'Registration'

    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(STD_STRING_SIZE))
    email = DB.Column(DB.String(STD_STRING_SIZE))
    data_json_string = DB.Column(DB.Text)
    token = DB.Column(DB.String(STD_STRING_SIZE))
    mail_sent = DB.Column(DB.Boolean)
    mail_confirmed = DB.Column(DB.Boolean)
    timestamp = DB.Column(DB.Integer)

    def __init__(self, username: str, email: str, data_json: Dict):
        self.username = username
        self.email = email
        self.data_json_string = dumps(data_json)
        self.mail_sent = False
        self.mail_confirmed = False
        self.timestamp = int(time.time())

    def get_data_json(self) -> Dict:
        """
        Get the json with the data about this registration
        """
        print(str(self.data_json_string))
        data = loads(self.data_json_string)
        print(str(data))
        return data
