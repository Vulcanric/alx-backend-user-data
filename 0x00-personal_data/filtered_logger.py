#!/usr/bin/env python3
""" Defines a function filter_datum that returns log message obfuscated
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    for field in fields:
        target_substr, obfuscated = f'{field}=\S+?{separator}',f'{field}={redaction}{separator}'
        message = re.sub(target_substr, obfuscated, message)
    return message
