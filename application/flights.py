from application.exceptions.flight_number_already_exists import (
    FlightNumberAlreadyExists,
)

from repositories.flights import (
    add_flight,
    assign_pilot_to_flight,
    delete_flight,
    flight_number_exists,
    get_all_flight_details,
    get_all_flights_for_selection,
    get_flights_by_criteria,
    update_flight_status,
    update_flight_departure_datetime,
)

def create_flight(
    connection,
    flight_number,
    destination_id,
    departure_datetime,
    status,
    pilot_id=None,
):
    ensure_flight_number_is_available(connection, flight_number)

    return add_flight(
        connection,
        flight_number=flight_number,
        destination_id=destination_id,
        departure_datetime=departure_datetime,
        status=status,
        pilot_id=pilot_id,
    )

def search_flights(
    connection,
    destination_id=None,
    status=None,
    departure_date=None,
):
    if status == "Any":
        status = None

    return get_flights_by_criteria(
        connection,
        destination_id=destination_id,
        status=status,
        departure_date=departure_date or None,
    )


def list_flights(connection):
    return get_all_flight_details(connection)


def list_flights_for_selection(connection):
    return get_all_flights_for_selection(connection)


def change_flight_status(connection, flight_id, status):
    return update_flight_status(connection, flight_id, status) == 1


def change_flight_departure_datetime(connection, flight_id, departure_datetime):
    return update_flight_departure_datetime(connection, flight_id, departure_datetime) == 1


def remove_flight(connection, flight_id):
    return delete_flight(connection, flight_id) == 1


def assign_pilot_to_existing_flight(connection, flight_id, pilot_id):
    return assign_pilot_to_flight(connection, flight_id, pilot_id) == 1


def ensure_flight_number_is_available(connection, flight_number):
    if flight_number_exists(connection, flight_number):
        raise FlightNumberAlreadyExists()