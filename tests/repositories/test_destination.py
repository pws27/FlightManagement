"""
Repository tests for destination-related database operations.

These tests verify destination creation, airport code
constraints, uniqueness checks, and update behaviour.
"""

import sqlite3

from repositories.destinations import (
    add_destination,
    airport_code_exists,
    get_all_destinations,
    get_all_destinations_by_airport_code,
    update_destination_airport_code,
)

from tests.database_test_case import DatabaseTestCase


class TestDestinationRepository(DatabaseTestCase):

    def test_add_destination_inserts_destination(self):
        self.seed_test_destination()

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT airport_code, city, country
            FROM destinations
        """)

        destination = cursor.fetchone()

        self.assertEqual(destination[0], "LHR")
        self.assertEqual(destination[1], "London")
        self.assertEqual(destination[2], "United Kingdom")

    def test_add_destination_rejects_duplicate_airport_code(self):
        self.seed_test_destination()

        with self.assertRaises(sqlite3.IntegrityError):
            self.seed_test_destination()

    def test_add_destination_rejects_invalid_airport_code_length(self):
        with self.assertRaises(sqlite3.IntegrityError):
            add_destination(
                self.connection,
                airport_code="LOND",
                city="London",
                country="United Kingdom",
            )

    def test_add_destination_rejects_lowercase_airport_code(self):
        with self.assertRaises(sqlite3.IntegrityError):
            add_destination(
                self.connection,
                airport_code="lhr",
                city="London",
                country="United Kingdom",
            )

    def test_airport_code_exists_returns_true(self):
        self.seed_test_destination()

        other_destination_id = add_destination(
            self.connection,
            airport_code="JFK",
            city="New York",
            country="United States",
        )

        exists = airport_code_exists(
            self.connection,
            airport_code="LHR",
            exclude_destination_id=other_destination_id,
        )

        self.assertTrue(exists)

    def test_airport_code_exists_returns_false_for_same_destination(
        self,
    ):
        destination_id = self.seed_test_destination()

        exists = airport_code_exists(
            self.connection,
            airport_code="LHR",
            exclude_destination_id=destination_id,
        )

        self.assertFalse(exists)

    def test_update_destination_airport_code_updates_code(self):
        destination_id = self.seed_test_destination()

        updated_rows = update_destination_airport_code(
            self.connection,
            destination_id,
            airport_code="JFK",
        )

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT airport_code
            FROM destinations
            WHERE destination_id = ?
        """,
            (destination_id,),
        )

        destination = cursor.fetchone()

        self.assertEqual(updated_rows, 1)
        self.assertEqual(destination[0], "JFK")

    def test_get_all_destinations_returns_destinations_ordered_by_airport_code(self):
        add_destination(
            self.connection,
            airport_code="JFK",
            city="New York",
            country="United States",
        )

        self.seed_test_destination()

        destinations = get_all_destinations(self.connection)

        self.assertEqual(
            destinations,
            [
                ("JFK", "New York", "United States"),
                ("LHR", "London", "United Kingdom"),
            ],
        )

    def test_get_all_destinations_by_airport_code_returns_selection_data(self):

        add_destination(
            self.connection,
            airport_code="JFK",
            city="New York",
            country="United States",
        )

        self.seed_test_destination()

        destinations = get_all_destinations_by_airport_code(
            self.connection,
        )

        self.assertEqual(
            destinations,
            [
                ("JFK", "New York", "United States", 1),
                ("LHR", "London", "United Kingdom", 2),
            ],
        )

    def test_airport_code_exists_returns_true_without_excluded_destination(self):
        self.seed_test_destination()

        exists = airport_code_exists(
            self.connection,
            airport_code="LHR",
        )

        self.assertTrue(exists)
