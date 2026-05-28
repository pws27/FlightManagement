"""
Application-layer destination use cases.

This module coordinates destination-related business
operations such as creation, updates, validation checks,
and retrieval for presentation layers.

The application layer separates business intent from
CLI interaction and database persistence concerns.
"""

from application.exceptions.airport_code_already_exists import (
    AirportCodeAlreadyExists,
)

from repositories.destinations import (
    add_destination,
    airport_code_exists,
    get_all_destinations,
    get_all_destinations_by_airport_code,
    update_destination_airport_code,
    update_destination_city,
    update_destination_country,
)


def ensure_airport_code_is_available(
    connection,
    airport_code,
    exclude_destination_id=None,
):
    if airport_code_exists(
        connection,
        airport_code,
        exclude_destination_id,
    ):
        raise AirportCodeAlreadyExists()


def create_destination(connection, airport_code, city, country):
    try:
        ensure_airport_code_is_available(connection, airport_code)

        destination_id = add_destination(connection, airport_code, city, country)

        connection.commit()

        return destination_id

    except Exception:
        connection.rollback()
        raise


def change_destination_airport_code(connection, destination_id, airport_code):
    try:
        ensure_airport_code_is_available(
            connection,
            airport_code,
            exclude_destination_id=destination_id,
        )

        success = (
            update_destination_airport_code(
                connection,
                destination_id,
                airport_code,
            )
            == 1
        )

        connection.commit()

        return success

    except Exception:
        connection.rollback()
        raise


def change_destination_city(connection, destination_id, city):
    try:
        success = update_destination_city(connection, destination_id, city) == 1

        connection.commit()

        return success

    except Exception:
        connection.rollback()
        raise


def change_destination_country(connection, destination_id, country):
    try:
        success = (
            update_destination_country(
                connection,
                destination_id,
                country,
            )
            == 1
        )

        connection.commit()

        return success

    except Exception:
        connection.rollback()
        raise


def list_destinations(connection):
    return get_all_destinations(connection)


def list_destinations_for_selection(connection):
    return get_all_destinations_by_airport_code(connection)
