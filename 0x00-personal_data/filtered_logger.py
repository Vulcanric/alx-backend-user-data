#!/usr/bin/env python3
""" Defines a function filter_datum that returns log message obfuscated
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """ Filters a log message, obfuscating PII fields """
    for field in fields:
        message = re.sub(f'{field}=\S+?{separator}', f'{field}={redaction}{separator}', message)
    return message
