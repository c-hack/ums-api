"""
Setup
"""
from setuptools import setup

setup(
    name='ums_api',
    packages=['ums_api'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'flask_jwt_extended',
        'flask_bcrypt',
        'flask_cors',
        'ldap3',
    ],
)
