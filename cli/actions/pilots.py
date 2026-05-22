"""
CLI actions related to pilot management.

This module handles pilot creation, pilot assignment
to flights, and viewing pilot schedules.
"""

from application.pilots import (
    change_pilot_first_name,
    change_pilot_last_name,
    create_pilot,
    get_pilot_schedule,
    list_pilots,
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

    display_flights(flights)


def add_pilot_action(connection):
    print("\nAdd New Pilot\n")

    first_name = prompt_for_required_text("First name")
    last_name = prompt_for_required_text("Last name")

    try:
        create_pilot(connection, first_name, last_name)

        print("Pilot added successfully.")

    except Exception as error:
        connection.rollback()
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
        connection.rollback()
        print(f"Could not update pilot: {error}")


def pilots_menu_action(connection):
    action = prompt_for_menu_selection(PILOT_GROUPS)

    if action is None:
        return

    action(connection)


PILOT_GROUPS = [
    (
        "Pilots",
        [
            ("List", view_pilots_action),
            ("Add", add_pilot_action),
            ("Update", update_pilot_action),
            ("View schedule", view_pilot_schedule_action),
        ],
    ),
]