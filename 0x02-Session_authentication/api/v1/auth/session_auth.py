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
