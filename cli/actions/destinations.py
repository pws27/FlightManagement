"""
CLI actions related to destination management.

This module handles user interaction for destination creation,
updates, and listing. Business operations are delegated to the
application layer.
"""

from application.destinations import (
    change_destination_airport_code,
    change_destination_city,
    change_destination_country,
    create_destination,
    ensure_airport_code_is_available,
    list_destinations_for_selection,
    list_destinations,
)

from application.exceptions.airport_code_already_exists import (
    AirportCodeAlreadyExists,
)

from cli.display import display_destination_codes

from cli.prompts import (
    prompt_for_airport_code,
    prompt_for_code_selection,
    prompt_for_required_text,
    prompt_for_value_from_list,
    prompt_for_menu_selection,
)

from cli.screen import clear_screen


def update_destination_action(connection):
    try:
        destination = prompt_for_code_selection(
            "Choose destination airport code",
            list_destinations_for_selection(connection),
            display_destination_codes,
        )

        if destination is None:
            return

        destination_id = destination[3]

        update_type = prompt_for_value_from_list(
            "Choose field to update",
            [
                "Airport code",
                "City",
                "Country",
            ],
        )

        if update_type == "Airport code":
            new_value = prompt_for_airport_code("New airport code")
        else:
            new_value = prompt_for_required_text(f"New {update_type.lower()}")

        if update_type == "Airport code":
            success = change_destination_airport_code(
                connection,
                destination_id,
                new_value,
            )
        elif update_type == "City":
            success = change_destination_city(
                connection,
                destination_id,
                new_value,
            )
        else:
            success = change_destination_country(
                connection,
                destination_id,
                new_value,
            )

        if success:
            print("Destination updated successfully.")
        else:
            print("Destination could not be found.")

    except AirportCodeAlreadyExists:
        print("That airport code already exists.")

    except Exception as error:
        print(f"Could not update destination: {error}")


def view_destinations_action(connection):
    destinations = list_destinations(connection)
    display_destination_codes(destinations)


def add_destination_action(connection):
    print("\nAdd New Destination\n")

    airport_code = prompt_for_airport_code("Airport code")

    try:
        # Fail fast before collecting the rest of the destination details.
        # create_destination also validates this so non-CLI callers are protected.
        ensure_airport_code_is_available(connection, airport_code)
    except AirportCodeAlreadyExists:
        print("That airport code already exists.")
        return

    city = prompt_for_required_text("City")
    country = prompt_for_required_text("Country")

    try:
        create_destination(
            connection,
            airport_code,
            city,
            country,
        )

        print("Destination added successfully.")

    except AirportCodeAlreadyExists:
        print("That airport code already exists.")

    except Exception as error:
        print(f"Could not add destination: {error}")


def destinations_menu_action(connection):

    clear_screen()

    action = prompt_for_menu_selection(DESTINATION_GROUPS)

    if action is None:
        return

    clear_screen()

    action(connection)


DESTINATION_GROUPS = [
    (
        "Destinations",
        [
            ("List", view_destinations_action),
            ("Add", add_destination_action),
            ("Update", update_destination_action),
        ],
    ),
]
