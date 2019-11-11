"""
Module containing database models for everything concerning Beverages.
"""

from .. import DB
from . import STD_STRING_SIZE

__all__ = [ 'Registration' ]


class Registration(DB.Model):
    """
    The representation of a Registration
    """

    __tablename__ = 'Registration'

    id = DB.Column(DB.Integer, primary_key=True)
    c_tag = DB.Column(DB.String(STD_STRING_SIZE))
    first_name = DB.Column(DB.String(STD_STRING_SIZE))
    last_name = DB.Column(DB.String(STD_STRING_SIZE))
    e_mail = DB.Column(DB.String(STD_STRING_SIZE))

    def __init__(self, c_tag: str, first_name: str, last_name: str, e_mail: str):
        self.c_tag = c_tag
        self.first_name = first_name
        self.last_name = last_name
        self.e_mail = e_mail
