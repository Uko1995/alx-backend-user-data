#!/usr/bin/env python3
''' authentication class module '''
from flask import request
from typing import List, TypeVar
import os


class Auth:
    '''auth class'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''reqiure_auth method'''
        if not path or not excluded_paths or len(excluded_paths) == 0:
            return True

        if path[-1] != '/':
            path += '/'

        for p in excluded_paths:
            if p.endswith('*'):
                if path.startswith(p[-1]):
                    return False

        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        '''authorization_header method'''
        if request is None:
            return None

        authorization = request.headers.get('Authorization', None)
        if authorization is None:
            return None
        return authorization

    def current_user(self, request=None) -> TypeVar('User'):
        '''current_user method'''
        return None

    def session_cookie(self, request=None):
        '''returns cookie value from a request'''
        if request is None:
            return None
        _my_session_id = os.getenv('SESSION_NAME', None)
        return request.cookies.get(_my_session_id)
