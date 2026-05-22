from application.exceptions.airport_code_already_exists import (
    AirportCodeAlreadyExists,
)

from repositories.destinations import (
    add_destination,
    airport_code_exists_for_other_destination,
    get_all_destinations, 
    get_all_destinations_by_airport_code, 
    update_destination_airport_code,
    update_destination_city,
    update_destination_country,
)


def ensure_airport_code_is_available_for_destination(
    connection,
    airport_code,
    destination_id,
):
    if airport_code_exists_for_other_destination(
        connection,
        airport_code,
        destination_id,
    ):
        raise AirportCodeAlreadyExists()

def create_destination(connection, airport_code, city, country):
    return add_destination(connection, airport_code, city, country)

def change_destination_airport_code(connection, destination_id, airport_code):
    ensure_airport_code_is_available_for_destination(
        connection,
        airport_code,
        destination_id,
    )

    return update_destination_airport_code(connection, destination_id, airport_code) == 1


def change_destination_city(connection, destination_id, city):
    return update_destination_city(connection, destination_id, city) == 1


def change_destination_country(connection, destination_id, country):
    return update_destination_country(connection, destination_id, country) == 1


def list_destinations(connection):
    return get_all_destinations(connection)


def list_destinations_for_selection(connection):
    return get_all_destinations_by_airport_code(connection)