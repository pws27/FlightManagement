"""
Application-layer pilot use cases.

This module coordinates pilot-related business operations
including pilot creation, updates, listing, and schedule
retrieval.

The application layer encapsulates business intent while
delegating persistence operations to repositories.
"""

from repositories.pilots import (
    add_pilot,
    delete_pilot,
    get_all_pilots,
    update_pilot_first_name,
    update_pilot_last_name,
)

from repositories.flights import get_flights_by_pilot_id


def get_pilot_schedule(connection, pilot_id):
    return get_flights_by_pilot_id(connection, pilot_id)


def create_pilot(connection, first_name, last_name):
    return add_pilot(connection, first_name, last_name)


def change_pilot_first_name(connection, pilot_id, first_name):
    return update_pilot_first_name(connection, pilot_id, first_name) == 1


def change_pilot_last_name(connection, pilot_id, last_name):
    return update_pilot_last_name(connection, pilot_id, last_name) == 1


def list_pilots(connection):
    return get_all_pilots(connection)


def remove_pilot(connection, pilot_id):
    return delete_pilot(connection, pilot_id) == 1
