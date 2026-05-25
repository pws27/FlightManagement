"""
Repository tests for aggregate reporting queries.

These tests verify grouped counting queries used for
reporting on destinations, flights, and airports.
"""

from repositories.destinations import add_destination
from repositories.reports import (
    count_airports_by_country,
    count_flights_by_destination,
    count_flights_by_pilot,
)
from tests.database_test_case import DatabaseTestCase


class TestReportRepository(DatabaseTestCase):

    def test_count_airports_by_country(self):
        self.seed_test_destination()

        add_destination(
            self.connection,
            airport_code="MAN",
            city="Manchester",
            country="United Kingdom",
        )

        add_destination(
            self.connection,
            airport_code="JFK",
            city="New York",
            country="United States",
        )

        countries = count_airports_by_country(self.connection)

        self.assertEqual(countries[0], ("United Kingdom", 2))
        self.assertEqual(countries[1], ("United States", 1))

    def test_count_flights_by_destination(self):
        self.seed_test_flight()
        destinations = count_flights_by_destination(self.connection)

        self.assertEqual(destinations[0], ("London", "United Kingdom", 1))

    def test_count_flights_by_pilot(self):
        flight_id = self.seed_test_flight()
        pilot_id = self.seed_test_pilot()

        cursor = self.connection.cursor()
        cursor.execute(
            """
            UPDATE flights
            SET pilot_id = ?
            WHERE flight_id = ?
            """,
            (pilot_id, flight_id),
        )
        self.connection.commit()

        pilots = count_flights_by_pilot(self.connection)

        self.assertEqual(pilots[0], ("John", "Smith", 1))
