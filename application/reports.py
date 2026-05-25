"""
Application-layer reporting use cases.

This module provides reporting operations used by
presentation layers to retrieve aggregate flight,
pilot, and destination statistics.

Report generation queries are delegated to repository
modules while this layer exposes application-focused
operations.
"""

from repositories.reports import (
    count_airports_by_country,
    count_flights_by_destination,
    count_flights_by_pilot,
    get_unassigned_flights,
)


def get_flight_counts_by_destination(connection):
    return count_flights_by_destination(connection)


def get_flight_counts_by_pilot(connection):
    return count_flights_by_pilot(connection)


def get_airport_counts_by_country(connection):
    return count_airports_by_country(connection)


def list_unassigned_flights(connection):
    return get_unassigned_flights(connection)
