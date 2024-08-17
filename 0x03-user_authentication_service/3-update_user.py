#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


my_db = DB()

email = 'test@test.com'
hashed_password = "hashedPwd"

user = my_db.add_user(email, hashed_password)
print(user.id, user.email, user.hashed_password)

try:
    my_db.update_user(user.id, hashed_password='NewPwd')
    print("Password updated")
except ValueError:
    print("Error")

print(user.id, user.email, user.hashed_password)

#-------------

next_user = my_db.add_user('jneric49@mail.com', 'jon')
print(next_user.id, next_user.email, next_user.hashed_password)

try:
    my_db.update_user(next_user.id, hashed_pword='NewPwd')
    print("Password updated")
except ValueError:
    print("Error")

print(next_user.id, next_user.email, next_user.hashed_password)
