from repositories import (
    add_flight,
    count_flights_by_destination,
    count_flights_by_pilot,
    get_all_destinations_by_airport_code,
    get_all_pilots,
    get_flights_by_criteria,
    get_all_flight_details,
    get_flights_by_pilot_id,
    update_flight_departure_datetime,
    get_all_flights_for_selection,
    update_flight_status,
    delete_flight,
    assign_pilot_to_flight,
    update_destination_airport_code,
    update_destination_city,
    update_destination_country,
    add_destination,
    airport_code_exists_for_other_destination,
)

from constants import FLIGHT_STATUSES

from cli.display import (
    display_destination_codes,
    display_flight_counts_by_destination,
    display_flight_counts_by_pilot,
    display_flights,
    display_pilots,
    display_flight_selection,
)

from cli.prompts import (
    prompt_for_code_selection,
    prompt_for_optional_code_selection,
    prompt_for_selection,
    prompt_for_value_from_list,
    prompt_for_required_text,
    prompt_for_datetime,
    prompt_for_optional_date,
    prompt_for_airport_code,
    prompt_for_flight_number,
)


def view_all_flights_action(connection):
    rows = get_all_flight_details(connection)
    display_flights(rows)


def search_flights_action(connection):
    destination = prompt_for_optional_code_selection(
        "Choose destination airport code",
        get_all_destinations_by_airport_code(connection),
        display_destination_codes,
    )

    destination_id = destination[3] if destination else None

    status = prompt_for_value_from_list(
        "Choose status filter",
        ["Any"] + FLIGHT_STATUSES,
    )

    if status == "Any":
        status = None

    departure_date = prompt_for_optional_date(
        "Departure date YYYY-MM-DD, leave blank to ignore"
    )

    rows = get_flights_by_criteria(
        connection,
        destination_id=destination_id,
        status=status,
        departure_date=departure_date or None,
    )

    display_flights(rows)


def count_destinations_action(connection):
    rows = count_flights_by_destination(connection)
    display_flight_counts_by_destination(rows)


def count_pilots_action(connection):
    rows = count_flights_by_pilot(connection)
    display_flight_counts_by_pilot(rows)


def add_flight_action(connection):
    print("\nAdd New Flight\n")

    flight_number = prompt_for_flight_number("Flight number")

    destination = prompt_for_code_selection(
        "Choose destination airport code",
        get_all_destinations_by_airport_code(connection),
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
            get_all_pilots(connection),
            display_pilots,
        )

        if pilot is None:
            return

        pilot_id = pilot[0]

    try:
        add_flight(
            connection,
            flight_number=flight_number,
            destination_id=destination_id,
            departure_datetime=departure_datetime,
            status=status,
            pilot_id=pilot_id,
        )

        print("Flight added successfully.")

    except Exception as error:
        connection.rollback()
        print(f"Could not add flight: {error}")


def view_pilot_schedule_action(connection):
    pilot = prompt_for_selection(
        "Choose pilot ID",
        get_all_pilots(connection),
        display_pilots,
    )

    if pilot is None:
        return

    pilot_id = pilot[0]

    rows = get_flights_by_pilot_id(connection, pilot_id)

    display_flights(rows)

def update_flight_information_action(connection):
    flight = prompt_for_selection(
        "Choose flight ID",
        get_all_flights_for_selection(connection),
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

            updated_rows = update_flight_status(
                connection,
                flight_id,
                status,
            )

        else:
            departure_datetime = prompt_for_datetime(
                "New departure datetime"
            )

            updated_rows = update_flight_departure_datetime(
                connection,
                flight_id,
                departure_datetime,
            )

        if updated_rows == 1:
            print("Flight updated successfully.")
        else:
            print("Flight could not be found.")

    except Exception as error:
        connection.rollback()
        print(f"Could not update flight: {error}")


def delete_flight_action(connection):
    flight = prompt_for_selection(
        "Choose flight ID to delete",
        get_all_flights_for_selection(connection),
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
        deleted_rows = delete_flight(connection, flight_id)

        if deleted_rows == 1:
            print("Flight deleted successfully.")
        else:
            print("Flight could not be found.")

    except Exception as error:
        connection.rollback()
        print(f"Could not delete flight: {error}")


def assign_pilot_to_flight_action(connection):
    flight = prompt_for_selection(
        "Choose flight ID",
        get_all_flights_for_selection(connection),
        display_flight_selection,
    )

    if flight is None:
        return

    flight_id = flight[0]

    pilot = prompt_for_selection(
        "Choose pilot ID",
        get_all_pilots(connection),
        display_pilots,
    )

    if pilot is None:
        return

    pilot_id = pilot[0]

    try:
        updated_rows = assign_pilot_to_flight(
            connection,
            flight_id,
            pilot_id,
        )

        if updated_rows == 1:
            print("Pilot assigned successfully.")
        else:
            print("Flight could not be found.")

    except Exception as error:
        connection.rollback()
        print(f"Could not assign pilot: {error}")


def update_destination_action(connection):
    try:
        destination = prompt_for_code_selection(
            "Choose destination airport code",
            get_all_destinations_by_airport_code(connection),
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
            if airport_code_exists_for_other_destination(
                connection,
                new_value,
                destination_id,
            ):
                print("That airport code already exists.")
                return
        else:
            new_value = prompt_for_required_text(f"New {update_type.lower()}")

        if update_type == "Airport code":
            updated_rows = update_destination_airport_code(
                connection,
                destination_id,
                new_value,
            )
        elif update_type == "City":
            updated_rows = update_destination_city(
                connection,
                destination_id,
                new_value,
            )
        else:
            updated_rows = update_destination_country(
                connection,
                destination_id,
                new_value,
            )

        if updated_rows == 1:
            print("Destination updated successfully.")
        else:
            print("Destination could not be found.")

    except Exception as error:
        connection.rollback()
        print(f"Could not update destination: {error}")


def add_destination_action(connection):
    print("\nAdd New Destination\n")

    airport_code = prompt_for_airport_code('Airport code')
    city = prompt_for_required_text("City")
    country = prompt_for_required_text("Country")

    try:
        add_destination(
            connection,
            airport_code,
            city,
            country,
        )

        print("Destination added successfully.")

    except Exception as error:
        connection.rollback()
        print(f"Could not add destination: {error}")