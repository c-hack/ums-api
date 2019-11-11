"""
Module containing Debug Methods and sites.

This Module should only be loaded in debug Mode.
"""

from flask import Blueprint, render_template
from .. import APP

if not APP.config['DEBUG']:
    raise ImportWarning("This Module should only be loaded if DEBUG mode is active!")

debug_blueprint = Blueprint('debug_routes', __name__, template_folder='templates',
                            static_folder='static')

from . import routes


@debug_blueprint.route('/')
@debug_blueprint.route('/index')
def index():
    return render_template('debug/index.html',
                           title='UMS API – Debug')


APP.register_blueprint(debug_blueprint, url_prefix='/debug')
