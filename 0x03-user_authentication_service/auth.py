#!/usr/bin/env python3
""" Authentication module
"""
import bcrypt
from db import DB

from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(passwd: str) -> bytes:
    """ Encrypts a password string and returns it
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(passwd.encode(), salt)


class Auth:
    """ Auth class to interact with the authentication database
    """

    def __init__(self):
        """ Instantiates Authentication Database
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a user given their email address and password
          - If a user with that same email exists, it raises a exception
                ValueError: User <email> already exists
          - Otherwise it hashes the password and save the user to the database
        """
        # Checking if user already exists
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:  # User can be added
            user = self._db.add_user(email, _hash_password(password))

        return user
