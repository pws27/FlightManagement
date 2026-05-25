"""
Repository tests for pilot-related database operations.

These tests verify pilot creation and update behaviour
used by scheduling and flight assignment features.
"""

from repositories.flights import assign_pilot_to_flight
from repositories.pilots import (
    add_pilot,
    delete_pilot,
    get_all_pilots,
    update_pilot_first_name,
    update_pilot_last_name,
)
from tests.database_test_case import DatabaseTestCase


class TestPilotRepository(DatabaseTestCase):

    def test_add_pilot_inserts_pilot(self):
        pilot_id = add_pilot(
            self.connection,
            first_name="John",
            last_name="Smith",
        )

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT first_name, last_name
            FROM pilots
            WHERE pilot_id = ?
        """,
            (pilot_id,),
        )

        pilot = cursor.fetchone()

        self.assertEqual(pilot[0], "John")
        self.assertEqual(pilot[1], "Smith")

    def test_update_pilot_first_name_updates_pilot(self):
        pilot_id = self.seed_test_pilot()

        updated_rows = update_pilot_first_name(
            self.connection,
            pilot_id,
            first_name="Julie",
        )

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT first_name
            FROM pilots
            WHERE pilot_id = ?
        """,
            (pilot_id,),
        )

        pilot = cursor.fetchone()

        self.assertEqual(updated_rows, 1)
        self.assertEqual(pilot[0], "Julie")

    def test_update_pilot_last_name_updates_pilot(self):
        pilot_id = self.seed_test_pilot()

        updated_rows = update_pilot_last_name(
            self.connection,
            pilot_id,
            last_name="Amphlett",
        )

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT last_name
            FROM pilots
            WHERE pilot_id = ?
        """,
            (pilot_id,),
        )

        pilot = cursor.fetchone()

        self.assertEqual(updated_rows, 1)
        self.assertEqual(pilot[0], "Amphlett")

    def test_update_pilot_first_name_returns_zero_for_missing_pilot(self):
        updated_rows = update_pilot_first_name(
            self.connection,
            pilot_id=999,
            first_name="Julie",
        )

        self.assertEqual(updated_rows, 0)

    def test_update_pilot_last_name_returns_zero_for_missing_pilot(self):
        updated_rows = update_pilot_last_name(
            self.connection,
            pilot_id=999,
            last_name="Amphlett",
        )

        self.assertEqual(updated_rows, 0)

    def test_delete_pilot_sets_flight_pilot_id_to_null(self):
        flight_id = self.seed_test_flight()
        pilot_id = self.seed_test_pilot()

        assign_pilot_to_flight(self.connection, flight_id, pilot_id)

        delete_pilot(self.connection, pilot_id)

        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT pilot_id
            FROM flights
            WHERE flight_id = ?
            """,
            (flight_id,),
        )

        flight = cursor.fetchone()

        self.assertIsNone(flight[0])

    def test_get_all_pilots_returns_pilots_ordered_by_id(self):
        first_pilot_id = add_pilot(
            self.connection,
            first_name="John",
            last_name="Smith",
        )

        second_pilot_id = add_pilot(
            self.connection,
            first_name="Julie",
            last_name="Amphlett",
        )

        pilots = get_all_pilots(self.connection)

        self.assertEqual(
            pilots,
            [
                (first_pilot_id, "John", "Smith"),
                (second_pilot_id, "Julie", "Amphlett"),
            ],
        )
