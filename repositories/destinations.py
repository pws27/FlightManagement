"""
Database queries and update operations related to destinations.

This module manages destination records and airport code
lookups used throughout the flight management system.

Keeping SQL operations in repository modules makes database
queries easier to locate, test, and explain separately from
CLI interaction and business logic.
"""


def add_destination(connection, airport_code, city, country):
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO destinations (
            airport_code,
            city,
            country
        )
        VALUES (?, ?, ?)
    """,
        (
            airport_code,
            city,
            country,
        ),
    )

    connection.commit()

    return cursor.lastrowid


def get_all_destinations(connection):
    """
    Retrieves destination data for display, ordered by airport code.
    """

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
    """
    Retrieves destination data ordered by airport code for CLI selection.

    The destination_id is included so selected airport codes can be mapped
    back to their database row.
    """

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

    cursor.execute(
        """
        UPDATE destinations
        SET airport_code = ?
        WHERE destination_id = ?
    """,
        (airport_code, destination_id),
    )

    connection.commit()

    return cursor.rowcount


def update_destination_city(connection, destination_id, city):
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE destinations
        SET city = ?
        WHERE destination_id = ?
    """,
        (city, destination_id),
    )

    connection.commit()

    return cursor.rowcount


def update_destination_country(connection, destination_id, country):
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE destinations
        SET country = ?
        WHERE destination_id = ?
    """,
        (country, destination_id),
    )

    connection.commit()

    return cursor.rowcount


def airport_code_exists(
    connection,
    airport_code,
    exclude_destination_id=None,
):
    """
    Checks whether an airport code is already used by another destination.

    The current destination is excluded so an existing code can be retained
    during an update.

    When exclude_destination_id is None, the check applies to all destinations.
    """

    cursor = connection.cursor()

    query = """
        SELECT 1
        FROM destinations
        WHERE airport_code = ?
    """

    params = [airport_code]

    if exclude_destination_id is not None:
        query += """
          AND destination_id != ?
        """

        params.append(exclude_destination_id)

    cursor.execute(query, params)

    return cursor.fetchone() is not None
