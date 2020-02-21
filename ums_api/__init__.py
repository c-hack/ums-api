"""
UMS api init file.
"""
from os import environ
from os.path import abspath

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import MetaData
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from .logging import init_logging, get_logging
from .profile_adapter_loader import load_profile_adapter

APP = Flask(__name__, instance_relative_config=True)  # type: Flask
APP.config['MODE'] = environ['MODE'].upper()
if APP.config['MODE'] == 'PRODUCTION':
    APP.config.from_object('ums_api.config.ProductionConfig')
elif APP.config['MODE'] == 'DEBUG':
    APP.config.from_object('ums_api.config.DebugConfig')
elif APP.config['MODE'] == 'TEST':
    APP.config.from_object('ums_api.config.TestingConfig')

APP.config.from_pyfile('/etc/ums_api.conf', silent=True)
APP.config.from_pyfile('ums_api.conf', silent=True)
if 'CONFIG_FILE' in environ:
    APP.config.from_pyfile(environ.get('CONFIG_FILE', 'ums_api.conf'), silent=True)

ENV_VARS = ('SQLALCHEMY_DATABASE_URI', 'JWT_SECRET_KEY', 'USER_ID_SECRET_KEY')
for env_var in ENV_VARS:
    APP.config[env_var] = environ.get(env_var, APP.config.get(env_var))

SECRETS = ('JWT_SECRET_KEY', 'USER_ID_SECRET_KEY')
for var in SECRETS:
    if not APP.config[var]:
        raise ValueError("The secret " + var + " is not set!")
try:
    if len(bytes(APP.config['USER_ID_SECRET_KEY'])) != 32:
        raise ValueError("The secret USER_ID_SECRET_KEY must be exactly 32 bytes long!")
except TypeError:
    raise ValueError("The secret USER_ID_SECRET_KEY must be a bytes object. Use b'whatever' to create one.")

init_logging(APP)

APP_LOGGER = get_logging().APP_LOGGER

# Setup DB with Migrations and bcrypt
APP_LOGGER.info('Connecting to database %s.', APP.config['SQLALCHEMY_DATABASE_URI'])
DB: SQLAlchemy
DB = SQLAlchemy(APP, metadata=MetaData(naming_convention={
    'pk': 'pk_%(table_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s',
    'ix': 'ix_%(table_name)s_%(column_0_name)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
}))

MIGRATE: Migrate = Migrate(APP, DB)

# Setup JWT
JWT: JWTManager = JWTManager(APP)

# Setup Headers
CORS(APP)

PROFILE_ADAPTER = load_profile_adapter(abspath(APP.config["PROFILE_ADAPTER_PLUGIN"]))

if APP.config["REGISTRATION_VERIFY_EMAILS"] and not PROFILE_ADAPTER.is_email_verification_supported():
    raise ValueError('E-Mail Verification is turned on but not supported by the adapter!')

# pylint: disable=C0413
from . import db_models
# pylint: disable=C0413
from . import routes
