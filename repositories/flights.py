"""
Database queries and update operations related to flights.

This module contains SQL used for retrieving, filtering,
creating, updating, and deleting flight records, including
queries involving destinations and pilot assignments.

Separating SQL into repository modules keeps joins, filters,
aggregations, and update queries isolated from CLI code and
application business rules.
"""


def get_all_flight_details(connection):
    """
    Retrieves flight details joined with destination and optional pilot data.

    A LEFT JOIN is used for pilots so unassigned flights are still included
    in the main flight listing.
    """

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            f.flight_number,
            d.city,
            d.country,
            f.departure_datetime,
            f.status,
            p.first_name,
            p.last_name
        FROM flights f
        JOIN destinations d
            ON f.destination_id = d.destination_id
        LEFT JOIN pilots p
            ON f.pilot_id = p.pilot_id
        ORDER BY f.departure_datetime
    """)

    return cursor.fetchall()


def find_flights(
    connection,
    destination_id=None,
    status=None,
    departure_start=None,
    departure_end=None,
):
    """
    Retrieves flights using optional destination, status, and departure
    datetime filters.

    SQL conditions are added dynamically depending on which filters are
    provided. Query values are still passed as parameters to avoid SQL
    injection.
    """

    cursor = connection.cursor()

    query = """
        SELECT
            f.flight_number,
            d.city,
            d.country,
            f.departure_datetime,
            f.status,
            p.first_name,
            p.last_name
        FROM flights f
        JOIN destinations d
            ON f.destination_id = d.destination_id
        LEFT JOIN pilots p
            ON f.pilot_id = p.pilot_id
        WHERE 1 = 1
    """

    params = []

    if destination_id is not None:
        query += " AND f.destination_id = ?"
        params.append(destination_id)

    if status is not None:
        query += " AND f.status = ?"
        params.append(status)

    # A datetime range is used instead of DATE(...)
    # so the departure_datetime index can be used efficiently.
    if departure_start is not None and departure_end is not None:
        query += """
            AND f.departure_datetime >= ?
            AND f.departure_datetime < ?
        """
        params.append(departure_start)
        params.append(departure_end)

    query += " ORDER BY f.departure_datetime"

    cursor.execute(query, params)

    return cursor.fetchall()


def add_flight(
    connection,
    flight_number,
    destination_id,
    departure_datetime,
    status,
    pilot_id=None,
):
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO flights (
            flight_number,
            destination_id,
            pilot_id,
            departure_datetime,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """,
        (
            flight_number,
            destination_id,
            pilot_id,
            departure_datetime,
            status,
        ),
    )

    return cursor.lastrowid


def get_flights_by_pilot_id(connection, pilot_id):
    """
    Retrieves the schedule for a specific pilot.

    Only flights currently assigned to the selected pilot are returned.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            f.flight_number,
            d.city,
            d.country,
            f.departure_datetime,
            f.status,
            p.first_name,
            p.last_name
        FROM flights f
        JOIN destinations d
            ON f.destination_id = d.destination_id
        JOIN pilots p
            ON f.pilot_id = p.pilot_id
        WHERE p.pilot_id = ?
        ORDER BY f.departure_datetime
    """,
        (pilot_id,),
    )

    return cursor.fetchall()


def get_all_flights_for_selection(connection):
    """
    Retrieves compact flight data used by CLI selection prompts.
    """

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            flight_id,
            flight_number,
            departure_datetime,
            status
        FROM flights
        ORDER BY flight_id
    """)

    return cursor.fetchall()


def get_cancellable_flights(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            flight_id,
            flight_number,
            departure_datetime,
            status
        FROM flights
        WHERE status != 'Cancelled'
        ORDER BY departure_datetime
        """)

    return cursor.fetchall()


def update_flight_status(connection, flight_id, status):
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE flights
        SET status = ?
        WHERE flight_id = ?
    """,
        (status, flight_id),
    )

    return cursor.rowcount


def update_flight_departure_datetime(connection, flight_id, departure_datetime):
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE flights
        SET departure_datetime = ?
        WHERE flight_id = ?
    """,
        (departure_datetime, flight_id),
    )

    return cursor.rowcount


def assign_pilot_to_flight(connection, flight_id, pilot_id):
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE flights
        SET pilot_id = ?
        WHERE flight_id = ?
    """,
        (pilot_id, flight_id),
    )

    return cursor.rowcount


def unassign_pilot_from_flight(connection, flight_id):
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE flights
        SET pilot_id = NULL
        WHERE flight_id = ?
    """,
        (flight_id,),
    )

    return cursor.rowcount


def flight_number_exists(connection, flight_number):
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM flights
        WHERE flight_number = ?
    """,
        (flight_number,),
    )

    return cursor.fetchone() is not None


def get_flight_departure_datetime(connection, flight_id):
    """
    Retrieves a flight's departure datetime before assignment validation.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT departure_datetime
        FROM flights
        WHERE flight_id = ?
        """,
        (flight_id,),
    )

    row = cursor.fetchone()

    return row[0] if row else None


def pilot_has_flight_on_departure_date(
    connection,
    pilot_id,
    departure_datetime,
    exclude_flight_id=None,
):
    """
    Checks whether a pilot already has a flight on the same calendar date.

    exclude_flight_id allows the current flight to be ignored when checking
    whether an updated assignment would conflict with another flight.
    """

    cursor = connection.cursor()

    query = """
        SELECT 1
        FROM flights
        WHERE pilot_id = ?
          AND date(departure_datetime) = date(?)
    """

    params = [
        pilot_id,
        departure_datetime,
    ]

    if exclude_flight_id is not None:
        query += " AND flight_id != ?"
        params.append(exclude_flight_id)

    cursor.execute(query, params)

    return cursor.fetchone() is not None
