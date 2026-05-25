"""
Aggregate reporting queries for the flight management system.

This module contains SQL queries that summarise flight,
pilot, and destination data using grouping, counting,
LEFT JOINs, and NULL filtering.

Keeping reporting queries separate from the CLI and application
layers makes joins, grouping, and aggregation logic easier to
identify and evaluate.
"""


def count_flights_by_destination(connection):
    """
    Counts flights grouped by destination.

    A LEFT JOIN is used so destinations with no flights are still
    included in the report with a count of zero.
    """

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            d.city,
            d.country,
            COUNT(f.flight_id) AS number_of_flights
        FROM destinations d
        LEFT JOIN flights f
            ON d.destination_id = f.destination_id
        GROUP BY d.destination_id
        ORDER BY number_of_flights DESC
    """)

    return cursor.fetchall()


def count_flights_by_pilot(connection):
    """
    Counts flights assigned to each pilot.

    A LEFT JOIN is used so pilots with no assigned flights are still
    included in the report with a count of zero.
    """

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            p.first_name,
            p.last_name,
            COUNT(f.flight_id) AS number_of_flights
        FROM pilots p
        LEFT JOIN flights f
            ON p.pilot_id = f.pilot_id
        GROUP BY p.pilot_id
        ORDER BY number_of_flights DESC
    """)

    return cursor.fetchall()


def count_airports_by_country(connection):
    """
    Counts destinations grouped by country.

    This report summarises how many airport destinations are stored
    for each country in the database.
    """

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            country,
            COUNT(destination_id) AS number_of_airports
        FROM destinations
        GROUP BY country
        ORDER BY number_of_airports DESC, country
    """)

    return cursor.fetchall()


def get_unassigned_flights(connection):
    """
    Returns flights that do not currently have an assigned pilot.

    This query reflects the optional pilot assignment relationship,
    where flights can exist with a NULL pilot_id.
    """

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            flight_number,
            departure_datetime,
            status
        FROM flights
        WHERE pilot_id IS NULL
        ORDER BY departure_datetime
    """)

    return cursor.fetchall()
