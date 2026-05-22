from repositories.reports import (
    count_airports_by_country,
    count_flights_by_destination,
    count_flights_by_pilot,
)


def get_flight_counts_by_destination(connection):
    return count_flights_by_destination(connection)


def get_flight_counts_by_pilot(connection):
    return count_flights_by_pilot(connection)


def get_airport_counts_by_country(connection):
    return count_airports_by_country(connection)