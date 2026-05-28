"""
Database queries and update operations related to pilots.

This module manages pilot records and supports flight
assignment and scheduling features within the application.

This separation keeps persistence concerns independent from
user interaction and application-level decision making.
"""


def get_all_pilots(connection):
    """
    Retrieves pilot records ordered by pilot ID for display and selection.
    """

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

    cursor.execute(
        """
        INSERT INTO pilots (
            first_name,
            last_name
        )
        VALUES (?, ?)
    """,
        (
            first_name,
            last_name,
        ),
    )

    return cursor.lastrowid


def update_pilot_first_name(connection, pilot_id, first_name):
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE pilots
        SET first_name = ?
        WHERE pilot_id = ?
    """,
        (first_name, pilot_id),
    )

    return cursor.rowcount


def update_pilot_last_name(connection, pilot_id, last_name):
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE pilots
        SET last_name = ?
        WHERE pilot_id = ?
    """,
        (last_name, pilot_id),
    )

    return cursor.rowcount


def delete_pilot(connection, pilot_id):
    """
    Deletes a pilot record.

    Related flight assignments are automatically cleared through the
    ON DELETE SET NULL foreign key action defined in the schema.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM pilots
        WHERE pilot_id = ?
        """,
        (pilot_id,),
    )

    return cursor.rowcount
