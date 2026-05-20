from cli.actions import (
    add_flight_action,
    count_destinations_action,
    count_pilots_action,
    search_flights_action,
    view_all_flights_action,
    view_pilot_schedule_action,
)

from cli.prompts import prompt_for_menu_selection


MENU_OPTIONS = [
    ("View all flights", view_all_flights_action),
    ("Search flights by criteria", search_flights_action),
    ("Count flights by destination", count_destinations_action),
    ("Count flights by pilot", count_pilots_action),
    ("Add new flight", add_flight_action),
    ("View pilot schedule", view_pilot_schedule_action),
]

def run_cli(connection):
    while True:
        action = prompt_for_menu_selection(MENU_OPTIONS)

        if action is None:
            print("Goodbye.")
            break

        action(connection)