from datetime import datetime
from constants import DATE_FORMAT, DATETIME_FORMAT

from validators import (
    is_valid_airport_code,
    is_valid_flight_number,
)

def prompt_for_selection(prompt, rows, display_function):
    display_function(rows)
    if not rows:
        return None

    while True:
        choice = input(f"{prompt}: ").strip()

        try:
            selected_id = int(choice)
        except ValueError:
            print("Please enter a valid number.")
            continue

        for row in rows:
            if row[0] == selected_id:
                return row

        print("Invalid selection. Please try again.")


def prompt_for_value_from_list(prompt, values):
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


def prompt_for_code_selection(prompt, rows, display_function):
    display_function(rows)
    if not rows:
        return None

    while True:
        choice = input(f"{prompt}: ").strip().upper()

        for row in rows:
            if row[0] == choice:
                return row

        print("Invalid selection. Please try again.")


def prompt_for_optional_code_selection(prompt, rows, display_function):
    print("ANY - Any destination")
    display_function(rows)
    
    if not rows:
        return None
    
    while True:

        choice = input(f"{prompt}: ").strip().upper()

        if choice == "ANY":
            return None

        for row in rows:
            if row[0] == choice:
                return row

        print("Invalid selection. Please try again.")


def prompt_for_menu_selection(options):
    while True:
        print("\nFlight Management System\n")

        for index, (description, _) in enumerate(options, start=1):
            print(f"{index}. {description}")

        print(f"{len(options) + 1}. Exit")
        print()

        choice = input("Choose an option: ").strip()

        try:
            selected_index = int(choice) - 1

            if selected_index == len(options):
                return None

            if selected_index < 0 or selected_index >= len(options):
                raise IndexError

            return options[selected_index][1]

        except (ValueError, IndexError):
            print("Invalid option. Please choose again.")


def prompt_for_required_text(prompt):
    while True:
        value = input(f"{prompt}: ").strip()

        if value:
            return value

        print("This field is required.")


def prompt_for_datetime(prompt):
    while True:
        value = input(f"{prompt} YYYY-MM-DD HH:MM: ").strip()

        try:
            datetime.strptime(value, DATETIME_FORMAT)
            return value
        except ValueError:
            print("Invalid date/time format. Please use YYYY-MM-DD HH:MM.")


def prompt_for_optional_date(prompt):
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
    while True:
        value = input(f"{prompt}: ").strip().upper()

        if is_valid_airport_code(value):
            return value

        print("Airport code must be exactly 3 letters.")


def prompt_for_flight_number(prompt):
    while True:
        value = input(f"{prompt}: ").strip().upper()

        if is_valid_flight_number(value):
            return value

        print(
            "Flight number must start with "
            "'UOB' followed by digits."
        )