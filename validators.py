def is_valid_airport_code(value):
    return len(value) == 3 and value.isalpha() and value.isupper()


def is_valid_flight_number(value):
    if not value.startswith("UOB"):
        return False

    suffix = value[3:]

    return suffix.isdigit() and len(suffix) > 0
