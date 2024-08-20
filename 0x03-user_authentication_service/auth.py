#!/usr/bin/env python3
""" Authentication module
"""
import bcrypt
import uuid

from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional


def _hash_password(password: str) -> bytes:
    """ Encrypts a password string and returns it
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ Generates a string representation of universally unique id
    """
    return uuid.uuid4().__str__()


class Auth:
    """ Authentication class proxying the DB model to authenticate users
    before performing CRUD operations on them.
    """

    def __init__(self):
        """ Instantiates Authentication Database
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a new user given their email address and password
          - If a user with that same email exists, it raises a exception
                ValueError: User <email> already exists
          - Otherwise it hashes the password and save the user to the database
        """
        # Checking if user already exists
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:  # User can be added
            user = self._db.add_user(email, _hash_password(password), )
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """ Validates a user's login given user email and password
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> uuid.UUID:
        """ Creates a session for the user with the given email
        """
        try:
            user = self._db.find_user_by(email=email)  # Find user
            session_id = _generate_uuid()  # Generates user session id
            self._db.update_user(user.id, session_id=session_id)
        except NoResultFound:
            session_id = None
        finally:
            return session_id

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """ Finds a user with the given session id
        """
        if session_id is None:
            session_id = ""  # Avoid retrieving user with empty session field
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """ Destroys a user's session, or rather logs out the user
        """
        self._db.update_user(user_id, session_id="")

    def get_reset_password_token(self, email: str) -> str:
        """ Generates a user's reset password token given their email address
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:  # User doesn't exist
            raise ValueError
        else:
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updates a users password
        """
        if reset_token is None:
            reset_token = "" # Avoid retrieving user's with empty token field
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        else:
            self._db.update_user(
                    user.id,
                    hash_password=_hash_password(password),
                    reset_token=None
                )
