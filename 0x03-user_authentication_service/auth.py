#!/usr/bin/env python3
'''method that hashes a password'''

import bcrypt
from uuid import uuid4
from user import Base, User
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    '''returns bytes of the salted hash'''
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt)


def _generate_uuid() -> str:
    '''generates a new UUID'''
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''returns a user object'''
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        '''implements a valid login'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        '''generates session_id for user'''
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        '''takes session_id and returns User'''
        if session_id is None:
            return None
        try:
            user = self_db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        '''destroys session'''
        self_db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        '''gets reset token'''
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            user.reset_token = token
            return token
        except Exception:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        ''' updates password'''
        user = self._db.find_user_by(reset_token=reset_token)
        if not user:
            raise ValueError()
        else:
            passw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self._db.update_user(
                user.id, hashed_password=passw, reset_token=None)
