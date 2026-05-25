"""
CLI actions for report generation and summary views.

This module provides menu actions that execute aggregate
report queries and display summarised database information.
"""

from cli.display import (
    display_flight_counts_by_destination,
    display_flight_counts_by_pilot,
    display_airport_counts_by_country,
    display_unassigned_flights,
)

from cli.prompts import prompt_for_menu_selection

from application.reports import (
    get_airport_counts_by_country,
    get_flight_counts_by_destination,
    get_flight_counts_by_pilot,
    list_unassigned_flights,
)
from cli.screen import clear_screen


def count_destinations_action(connection):
    destinations = get_flight_counts_by_destination(connection)

    clear_screen()

    print("Flights by Destination")

    display_flight_counts_by_destination(destinations)


def count_pilots_action(connection):
    pilots = get_flight_counts_by_pilot(connection)

    clear_screen()

    print("Flights by Pilot")

    display_flight_counts_by_pilot(pilots)


def count_airports_by_country_action(connection):
    countries = get_airport_counts_by_country(connection)

    clear_screen()

    print("Airports by Country")

    display_airport_counts_by_country(countries)


def view_unassigned_flights_action(connection):
    flights = list_unassigned_flights(connection)

    clear_screen()

    print("Unassigned Flights")

    display_unassigned_flights(flights)


def reports_menu_action(connection):

    clear_screen()

    action = prompt_for_menu_selection(REPORT_GROUPS)

    if action is None:
        return

    clear_screen()

    action(connection)


REPORT_GROUPS = [
    (
        "Reports",
        [
            ("Count flights by destination", count_destinations_action),
            ("Count flights by pilot", count_pilots_action),
            ("Count airports by country", count_airports_by_country_action),
            ("View unassigned flights", view_unassigned_flights_action),
        ],
    ),
]
