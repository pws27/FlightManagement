def display_flights(rows):
    if not rows:
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

    for row in rows:
        (
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
            f"{flight_number:<10} "
            f"{city:<18} "
            f"{country:<22} "
            f"{departure_datetime:<18} "
            f"{status:<12} "
            f"{pilot_name:<25}"
        )

def display_destination_codes(rows):
    if not rows:
        print("No destinations found.")
        return

    print()
    print(
        f"{'Code':<8} "
        f"{'City':<18} "
        f"{'Country':<22}"
    )
    print("-" * 50)

    for airport_code, city, country, destination_id in rows:
        print(
            f"{airport_code:<8} "
            f"{city:<18} "
            f"{country:<22}"
        )


def display_pilots(rows):
    if not rows:
        print("No pilots found.")
        return

    print()
    print(
        f"{'ID':<5} "
        f"{'Pilot':<25}"
    )
    print("-" * 32)

    for pilot_id, first_name, last_name in rows:
        pilot_name = f"{first_name} {last_name}"

        print(
            f"{pilot_id:<5} "
            f"{pilot_name:<25}"
        )


def display_flight_counts_by_destination(rows):
    if not rows:
        print("No destination data found.")
        return

    print()
    print(
        f"{'Destination':<18} "
        f"{'Country':<22} "
        f"{'Flights':<8}"
    )
    print("-" * 50)

    for city, country, number_of_flights in rows:
        print(
            f"{city:<18} "
            f"{country:<22} "
            f"{number_of_flights:<8}"
        )


def display_flight_counts_by_pilot(rows):
    if not rows:
        print("No pilot data found.")
        return

    print()
    print(
        f"{'Pilot':<25} "
        f"{'Flights':<8}"
    )
    print("-" * 35)

    for first_name, last_name, number_of_flights in rows:
        pilot_name = f"{first_name} {last_name}"

        print(
            f"{pilot_name:<25} "
            f"{number_of_flights:<8}"
        )

def display_flight_selection(rows):
    if not rows:
        print("No flights found.")
        return

    print()
    print(
        f"{'ID':<5} "
        f"{'Flight':<10} "
        f"{'Departure':<18} "
        f"{'Status':<12}"
    )
    print("-" * 50)

    for flight_id, flight_number, departure_datetime, status in rows:
        print(
            f"{flight_id:<5} "
            f"{flight_number:<10} "
            f"{departure_datetime:<18} "
            f"{status:<12}"
        )