"""
Database queries and update operations related to pilots.

This module manages pilot records and supports flight
assignment and scheduling features within the application.
"""

def get_all_pilots(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            pilot_id,
            first_name,
            last_name
        FROM pilots
        ORDER BY pilot_id
    """)

    return cursor.fetchall()


def add_pilot(connection, first_name, last_name):
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO pilots (
            first_name,
            last_name
        )
        VALUES (?, ?)
    """, (
        first_name,
        last_name,
    ))

    connection.commit()

    return cursor.lastrowid


def update_pilot_first_name(connection, pilot_id, first_name):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE pilots
        SET first_name = ?
        WHERE pilot_id = ?
    """, (first_name, pilot_id))

    connection.commit()

    return cursor.rowcount


def update_pilot_last_name(connection, pilot_id, last_name):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE pilots
        SET last_name = ?
        WHERE pilot_id = ?
    """, (last_name, pilot_id))

    connection.commit()

    return cursor.rowcount