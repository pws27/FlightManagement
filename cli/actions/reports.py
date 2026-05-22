"""
CLI actions for report generation and summary views.

This module provides menu actions that execute aggregate
report queries and display summarised database information.
"""

from cli.display import (
    display_flight_counts_by_destination, 
    display_flight_counts_by_pilot,
    display_airport_counts_by_country,
)

from cli.prompts import prompt_for_menu_selection

from application.reports import (
    get_airport_counts_by_country,
    get_flight_counts_by_destination,
    get_flight_counts_by_pilot,
)

def count_destinations_action(connection):
    destinations = get_flight_counts_by_destination(connection)
    display_flight_counts_by_destination(destinations)


def count_pilots_action(connection):
    pilots = get_flight_counts_by_pilot(connection)
    display_flight_counts_by_pilot(pilots)


def count_airports_by_country_action(connection):
    countries = get_airport_counts_by_country(connection)
    display_airport_counts_by_country(countries)


def reports_menu_action(connection):
    action = prompt_for_menu_selection(REPORT_GROUPS)

    if action is None:
        return

    action(connection)


REPORT_GROUPS = [
    (
        "Reports",
        [
            ("Count flights by destination", count_destinations_action),
            ("Count flights by pilot", count_pilots_action),
            ("Count airports by country", count_airports_by_country_action),
        ],
    ),
]