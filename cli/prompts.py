"""
Reusable CLI input prompts and validation loops.

This module handles menu navigation, user selections,
date parsing, and validation of business rules such as
airport codes and flight numbers.
"""

from datetime import datetime
from constants import DATE_FORMAT, DATETIME_FORMAT

from validators import (
    is_valid_airport_code,
    is_valid_flight_number,
)


def prompt_for_selection(prompt, options, display_function):
    display_function(options)
    if not options:
        return None

    while True:
        choice = input(f"{prompt}: ").strip()

        try:
            selected_id = int(choice)
        except ValueError:
            print("Please enter a valid number.")
            continue

        for option in options:
            if option[0] == selected_id:
                return option

        print("Invalid selection. Please try again.")


def prompt_for_value_from_list(prompt, values):
    """
    Prompts the user to choose a value from a numbered list.
    """

    while True:
        print()

        for index, value in enumerate(values, start=1):
            print(f"{index}. {value}")

        choice = input(f"{prompt}: ").strip()

        try:
            selected_index = int(choice) - 1

            if selected_index < 0 or selected_index >= len(values):
                raise IndexError

            return values[selected_index]

        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")


def prompt_for_code_selection(prompt, options, display_function):
    display_function(options)
    if not options:
        return None

    while True:
        choice = input(f"{prompt}: ").strip().upper()

        for option in options:
            if option[0] == choice:
                return option

        print("Invalid selection. Please try again.")


def prompt_for_optional_code_selection(prompt, options, display_function):
    """
    Prompts the user to select an airport code or choose ANY
    to disable destination filtering.
    """

    print("ANY - Any destination")
    display_function(options)

    if not options:
        return None

    while True:

        choice = input(f"{prompt}: ").strip().upper()

        if choice == "ANY":
            return None

        for option in options:
            if option[0] == choice:
                return option

        print("Invalid selection. Please try again.")


def prompt_for_menu_selection(groups):
    """
    Displays a grouped CLI menu and returns
    the selected action.
    """

    while True:
        numbered_options = [
            (description, action)
            for _, options in groups
            for description, action in options
        ]

        number_width = len(str(len(numbered_options) + 1))

        print("\nFlight Management System\n")

        current_number = 1

        for title, options in groups:
            print(title)

            for description, action in options:
                print(f"{current_number:>{number_width}}. {description}")
                current_number += 1

            print()

        print(f"{len(numbered_options) + 1:>{number_width}}. Exit")
        print()

        choice = input("Choose an option: ").strip()

        try:
            selected_index = int(choice) - 1
        except ValueError:
            print("Invalid option. Please choose again.")
            continue

        if selected_index == len(numbered_options):
            return None

        if selected_index < 0 or selected_index >= len(numbered_options):
            print("Invalid option. Please choose again.")
            continue

        return numbered_options[selected_index][1]


def prompt_for_required_text(prompt):
    while True:
        value = input(f"{prompt}: ").strip()

        if value:
            return value

        print("This field is required.")


def prompt_for_datetime(prompt):
    """
    Prompts the user for a date and time in
    YYYY-MM-DD HH:MM format.
    """

    while True:
        value = input(f"{prompt} YYYY-MM-DD HH:MM: ").strip()

        try:
            datetime.strptime(value, DATETIME_FORMAT)
            return value
        except ValueError:
            print("Invalid date/time format. Please use YYYY-MM-DD HH:MM.")


def prompt_for_optional_date(prompt):
    """
    Prompts the user for an optional date filter in YYYY-MM-DD format.
    Blank input disables date filtering.
    """

    while True:
        value = input(f"{prompt}: ").strip()

        if not value:
            return None

        try:
            datetime.strptime(value, DATE_FORMAT)
            return value
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def prompt_for_airport_code(prompt):
    """
    Prompts the user for a valid three-letter
    airport code.
    """
    while True:
        value = input(f"{prompt}: ").strip().upper()

        if is_valid_airport_code(value):
            return value

        print("Airport code must be exactly 3 letters.")


def prompt_for_flight_number(prompt):
    """
    Prompts the user for a valid flight number
    beginning with the UOB prefix.
    """
    while True:
        value = input(f"{prompt}: ").strip().upper()

        if is_valid_flight_number(value):
            return value

        print("Flight number must start with 'UOB' followed by digits.")


def pause():
    """
    Pauses CLI execution until the user presses Enter.
    """
    input("\nPress Enter to continue...")
