from repositories import (
    count_flights_by_destination,
    count_flights_by_pilot,
    get_flights_by_criteria,
    view_all_flights,
    add_flight,
)


def run_menu(connection):
    while True:
        display_menu()

        choice = input("Choose an option: ").strip()
        exit_option = str(len(MENU_OPTIONS) + 1)

        if choice == exit_option:
            print("Goodbye.")
            break

        try:
            selected_index = int(choice) - 1
            _, action = MENU_OPTIONS[selected_index]
            action(connection)
        except (ValueError, IndexError):
            print("Invalid option. Please choose again.")


def display_menu():
    print("\nFlight Management System\n")

    for index, (description, _) in enumerate(MENU_OPTIONS, start=1):
        print(f"{index}. {description}")

    print(f"{len(MENU_OPTIONS) + 1}. Exit")
    print()


def view_all_flights_action(connection):
    rows = view_all_flights(connection)
    display_flights(rows)


def search_flights_action(connection):
    city = input("Destination city, leave blank to ignore: ").strip()
    status = input("Status, leave blank to ignore: ").strip()
    departure_date = input("Departure date YYYY-MM-DD, leave blank to ignore: ").strip()

    rows = get_flights_by_criteria(
        connection,
        city=city or None,
        status=status or None,
        departure_date=departure_date or None,
    )

    display_flights(rows)


def count_destinations_action(connection):
    rows = count_flights_by_destination(connection)
    display_flight_counts_by_destination(rows)


def count_pilots_action(connection):
    rows = count_flights_by_pilot(connection)
    display_flight_counts_by_pilot(rows)

def add_flight_action(connection):
    print("\nAdd New Flight\n")

    flight_number = input("Flight number: ").strip()
    destination_id = input("Destination ID: ").strip()
    departure_datetime = input(
        "Departure datetime (YYYY-MM-DD HH:MM): "
    ).strip()

    status = input("Status: ").strip()

    pilot_id = input(
        "Pilot ID (leave blank for unassigned): "
    ).strip()

    if not pilot_id:
        pilot_id = None

    try:
        add_flight(
            connection,
            flight_number=flight_number,
            destination_id=int(destination_id),
            departure_datetime=departure_datetime,
            status=status,
            pilot_id=int(pilot_id) if pilot_id else None,
        )

        print("Flight added successfully.")

    except Exception as error:
        print(f"Error adding flight: {error}")

MENU_OPTIONS = [
    ("View all flights", view_all_flights_action),
    ("Search flights by criteria", search_flights_action),
    ("Count flights by destination", count_destinations_action),
    ("Count flights by pilot", count_pilots_action),
    ("Add new flight", add_flight_action),
]


def display_flights(rows):
    if not rows:
        print("No flights found.")
        return

    print()
    print(
        f"{'ID':<5} "
        f"{'Flight':<10} "
        f"{'Destination':<18} "
        f"{'Country':<22} "
        f"{'Departure':<18} "
        f"{'Status':<12} "
        f"{'Pilot':<25}"
    )
    print("-" * 115)

    for row in rows:
        (
            flight_id,
            flight_number,
            city,
            country,
            departure_datetime,
            status,
            pilot_first_name,
            pilot_last_name,
        ) = row

        pilot_name = "Unassigned"

        if pilot_first_name and pilot_last_name:
            pilot_name = f"{pilot_first_name} {pilot_last_name}"

        print(
            f"{flight_id:<5} "
            f"{flight_number:<10} "
            f"{city:<18} "
            f"{country:<22} "
            f"{departure_datetime:<18} "
            f"{status:<12} "
            f"{pilot_name:<25}"
        )


def display_flight_counts_by_destination(rows):
    if not rows:
        print("No destination data found.")
        return

    print()
    print(f"{'Destination':<18} {'Country':<22} {'Flights':<8}")
    print("-" * 50)

    for city, country, number_of_flights in rows:
        print(f"{city:<18} {country:<22} {number_of_flights:<8}")


def display_flight_counts_by_pilot(rows):
    if not rows:
        print("No pilot data found.")
        return

    print()
    print(f"{'Pilot':<25} {'Flights':<8}")
    print("-" * 35)

    for first_name, last_name, number_of_flights in rows:
        pilot_name = f"{first_name} {last_name}"
        print(f"{pilot_name:<25} {number_of_flights:<8}")