"""
Database queries and update operations related to flights.

This module contains SQL used for retrieving, filtering,
creating, updating, and deleting flight records, including
queries involving destinations and pilot assignments.
"""

def get_all_flight_details(connection):
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


def get_flights_by_criteria(connection, destination_id=None, status=None, departure_date=None):
    """
    Retrieves flights using optional destination,
    status, and departure date filters.

    SQL conditions are added dynamically depending
    on which filters are provided.
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

    if departure_date is not None:
        query += " AND DATE(f.departure_datetime) = ?"
        params.append(departure_date)

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

    cursor.execute("""
        INSERT INTO flights (
            flight_number,
            destination_id,
            pilot_id,
            departure_datetime,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        flight_number,
        destination_id,
        pilot_id,
        departure_datetime,
        status,
    ))

    connection.commit()

    return cursor.lastrowid


def get_flights_by_pilot_id(connection, pilot_id):
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
        JOIN pilots p
            ON f.pilot_id = p.pilot_id
        WHERE p.pilot_id = ?
        ORDER BY f.departure_datetime
    """, (pilot_id,))

    return cursor.fetchall()


def get_all_flights_for_selection(connection):
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


def update_flight_status(connection, flight_id, status):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE flights
        SET status = ?
        WHERE flight_id = ?
    """, (status, flight_id))

    connection.commit()

    return cursor.rowcount


def update_flight_departure_datetime(connection, flight_id, departure_datetime):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE flights
        SET departure_datetime = ?
        WHERE flight_id = ?
    """, (departure_datetime, flight_id))

    connection.commit()

    return cursor.rowcount

def delete_flight(connection, flight_id):
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM flights
        WHERE flight_id = ?
    """, (flight_id,))

    connection.commit()

    return cursor.rowcount


def assign_pilot_to_flight(connection, flight_id, pilot_id):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE flights
        SET pilot_id = ?
        WHERE flight_id = ?
    """, (pilot_id, flight_id))

    connection.commit()

    return cursor.rowcount


def flight_number_exists(connection, flight_number):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 1
        FROM flights
        WHERE flight_number = ?
    """, (flight_number,))

    return cursor.fetchone() is not None
