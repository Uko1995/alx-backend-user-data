#!/usr/bin/env python3
'''function that returns thelog message obfuscated'''
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    '''filter_datum function
    arguments:
    fields: list of strings to obfuscate
    redaction: string to be obfuscated
    message: string representing the log line
    seperator: a string of characters to represent fields in message
    '''
    for field in fields:
        message = re.sub(rf'({re.escape(field)}=)[^{separator}]*',
                         rf'\1{redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        ''' format method'''
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
