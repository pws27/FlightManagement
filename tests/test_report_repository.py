"""
Repository tests for aggregate reporting queries.

These tests verify grouped counting queries used for
reporting on destinations, flights, and airports.
"""

from repositories.destinations import add_destination
from repositories.reports import count_airports_by_country
from tests.database_test_case import DatabaseTestCase


class TestReportRepository(DatabaseTestCase):

    def test_count_airports_by_country(self):
        add_destination(
            self.connection,
            "LHR",
            "London",
            "United Kingdom",
        )

        add_destination(
            self.connection,
            "MAN",
            "Manchester",
            "United Kingdom",
        )

        add_destination(
            self.connection,
            "JFK",
            "New York",
            "United States",
        )

        countries = count_airports_by_country(self.connection)

        self.assertEqual(countries[0], ("United Kingdom", 2))
        self.assertEqual(countries[1], ("United States", 1))