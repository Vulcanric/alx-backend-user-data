#!/usr/bin/env python3
""" DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import (Tuple, Dict, Optional)

from user import Base
from user import User


class DB:
    """ DB class
    """

    def __init__(self) -> None:
        """ Initialize a new DB instance
        """
        self._engine = create_engine('sqlite:///a.db', echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session: Optional[Session] = None

    @property
    def _session(self) -> Session:
        """ Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Creates a user object, adds it to the database and returns it.
        """
        user = User(
                email=email,
                hashed_password=hashed_password,
                session_id=""
            )
        self._session.add(user)  # Property function, don't have to call it
        self._session.commit()  # Save user to database
        return user

    def find_user_by(self, **attributes) -> User:
        """ Find a user identified by @attributes kwargs
        """
        user_attrs = {
                'id': User.id,
                'email': User.email,
                'hashed_password': User.hashed_password,
                'session_id': User.session_id,
                'reset_token': User.reset_token
            }

        query = self._session.query(User)  # Query the users table

        for attr, value in attributes.items():  # Filter by inputed value
            try:
                query = query.filter(user_attrs[attr] == value)
            except KeyError:  # Invalid attribute name, not found in User
                raise InvalidRequestError

        result = query.first()
        if not result:
            raise NoResultFound

        return result

    def update_user(self, user_id: int, **attributes) -> None:
        """ Updates a user's @attributes, identified by @user_id
        """
        for attr in attributes.keys():
            if attr not in (
                    "email", "hashed_password",
                    "session_id", "reset_token"
                    ):
                raise ValueError

        user = self.find_user_by(id=user_id)

        for attr, value in attributes.items():
            setattr(user, attr, value)
        self._session.commit()  # Save updated user to database
