import re
import random
import functools
from typing import Any, Optional


def get_nested_object(o: dict, path: list) -> Optional[Any]:
    """Takes in a dictionary object and a list representing a nested path,
    and returns the value at the nested path if it exists within the object.
    Otherwise, returns None."""
    return functools.reduce(lambda xs, x: xs[x] if xs else None, path, o)


def extract_value(string: str, pattern: str) -> Optional[str]:
    """Takes in a string and a pattern to search for within the string.
    If the pattern exists within the string, returns the value associated
    with it. Otherwise, returns None."""
    match = re.search(f'"{pattern}":".*?"', string)
    if match:
        return match.group(0).replace(f'"{pattern}":"', "")[:-1]
    return None


def generate_request_id():
    """Generate a random request ID"""
    return 1000 + int(random.randint(1, 100) * 9000)
