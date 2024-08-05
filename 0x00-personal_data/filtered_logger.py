#!/usr/bin/env python3
'''function that returns thelog message obfuscated'''
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 seperator: str) -> str:
    '''filter_datum function
    arguments:
    fields: list of strings to obfuscate
    redaction: string to be obfuscated
    message: string representing the log line
    seperator: a string of characters to represent fields in message
    '''
    for field in fields:
        message = re.sub(rf'({re.escape(field)}=)[^{seperator}]*',
                         rf'\1{redaction}', message)
    return message
