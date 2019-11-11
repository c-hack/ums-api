"""Module containing default config values."""
from random import randint

class Config(object):
    DEBUG = False
    TESTING = False
    RESTPLUS_VALIDATE = True
    JWT_CLAIMS_IN_REFRESH_TOKEN = True
    JWT_SECRET_KEY = ''.join(hex(randint(0, 255))[2:] for i in range(16))
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_UNIQUE_CONSTRAIN_FAIL = 'UNIQUE constraint failed'
    URI_BASE_PATH = '/'

    LDAP_URI = ""
    LDAP_PORT = 0
    LDAP_SSL = False
    LDAP_START_TLS = False
    LDAP_USER_SEARCH_BASE = ""
    LDAP_GROUP_SEARCH_BASE = ""
    LDAP_USER_RDN = ""
    LDAP_USER_UID_FIELD = ""
    LDAP_GROUP_MEMBERSHIP_FIELD = ""
    LDAP_CONSUMER_FILTER = ""
    LDAP_KIOSK_USER_FILTER = ""
    LDAP_ADMIN_FILTER = ""
    LDAP_CONSUMER_GROUP_FILTER = ""
    LDAP_KIOSK_USER_GROUP_FILTER = ""
    LDAP_ADMIN_GROUP_FILTER = ""

    LOGGING_CONFIGS = ['logging_config.json']

    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    RESTPLUS_JSON = {'indent': None}


class ProductionConfig(Config):
    pass


class DebugConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    JWT_SECRET_KEY = 'debug'

    LOGGING_CONFIGS = ['logging_config.json', 'logging_config_debug.json']


class TestingConfig(Config):
    TESTING = True
