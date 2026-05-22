"""
Unit tests for reusable CLI prompt functions.

These tests verify menu selection, user input handling,
validation retries, and date parsing behaviour.
"""

import unittest
from unittest.mock import patch

from cli.prompts import (
    prompt_for_airport_code,
    prompt_for_flight_number,
    prompt_for_required_text,
    prompt_for_optional_date,
    prompt_for_value_from_list,
    prompt_for_datetime,
    prompt_for_menu_selection,
    prompt_for_selection,
    prompt_for_code_selection,
)

class TestPrompts(unittest.TestCase):

    @patch("builtins.input", return_value="lhr")
    def test_prompt_for_airport_code_converts_to_uppercase(self, mock_input):
        airport_code = prompt_for_airport_code("Airport code")

        self.assertEqual(airport_code, "LHR")


    @patch("builtins.input", side_effect=["LH", "LHR"])
    def test_prompt_for_airport_code_retries_until_valid(self, mock_input):
        airport_code = prompt_for_airport_code("Airport code")

        self.assertEqual(airport_code, "LHR")
        self.assertEqual(mock_input.call_count, 2)


    @patch("builtins.input", return_value="uob123")
    def test_prompt_for_flight_number_converts_to_uppercase(self, mock_input):
        flight_number = prompt_for_flight_number("Flight number")

        self.assertEqual(flight_number, "UOB123")


    @patch("builtins.input", side_effect=["BA123", "UOB123"])
    def test_prompt_for_flight_number_retries_until_valid(self, mock_input):
        flight_number = prompt_for_flight_number("Flight number")

        self.assertEqual(flight_number, "UOB123")
        self.assertEqual(mock_input.call_count, 2)


    @patch("builtins.input", side_effect=["", "London"])
    def test_prompt_for_required_text_retries_until_not_blank(self, mock_input):
        value = prompt_for_required_text("City")

        self.assertEqual(value, "London")
        self.assertEqual(mock_input.call_count, 2)


    @patch("builtins.input", return_value="")
    def test_prompt_for_optional_date_allows_blank(self, mock_input):
        value = prompt_for_optional_date("Departure date")

        self.assertIsNone(value)


    @patch("builtins.input", side_effect=["2026/06/01", "2026-06-01"])
    def test_prompt_for_optional_date_retries_until_valid_date(self, mock_input):
        value = prompt_for_optional_date("Departure date")

        self.assertEqual(value, "2026-06-01")
        self.assertEqual(mock_input.call_count, 2)


    @patch("builtins.input", side_effect=["9", "2"])
    def test_prompt_for_value_from_list_retries_until_valid_choice(self, mock_input):
        value = prompt_for_value_from_list(
            "Choose status",
            ["Scheduled", "Delayed", "Cancelled"],
        )

        self.assertEqual(value, "Delayed")
        self.assertEqual(mock_input.call_count, 2)

    
    @patch("builtins.input", return_value="2026-06-01 10:30")
    def test_prompt_for_datetime_accepts_valid_datetime(self, mock_input):
        value = prompt_for_datetime("Departure datetime")

        self.assertEqual(value, "2026-06-01 10:30")


    @patch("builtins.input", side_effect=["2026/06/01 10:30", "2026-06-01 10:30"])
    def test_prompt_for_datetime_retries_until_valid(self, mock_input):
        value = prompt_for_datetime("Departure datetime")

        self.assertEqual(value, "2026-06-01 10:30")
        self.assertEqual(mock_input.call_count, 2)


    @patch("builtins.input", return_value="2")
    def test_prompt_for_menu_selection_returns_selected_action(self, mock_input):
        def first_action(connection):
            pass

        def second_action(connection):
            pass

        action = prompt_for_menu_selection([
            (
                "Test group",
                [
                    ("First", first_action),
                    ("Second", second_action),
                ],
            ),
        ])

        self.assertEqual(action, second_action)


    @patch("builtins.input", return_value="3")
    def test_prompt_for_menu_selection_returns_none_for_exit(self, mock_input):
        def first_action(connection):
            pass

        def second_action(connection):
            pass

        action = prompt_for_menu_selection([
            (
                "Test group",
                [
                    ("First", first_action),
                    ("Second", second_action),
                ],
            ),
        ])

        self.assertIsNone(action)


    @patch("builtins.input", return_value="2")
    def test_prompt_for_selection_returns_matching_option(self, mock_input):
        options = [
            (1, "Peter", "Somerville"),
            (2, "Julie", "Amphlett"),
        ]

        selected = prompt_for_selection(
            "Choose pilot ID",
            options,
            lambda options: None,
        )

        self.assertEqual(selected, (2, "Julie", "Amphlett"))


    def test_prompt_for_selection_returns_none_when_no_options(self):
        selected = prompt_for_selection(
            "Choose pilot ID",
            [],
            lambda options: None,
        )

        self.assertIsNone(selected)


    @patch("builtins.input", return_value="lhr")
    def test_prompt_for_code_selection_returns_matching_option_case_insensitive(self, mock_input):
        options = [
            ("LHR", "London", "United Kingdom", 1),
            ("JFK", "New York", "United States", 2),
        ]

        selected = prompt_for_code_selection(
            "Choose destination airport code",
            options,
            lambda options: None,
        )

        self.assertEqual(selected, ("LHR", "London", "United Kingdom", 1))

if __name__ == "__main__":
    unittest.main()
