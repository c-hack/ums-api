"""Module containing default config values."""

class Config(object):
    DEBUG = False
    TESTING = False
    RESTPLUS_VALIDATE = True
    JWT_CLAIMS_IN_REFRESH_TOKEN = True
    JWT_SECRET_KEY = ''
    USER_ID_SECRET_KEY = ''
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

    LDAP_ANONYMOUS_BIND = False

    #The following block is only used when LDAP_ANONYMOUS_BIND is False
    LDAP_SYSTEM_USER_DN = ""
    LDAP_SYSTEM_USER_PW = ""

    LOGGING_CONFIGS = ['logging_config.json']

    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    RESTPLUS_JSON = {'indent': None}

    PROFILE_ADAPTER_PLUGIN = "example_profile_adapter.py"

    MAIL_SERVER_HOST = ""
    MAIL_SERVER_PORT = 25
    MAIL_SERVER_SSL = False
    MAIL_SERVER_STARTTLS = True
    MAIL_SERVER_LOGIN = True
    MAIL_SERVER_USER = ""
    MAIL_SERVER_PW = ""
    MAIL_SENDING_ADDRESS = ""

    REGISTRATION_VERIFY_EMAILS = True
    REGISTRATION_MAIL_SUBJECT = "Welcome to UMS"
    REGISTRATION_MAIL_BODY = "Hi, \n\nyou have just registered at our UMS. \n" \
                             "Please click the following link to continue the registration process: \n" \
                             "{} \n\nCheers \nYour admins"

    LOGIN_SEARCH_USER = True

    #Only used if LOGIN_SEARCH_USER user is True
    #The character % will be replaced by the username which is searched
    LOGIN_SEARCH_USER_FILTER = ""

    #Only used if LOGIN_SEARCH_USER user is False
    #The character % will be replaced by the username
    LOGIN_USER_DN_PATTERN = ""

    USER_CREATOR_FILTER = ""

    # If True LDAP_ANONYMOUS_BIND must be False and the LDAP_SYSTEM_USER_DN must be able to write to the password field of users.
    ALLOW_PASSWORD_RESET_BY_SYSTEM = True

class ProductionConfig(Config):
    pass


class DebugConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    JWT_SECRET_KEY = 'debug'
    USER_ID_SECRET_KEY = b'0123456789ABCDEF0123456789ABCDEF'

    LOGGING_CONFIGS = ['logging_config.json', 'logging_config_debug.json']


class TestingConfig(Config):
    TESTING = True
