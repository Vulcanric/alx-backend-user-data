#!/usr/bin/env python3
""" Defines a function filter_datum that returns log message obfuscated
"""
import re
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

        fields <list>:
            List of strings representing all fields to obfuscate.

        redaction <str>:
            String representing by what the field will be obfu-
scated.
        message <str>:
            String representing the log line

        separator <str>:
            String representing by which character is separati-
ng all fields.

    Example
    ________

    >>> fields = ["password", "date_of_birth"]
    >>> message = "name=matthew;email=mathew@example.com;password=mattpass;date_of_birth=12/3/2005;"
    >>> filter_datum(fields, 'xxx', message, ';')
    name=matthew;email=matthew@example.com;password=xxx;date_of_birth=xxx;
    """
    for field in fields:
        target_substr, obfuscated = f'{field}=\S+?{separator}', f'{field}={redaction}{separator}'
        message = re.sub(target_substr, obfuscated, message)
    return message
