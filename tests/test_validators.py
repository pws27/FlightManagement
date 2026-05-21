import unittest

from validators import (
    is_valid_airport_code,
    is_valid_flight_number,
)


class TestValidators(unittest.TestCase):

    def test_valid_airport_code(self):
        self.assertTrue(is_valid_airport_code("LHR"))

    def test_airport_code_must_be_three_letters(self):
        self.assertFalse(is_valid_airport_code("LH"))
        self.assertFalse(is_valid_airport_code("LHRR"))

    def test_airport_code_must_not_contain_digits(self):
        self.assertFalse(is_valid_airport_code("LH1"))
    
    def test_airport_code_must_be_upper_case(self):
        self.assertFalse(is_valid_airport_code('lhr'))

    def test_valid_flight_number(self):
        self.assertTrue(is_valid_flight_number("UOB123"))

    def test_flight_number_must_start_with_uob(self):
        self.assertFalse(is_valid_flight_number("BA123"))

    def test_flight_number_must_end_with_digits(self):
        self.assertFalse(is_valid_flight_number("UOBABC"))

    def test_flight_number_must_have_digits_after_prefix(self):
        self.assertFalse(is_valid_flight_number("UOB"))


if __name__ == "__main__":
    unittest.main()
