from repositories import (
    add_flight,
    count_flights_by_destination,
    count_flights_by_pilot,
    get_all_destinations_by_airport_code,
    get_all_pilots,
    get_flights_by_criteria,
    view_all_flights,
    get_flights_by_pilot_id,
)

from cli.display import (
    display_destination_codes,
    display_flight_counts_by_destination,
    display_flight_counts_by_pilot,
    display_flights,
    display_pilots,
)

from cli.prompts import (
    prompt_for_code_selection,
    prompt_for_optional_code_selection,
    prompt_for_selection,
    prompt_for_value_from_list,
    prompt_for_required_text,
    prompt_for_datetime,
    prompt_for_optional_date,
)

FLIGHT_STATUSES = [
    "Scheduled",
    "Delayed",
    "Cancelled",
    "Boarding",
    "Departed",
]


def view_all_flights_action(connection):
    rows = view_all_flights(connection)
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

    departure_date = prompt_for_optional_date("Departure date YYYY-MM-DD, leave blank to ignore")

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

    flight_number = prompt_for_required_text("Flight number")

    destination = prompt_for_code_selection(
        "Choose destination airport code",
        get_all_destinations_by_airport_code(connection),
        display_destination_codes,
    )

    destination_id = destination[3]

    departure_datetime = prompt_for_datetime("Departure datetime ")

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
        print(f"Could not add flight: {error}")


def view_pilot_schedule_action(connection):
    pilot = prompt_for_selection(
        "Choose pilot ID",
        get_all_pilots(connection),
        display_pilots,
    )

    pilot_id = pilot[0]

    rows = get_flights_by_pilot_id(connection, pilot_id)

    display_flights(rows)