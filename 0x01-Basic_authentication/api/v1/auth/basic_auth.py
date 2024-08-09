#!/usr/bin/env python3
''' basic_auth class module'''
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        '''decodesbase64 authorization'''
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_str = base64.b64decode(base64_authorization_header)
            decoded_utf8 = decoded_str.decode('utf-8')
            return decoded_utf8
        except Exception as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        '''extracts email and password'''
        string = decoded_base64_authorization_header
        if not string:
            return None
        if not isinstance(string, str):
            return None
        if ':' not in string:
            return None
        else:
            seperated = string.split(':')
            return tuple(seperated)
