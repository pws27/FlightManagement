"""
CLI display and table-formatting functions.

This module is responsible for presenting query results
in a readable tabular format for the command-line interface.
"""


def display_flights(flights):
    """
    Displays flight information in a formatted table.
    """
    if not flights:
        print("No flights found.")
        return

    print()
    print(
        f"{'Flight':<10} "
        f"{'Destination':<18} "
        f"{'Country':<22} "
        f"{'Departure':<18} "
        f"{'Status':<12} "
        f"{'Pilot':<25}"
    )
    print("-" * 115)

    for flight in flights:
        (
            flight_number,
            city,
            country,
            departure_datetime,
            status,
            pilot_first_name,
            pilot_last_name,
        ) = flight

        pilot_name = "Unassigned"

        if pilot_first_name and pilot_last_name:
            pilot_name = f"{pilot_first_name} {pilot_last_name}"

        print(
            f"{flight_number:<10} "
            f"{city:<18} "
            f"{country:<22} "
            f"{departure_datetime:<18} "
            f"{status:<12} "
            f"{pilot_name:<25}"
        )


def display_destination_codes(destinations):
    if not destinations:
        print("No destinations found.")
        return

    print()
    print(f"{'Code':<8} " f"{'City':<18} " f"{'Country':<22}")
    print("-" * 50)

    for destination in destinations:
        airport_code, city, country = destination[:3]
        print(f"{airport_code:<8} " f"{city:<18} " f"{country:<22}")


def display_pilots(pilots):
    """
    Displays pilot information in a formatted table.
    """
    if not pilots:
        print("No pilots found.")
        return

    print()
    print(f"{'ID':<5} " f"{'Pilot':<25}")
    print("-" * 32)

    for pilot_id, first_name, last_name in pilots:
        pilot_name = f"{first_name} {last_name}"

        print(f"{pilot_id:<5} " f"{pilot_name:<25}")


def display_flight_counts_by_destination(destinations):
    if not destinations:
        print("No destination data found.")
        return

    print()
    print(f"{'Destination':<18} " f"{'Country':<22} " f"{'Flights':<8}")
    print("-" * 50)

    for city, country, number_of_flights in destinations:
        print(f"{city:<18} " f"{country:<22} " f"{number_of_flights:<8}")


def display_flight_counts_by_pilot(pilots):
    if not pilots:
        print("No pilot data found.")
        return

    print()
    print(f"{'Pilot':<25} " f"{'Flights':<8}")
    print("-" * 35)

    for first_name, last_name, number_of_flights in pilots:
        pilot_name = f"{first_name} {last_name}"

        print(f"{pilot_name:<25} " f"{number_of_flights:<8}")


def display_flight_selection(flights):
    if not flights:
        print("No flights found.")
        return

    print()
    print(f"{'ID':<5} " f"{'Flight':<10} " f"{'Departure':<18} " f"{'Status':<12}")
    print("-" * 50)

    for flight_id, flight_number, departure_datetime, status in flights:
        print(
            f"{flight_id:<5} "
            f"{flight_number:<10} "
            f"{departure_datetime:<18} "
            f"{status:<12}"
        )


def display_airport_counts_by_country(countries):
    if not countries:
        print("No country data found.")
        return

    print()
    print(f"{'Country':<25} " f"{'Airports':<10}")
    print("-" * 36)

    for country, number_of_airports in countries:
        print(f"{country:<25} " f"{number_of_airports:<10}")


def display_unassigned_flights(flights):
    if not flights:
        print("No unassigned flights found.")
        return

    print()
    print(f"{'Flight':<10} {'Departure':<18} {'Status':<12}")
    print("-" * 42)

    for flight_number, departure_datetime, status in flights:
        print(f"{flight_number:<10} " f"{departure_datetime:<18} " f"{status:<12}")
