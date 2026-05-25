"""
Application-layer flight use cases.

This module coordinates flight-related business operations
including creation, searching, status updates, scheduling,
pilot assignment, and deletion.

Business rules such as duplicate flight number validation
are enforced here before repository operations are executed.
"""

from datetime import datetime, timedelta

from application.exceptions.flight_number_already_exists import (
    FlightNumberAlreadyExists,
)

from application.exceptions.pilot_already_assigned_on_date import (
    PilotAlreadyAssignedOnDate,
)

from constants import DATE_FORMAT, DATETIME_FORMAT

from repositories.flights import (
    add_flight,
    assign_pilot_to_flight,
    delete_flight,
    flight_number_exists,
    get_all_flight_details,
    get_all_flights_for_selection,
    get_flight_departure_datetime,
    find_flights,
    pilot_has_flight_on_departure_date,
    unassign_pilot_from_flight,
    update_flight_departure_datetime,
    update_flight_status,
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

    ensure_pilot_is_available_for_flight_date(
        connection,
        pilot_id,
        departure_datetime,
    )

    return add_flight(
        connection,
        flight_number,
        destination_id,
        departure_datetime,
        status,
        pilot_id,
    )


def search_flights(
    connection,
    destination_id=None,
    status=None,
    departure_date=None,
):
    if status == "Any":
        status = None

    departure_start = None
    departure_end = None

    if departure_date:
        departure_start, departure_end = get_departure_datetime_range(departure_date)

    return find_flights(
        connection,
        destination_id,
        status,
        departure_start,
        departure_end,
    )


def list_flights(connection):
    return get_all_flight_details(connection)


def list_flights_for_selection(connection):
    return get_all_flights_for_selection(connection)


def change_flight_status(connection, flight_id, status):
    return update_flight_status(connection, flight_id, status) == 1


def change_flight_departure_datetime(connection, flight_id, departure_datetime):
    return (
        update_flight_departure_datetime(connection, flight_id, departure_datetime) == 1
    )


def remove_flight(connection, flight_id):
    return delete_flight(connection, flight_id) == 1


def assign_pilot_to_existing_flight(connection, flight_id, pilot_id):
    departure_datetime = get_flight_departure_datetime(connection, flight_id)

    if departure_datetime is None:
        return False

    ensure_pilot_is_available_for_flight_date(
        connection,
        pilot_id,
        departure_datetime,
        exclude_flight_id=flight_id,
    )

    return assign_pilot_to_flight(connection, flight_id, pilot_id) == 1


def unassign_pilot_from_existing_flight(connection, flight_id):
    return unassign_pilot_from_flight(connection, flight_id) == 1


def ensure_flight_number_is_available(connection, flight_number):
    if flight_number_exists(connection, flight_number):
        raise FlightNumberAlreadyExists()


def get_departure_datetime_range(departure_date):
    start = datetime.strptime(departure_date, DATE_FORMAT)
    end = start + timedelta(days=1)

    return (
        start.strftime(DATETIME_FORMAT),
        end.strftime(DATETIME_FORMAT),
    )


def ensure_pilot_is_available_for_flight_date(
    connection,
    pilot_id,
    departure_datetime,
    exclude_flight_id=None,
):
    """
    Raises an exception if the pilot is already assigned to another
    flight on the same departure date.
    """

    if pilot_id is None:
        return

    if pilot_has_flight_on_departure_date(
        connection,
        pilot_id,
        departure_datetime,
        exclude_flight_id,
    ):
        raise PilotAlreadyAssignedOnDate()
