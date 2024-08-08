#!/usr/bin/env python3
''' basic_auth class module'''
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    '''Basic_Auth class'''
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        '''extracts the authorization header'''
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        if 'Basic ' not in authorization_header:
            return None
        return authorization_header[6:]
