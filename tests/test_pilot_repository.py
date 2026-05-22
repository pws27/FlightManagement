"""
Repository tests for pilot-related database operations.

These tests verify pilot creation and update behaviour
used by scheduling and flight assignment features.
"""

from repositories.pilots import (
    add_pilot,
    update_pilot_first_name,
    update_pilot_last_name,
)
from tests.database_test_case import DatabaseTestCase


class TestPilotRepository(DatabaseTestCase):

    def test_add_pilot_inserts_pilot(self):
        pilot_id = add_pilot(
            self.connection,
            "Peter",
            "Somerville",
        )

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT first_name, last_name
            FROM pilots
            WHERE pilot_id = ?
        """, (pilot_id,))

        pilot = cursor.fetchone()

        self.assertEqual(pilot[0], "Peter")
        self.assertEqual(pilot[1], "Somerville")

    def test_update_pilot_first_name_updates_pilot(self):
        pilot_id = self.seed_test_pilot()

        updated_rows = update_pilot_first_name(
            self.connection,
            pilot_id,
            "Julie",
        )

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT first_name
            FROM pilots
            WHERE pilot_id = ?
        """, (pilot_id,))

        pilot = cursor.fetchone()

        self.assertEqual(updated_rows, 1)
        self.assertEqual(pilot[0], "Julie")

    def test_update_pilot_last_name_updates_pilot(self):
        pilot_id = self.seed_test_pilot()

        updated_rows = update_pilot_last_name(
            self.connection,
            pilot_id,
            "Amphlett",
        )

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT last_name
            FROM pilots
            WHERE pilot_id = ?
        """, (pilot_id,))

        pilot = cursor.fetchone()

        self.assertEqual(updated_rows, 1)
        self.assertEqual(pilot[0], "Amphlett")
        