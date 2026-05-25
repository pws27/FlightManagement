"""
Main CLI application loop and top-level menu navigation.

This module coordinates submenu actions and manages
the overall flow of the flight management system.
"""

from cli.actions.destinations import destinations_menu_action
from cli.actions.flights import flights_menu_action
from cli.actions.pilots import pilots_menu_action
from cli.actions.reports import reports_menu_action

from cli.prompts import (
    prompt_for_menu_selection,
    pause,
)

from cli.screen import clear_screen

MENU_GROUPS = [
    (
        "Main Menu",
        [
            ("Flights", flights_menu_action),
            ("Pilots", pilots_menu_action),
            ("Destinations", destinations_menu_action),
            ("Reports", reports_menu_action),
        ],
    ),
]


def run_cli(connection):
    while True:
        clear_screen()
        action = prompt_for_menu_selection(MENU_GROUPS)

        if action is None:
            print("Goodbye.")
            break

        clear_screen()

        action(connection)

        pause()
