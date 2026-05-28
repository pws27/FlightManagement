"""
CLI actions related to pilot management.

This module handles user interaction for creating, updating,
listing pilots, and viewing pilot schedules.
Business operations are delegated to the application layer.
"""

from application.pilots import (
    change_pilot_first_name,
    change_pilot_last_name,
    create_pilot,
    get_pilot_schedule,
    list_pilots,
    remove_pilot,
)

from cli.display import (
    display_flights,
    display_pilots,
)

from cli.prompts import (
    prompt_for_required_text,
    prompt_for_selection,
    prompt_for_value_from_list,
    prompt_for_menu_selection,
)
from cli.screen import clear_screen


def view_pilot_schedule_action(connection):
    pilot = prompt_for_selection(
        "Choose pilot ID",
        list_pilots(connection),
        display_pilots,
    )

    if pilot is None:
        return

    pilot_id = pilot[0]

    flights = get_pilot_schedule(connection, pilot_id)

    clear_screen()

    print("Pilot Schedule")

    display_flights(flights)


def add_pilot_action(connection):
    print("\nAdd New Pilot\n")

    first_name = prompt_for_required_text("First name")
    last_name = prompt_for_required_text("Last name")

    try:
        create_pilot(connection, first_name, last_name)

        print("Pilot added successfully.")

    except Exception as error:
        print(f"Could not add pilot: {error}")


def view_pilots_action(connection):
    pilots = list_pilots(connection)
    display_pilots(pilots)


def update_pilot_action(connection):
    pilot = prompt_for_selection(
        "Choose pilot ID",
        list_pilots(connection),
        display_pilots,
    )

    if pilot is None:
        return

    pilot_id = pilot[0]

    update_type = prompt_for_value_from_list(
        "Choose field to update",
        [
            "First name",
            "Last name",
        ],
    )

    new_value = prompt_for_required_text(f"New {update_type.lower()}")

    try:
        if update_type == "First name":
            success = change_pilot_first_name(connection, pilot_id, new_value)
        else:
            success = change_pilot_last_name(connection, pilot_id, new_value)

        if success:
            print("Pilot updated successfully.")
        else:
            print("Pilot could not be found.")

    except Exception as error:
        print(f"Could not update pilot: {error}")


def delete_pilot_action(connection):
    pilot = prompt_for_selection(
        "Choose pilot ID to delete",
        list_pilots(connection),
        display_pilots,
    )

    if pilot is None:
        return

    confirm = prompt_for_value_from_list(
        "Are you sure you want to delete this pilot?",
        ["No", "Yes"],
    )

    if confirm == "No":
        print("Delete cancelled.")
        return

    try:
        success = remove_pilot(connection, pilot[0])

        if success:
            print("Pilot deleted successfully.")
        else:
            print("Pilot could not be found.")

    except Exception as error:
        print(f"Could not delete pilot: {error}")


def pilots_menu_action(connection):

    clear_screen()

    action = prompt_for_menu_selection(PILOT_GROUPS)

    if action is None:
        return

    clear_screen()

    action(connection)


PILOT_GROUPS = [
    (
        "Pilots",
        [
            ("List", view_pilots_action),
            ("Add", add_pilot_action),
            ("Update", update_pilot_action),
            ("View schedule", view_pilot_schedule_action),
            ("Delete", delete_pilot_action),
        ],
    ),
]
