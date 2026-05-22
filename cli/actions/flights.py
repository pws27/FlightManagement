"""
CLI actions related to flight management.

This module coordinates user input, repository queries,
and display functions for creating, searching, updating,
and deleting flights.
"""

from application.exceptions.flight_number_already_exists import (
    FlightNumberAlreadyExists,
)

from application.flights import (
    assign_pilot_to_existing_flight,
    change_flight_departure_datetime,
    change_flight_status,
    create_flight,
    ensure_flight_number_is_available,
    list_flights,
    list_flights_for_selection,
    remove_flight,
    search_flights,
)

from cli.display import (
    display_destination_codes, 
    display_flight_selection, 
    display_flights, 
    display_pilots,
)

from cli.prompts import (
    prompt_for_code_selection, 
    prompt_for_datetime, 
    prompt_for_flight_number, 
    prompt_for_menu_selection,
    prompt_for_optional_code_selection, 
    prompt_for_optional_date, 
    prompt_for_selection, 
    prompt_for_value_from_list,
)

from constants import FLIGHT_STATUSES

from application.destinations import list_destinations_for_selection

from application.pilots import list_pilots


def view_all_flights_action(connection):
    flights = list_flights(connection)
    display_flights(flights)


def search_flights_action(connection):
    destination = prompt_for_optional_code_selection(
        "Choose destination airport code",
        list_destinations_for_selection(connection),
        display_destination_codes,
    )

    destination_id = destination[3] if destination else None

    status = prompt_for_value_from_list(
        "Choose status filter",
        ["Any"] + FLIGHT_STATUSES,
    )

    departure_date = prompt_for_optional_date(
        "Departure date YYYY-MM-DD, leave blank to ignore"
    )

    flights = search_flights(
        connection,
        destination_id=destination_id,
        status=status,
        departure_date=departure_date,
    )

    display_flights(flights)


def add_flight_action(connection):
    print("\nAdd New Flight\n")

    flight_number = prompt_for_flight_number("Flight number")

    try:
        ensure_flight_number_is_available(connection, flight_number)
    except FlightNumberAlreadyExists:
        print("That flight number already exists.")
        return

    destination = prompt_for_code_selection(
        "Choose destination airport code",
        list_destinations_for_selection(connection),
        display_destination_codes,
    )

    if destination is None:
        return

    destination_id = destination[3]

    departure_datetime = prompt_for_datetime("Departure datetime")

    status = prompt_for_value_from_list(
        "Choose flight status",
        FLIGHT_STATUSES,
    )

    pilot_id = None

    assign_pilot = prompt_for_value_from_list(
        "Assign a pilot now?",
        ["Yes", "No"],
    )

    if assign_pilot == "Yes":
        pilot = prompt_for_selection(
            "Choose pilot ID",
            list_pilots(connection),
            display_pilots,
        )

        if pilot is None:
            return

        pilot_id = pilot[0]

    try:
        create_flight(
            connection,
            flight_number=flight_number,
            destination_id=destination_id,
            departure_datetime=departure_datetime,
            status=status,
            pilot_id=pilot_id,
        )

        print("Flight added successfully.")

    except FlightNumberAlreadyExists:
        print("That flight number already exists.")

    except Exception as error:
        connection.rollback()
        print(f"Could not add flight: {error}")


def update_flight_information_action(connection):
    flight = prompt_for_selection(
        "Choose flight ID",
        list_flights_for_selection(connection),
        display_flight_selection,
    )

    if flight is None:
        return

    flight_id = flight[0]

    update_type = prompt_for_value_from_list(
        "Choose update type",
        [
            "Status",
            "Departure datetime",
        ],
    )

    try:
        if update_type == "Status":
            status = prompt_for_value_from_list(
                "Choose new flight status",
                FLIGHT_STATUSES,
            )

            success = change_flight_status(connection, flight_id, status)

        else:
            departure_datetime = prompt_for_datetime(
                "New departure datetime"
            )

            success = change_flight_departure_datetime(
                connection,
                flight_id,
                departure_datetime,
            )

        if success:
            print("Flight updated successfully.")
        else:
            print("Flight could not be found.")

    except Exception as error:
        connection.rollback()
        print(f"Could not update flight: {error}")


def delete_flight_action(connection):
    flight = prompt_for_selection(
        "Choose flight ID to delete",
        list_flights_for_selection(connection),
        display_flight_selection,
    )

    if flight is None:
        return

    flight_id = flight[0]

    confirm = prompt_for_value_from_list(
        "Are you sure you want to delete this flight?",
        ["No", "Yes"],
    )

    if confirm == "No":
        print("Delete cancelled.")
        return

    try:
        success = remove_flight(connection, flight_id)

        if success:
            print("Flight deleted successfully.")
        else:
            print("Flight could not be found.")

    except Exception as error:
        connection.rollback()
        print(f"Could not delete flight: {error}")

def flights_menu_action(connection):
    action = prompt_for_menu_selection(FLIGHT_GROUPS)

    if action is None:
        return

    action(connection)


def assign_pilot_to_flight_action(connection):
    flight = prompt_for_selection(
        "Choose flight ID",
        list_flights_for_selection(connection),
        display_flight_selection,
    )

    if flight is None:
        return

    flight_id = flight[0]

    pilot = prompt_for_selection(
        "Choose pilot ID",
        list_pilots(connection),
        display_pilots,
    )

    if pilot is None:
        return

    pilot_id = pilot[0]

    try:
        success = assign_pilot_to_existing_flight(
            connection,
            flight_id,
            pilot_id,
        )

        if success:
            print("Pilot assigned successfully.")
        else:
            print("Flight could not be found.")

    except Exception as error:
        connection.rollback()
        print(f"Could not assign pilot: {error}")

FLIGHT_GROUPS = [
    (
        "Flights",
        [
            ("List", view_all_flights_action),
            ("Search", search_flights_action),
            ("Add", add_flight_action),
            ("Update", update_flight_information_action),
            ("Assign pilot", assign_pilot_to_flight_action),
            ("Delete", delete_flight_action),
        ],
    ),
]