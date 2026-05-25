"""
Shared database test infrastructure for repository tests.

This module creates an isolated in-memory SQLite database
and provides reusable helper methods for seeding test data.
"""

import sqlite3
import unittest

from database import create_tables
from repositories.destinations import add_destination
from repositories.flights import add_flight


class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.execute("PRAGMA foreign_keys = ON")
        create_tables(self.connection)

    def tearDown(self):
        self.connection.close()

    def seed_test_destination(self):
        return add_destination(
            self.connection,
            airport_code="LHR",
            city="London",
            country="United Kingdom",
        )

    def seed_test_flight(self):
        destination_id = self.seed_test_destination()

        return add_flight(
            self.connection,
            flight_number="UOB100",
            destination_id=destination_id,
            departure_datetime="2026-06-01 10:00",
            status="Scheduled",
        )

    def seed_test_pilot(self):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO pilots (
                first_name,
                last_name
            )
            VALUES (?, ?)
        """,
            (
                "John",
                "Smith",
            ),
        )

        self.connection.commit()

        return cursor.lastrowid
