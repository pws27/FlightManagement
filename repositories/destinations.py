"""
Database queries and update operations related to destinations.

This module manages destination records and airport code
lookups used throughout the flight management system.
"""

def add_destination(connection, airport_code, city, country):
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO destinations (
            airport_code,
            city,
            country
        )
        VALUES (?, ?, ?)
    """, (
        airport_code,
        city,
        country,
    ))

    connection.commit()

    return cursor.lastrowid


def get_all_destinations(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            airport_code,
            city,
            country
        FROM destinations
        ORDER BY airport_code
    """)

    return cursor.fetchall()


def get_all_destinations_by_airport_code(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            airport_code,
            city,
            country,
            destination_id
        FROM destinations
        ORDER BY airport_code
    """)

    return cursor.fetchall()


def update_destination_airport_code(connection, destination_id, airport_code):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE destinations
        SET airport_code = ?
        WHERE destination_id = ?
    """, (airport_code, destination_id))

    connection.commit()

    return cursor.rowcount


def update_destination_city(connection, destination_id, city):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE destinations
        SET city = ?
        WHERE destination_id = ?
    """, (city, destination_id))

    connection.commit()

    return cursor.rowcount


def update_destination_country(connection, destination_id, country):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE destinations
        SET country = ?
        WHERE destination_id = ?
    """, (country, destination_id))

    connection.commit()

    return cursor.rowcount


def airport_code_exists_for_other_destination(connection, airport_code, destination_id):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 1
        FROM destinations
        WHERE airport_code = ?
          AND destination_id != ?
    """, (airport_code, destination_id))

    return cursor.fetchone() is not None