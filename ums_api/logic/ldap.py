"""
All logic interacting with the ldap server
"""
from typing import Optional
from ldap3 import Connection, Server, AUTO_BIND_TLS_BEFORE_BIND, SUBTREE, AUTO_BIND_NO_TLS, AUTO_BIND_NONE

from .. import APP
from ..logging import AUTH_LOGGER

server: Server = Server(APP.config["LDAP_URI"], port=APP.config["LDAP_PORT"], use_ssl=APP.config["LDAP_SSL"])


def get_auto_bind() -> str:
    auto_bind = AUTO_BIND_NO_TLS

    if APP.config["LDAP_START_TLS"]:
        auto_bind = AUTO_BIND_TLS_BEFORE_BIND
    return auto_bind

def find_user(username: str) -> Optional[str]:
    """
    Find the user identified by the given username.
    Returns the distinguished name (dn) of the entry or None if none was found.
    """

    user = None
    password = None

    if not APP.config["LDAP_ANONYMOUS_BIND"]:
        user = APP.config["LDAP_SYSTEM_USER_DN"]
        password = APP.config["LDAP_SYSTEM_USER_PW"]

    user_filter = APP.config["LOGIN_SEARCH_USER_FILTER"]

    user_filter = user_filter.replace("%", username)

    with Connection(server, auto_bind=get_auto_bind(), read_only=True, user=user, password=password) as conn:
        if not conn.search(APP.config["LDAP_USER_SEARCH_BASE"], user_filter, search_scope=SUBTREE):
            AUTH_LOGGER.info("Cannot find a user matching the name %s.", username)
            return None
        return conn.response.pop()["dn"]

def generate_user_dn(username: str) -> str:
    """
    Generate the user dn based on the configured pattern.
    Returns the distinguished name (dn) of the entry.
    """
    return APP.config["LOGIN_USER_DN_PATTERN"].replace("%", username)

def verify_bind(username: str, password: str) -> Optional[str]:
    """
    Verify that the given user can bind to the ldap server with the given password.
    Therefore this can be used to check the password of a user.
    If bind is succesfull returns the user dn, otherwise None
    """
    user_dn: str

    if APP.config["LOGIN_SEARCH_USER"]:
        result = find_user(username)
        if not result:
            return None
        user_dn = result
    else:
        user_dn = generate_user_dn(username)

    with Connection(server, auto_bind=AUTO_BIND_NONE, read_only=True, user=user_dn, password=password) as conn:
        if APP.config["LDAP_START_TLS"]:
            conn.start_tls()
        if not conn.bind():
            AUTH_LOGGER.info("User failed to log in: %s.", username)
            return None
        return user_dn

def check_user_matches_filter(user_dn: str, password: str, ldap_filter: str) -> bool:
    """
    Check whether a user matches a ldap filter.
    Pass the user dn, the password for the user and the ldap_filter as parameters.
    Returns True if the given user matches the filter
    """
    with Connection(server, auto_bind=get_auto_bind(), read_only=True, user=user_dn, password=password) as conn:
        if not conn.search(APP.config["LDAP_USER_SEARCH_BASE"], ldap_filter, search_scope=SUBTREE):
            return False
        return user_dn in [resp["dn"] for resp in conn.response]
