#!/usr/bin/env python3
""" Defines a function filter_datum that returns log message obfuscated
"""
import re
import logging
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
) -> str:
    """ Filters a log message and returns it obfuscated.

    Arguments
    _________

        fields : list
            List of strings representing all fields to obfuscate.

        redaction : str
            String representing by what the field will be obfu-
scated.
        message : str
            String representing the log line

        separator : str
            String representing by which character is separati-
ng all fields.

    Example
    ________

>>> fields = ["password", "dob"]
>>> message = "name=mark;email=mark@mail.com;password=1234;dob=12/3/2005;"
>>> filter_datum(fields, 'xxx', message, ';')
name=matthew;email=matthew@example.com;password=xxx;dob=xxx;
    """
    for field in fields:
        message = re.sub(
                f'{field}=\\S+?{separator}',  # Target field substring
                f'{field}={redaction}{separator}',  # Obfuscated replacement
                message
            )
    return message


class RedactingFormatter(logging.Formatter):
    """ A custom log formatter class, that redacts logs for security.
    It inherits from the logging.Formatter class

    Attributes
    __________

    fields : list of str
        List of strings representing all fields to obfuscate.

    Methods
    _______

    format(record: logging.LogRecord) -> str:
        Formats log records, obfuscating PII fields as specified by @fields
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format log records, obfuscating PII fields"""
        log = super().format(record).replace(';', '; ')
        return filter_datum(self.fields, self.REDACTION, log, self.SEPARATOR)
