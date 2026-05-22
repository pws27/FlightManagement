"""
Aggregate reporting queries for the flight management system.

This module contains SQL queries that use grouping and
counting functions to summarise flight and destination data.
"""

def count_flights_by_destination(connection):
    """
    Counts flights grouped by destination.
    Includes destinations with no flights.
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