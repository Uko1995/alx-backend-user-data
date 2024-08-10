#!/usr/bin/env python3
''' session auth class module '''
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    '''session auth class'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''creates a session ID'''
        if not isinstance(user_id, str) or user_id is None:
            return None

        session_id = uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''returns a User ID based on session ID'''
        if not isinstance(session_id, str) or session_id is None:
            return None

        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        '''returns a User based on cookie value'''
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)
