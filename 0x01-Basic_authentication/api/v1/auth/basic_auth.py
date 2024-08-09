#!/usr/bin/env python3
''' basic_auth class module'''
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar


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
            return None, None
        if not isinstance(string, str):
            return None, None
        if ':' not in string:
            return None, None
        else:
            seperated = string.split(':')
            return tuple(seperated)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        '''returns User instance on email and password'''
        if not user_email or isinstance(user_email, str):
            return None
        if not user_pwd or isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception as e:
            return None

        for user in users:
            if not user.is_valid_password(user_pwd):
                return None
            return user

    def current_user(self, request=None) -> TypeVar('User'):
        '''overloads Auth and retrieves User instance'''
        header = self.authorization_header(request)
        encoded = self.extract+base64_authorization_header(header)
        decoded = self.decode_base64_athorization_header(encoded)
        user_cred = self.extract_user_credentials(decoded)
        if user_cred:
            return self.user_object_from_credentials(*user_cred)
        return None
