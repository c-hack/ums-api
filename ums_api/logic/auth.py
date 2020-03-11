"""
The logic for authentication (logging in) and authorization (checking if a user can do something)
"""
from typing import Optional, Tuple

from base64 import standard_b64encode, standard_b64decode

from Crypto.Cipher import AES
from Crypto import Random

from .ldap import verify_bind, check_user_matches_filter

from .. import APP

def login(username: str, password: str) -> Optional[str]:
    """
    Login the given user with the given password.
    If successful returns the user identifier token for the user.
    """
    user_dn = verify_bind(username, password)
    if user_dn is None:
        return None
    encoded_username: bytes = standard_b64encode(username.encode(encoding='UTF-8', errors='strict'))
    encoded_user_dn: bytes = standard_b64encode(user_dn.encode(encoding='UTF-8', errors='strict'))
    encoded_password: bytes = standard_b64encode(password.encode(encoding='UTF-8', errors='strict'))
    data = bytes(encoded_username + b":" + encoded_user_dn + b":" + encoded_password)
    print(str(data))
    init_vector: bytes = Random.new().read(AES.block_size)
    cipher = AES.new(APP.config['USER_ID_SECRET_KEY'], AES.MODE_CFB, init_vector, segment_size=8)
    cipher_text = cipher.encrypt(data)
    return standard_b64encode(init_vector + cipher_text).decode(encoding='UTF-8', errors='strict')

def get_login_data_from_uid_token(uid_token: str) -> Tuple[str, str, str]:
    """
    Decrypts the given user identifier token.
    Returns the users username, user dn and password.
    """
    uid_bytes = standard_b64decode(uid_token.encode(encoding='UTF-8', errors='strict'))
    init_vector = uid_bytes[:AES.block_size]
    cipher_text = uid_bytes[AES.block_size:]
    cipher = AES.new(APP.config['USER_ID_SECRET_KEY'], AES.MODE_CFB, init_vector, segment_size=8)
    data = cipher.decrypt(cipher_text)
    parts = data.split(b":")
    print(str(parts))
    if len(parts) != 3:
        raise ValueError("data is wrong format:")
    username = standard_b64decode(parts[0]).decode(encoding='UTF-8', errors='strict')
    user_dn = standard_b64decode(parts[1]).decode(encoding='UTF-8', errors='strict')
    password = standard_b64decode(parts[2]).decode(encoding='UTF-8', errors='strict')
    return [username, user_dn, password]

def is_user_allowed_to_create_users(uid_token: str) -> bool:
    """
    Check if the user identified by the given uid toke is allowed to create users
    Returns True if this is the case, False otherwise.
    """
    _, user_dn, pw = get_login_data_from_uid_token(uid_token)
    return check_user_matches_filter(user_dn, pw, APP.config["USER_CREATOR_FILTER"])
