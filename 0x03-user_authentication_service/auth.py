#!/usr/bin/env python3
'''methos that hashes a password'''

import bcrypt


def _hash_password(password: str) -> bytes:
    '''returns bytes of the salted hash'''
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt)
