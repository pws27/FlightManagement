"""
Validation functions for application business rules.

This module validates user input such as airport codes
and flight numbers before database operations are performed.
"""


def is_valid_airport_code(value: str) -> bool:
    return len(value) == 3 and value.isalpha() and value.isupper()


def is_valid_flight_number(value: str) -> bool:
    if not value.startswith("UOB"):
        return False

    suffix = value[3:]

    return suffix.isdigit() and len(suffix) > 0
