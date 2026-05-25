"""
Application tests for reporting use cases.

These tests verify that application-layer reporting functions
return aggregate data from the reporting repositories.
"""

from application.destinations import create_destination
from application.reports import (
    get_airport_counts_by_country,
    get_flight_counts_by_destination,
    get_flight_counts_by_pilot,
)
from application.flights import assign_pilot_to_existing_flight
from tests.database_test_case import DatabaseTestCase


class TestReportApplication(DatabaseTestCase):

    def test_get_airport_counts_by_country(self):
        self.seed_test_destination()

        create_destination(
            self.connection,
            airport_code="MAN",
            city="Manchester",
            country="United Kingdom",
        )

        countries = get_airport_counts_by_country(self.connection)

        self.assertEqual(countries[0], ("United Kingdom", 2))

    def test_get_flight_counts_by_destination(self):
        self.seed_test_flight()

        destinations = get_flight_counts_by_destination(self.connection)

        self.assertEqual(destinations[0], ("London", "United Kingdom", 1))

    def test_get_flight_counts_by_pilot(self):
        flight_id = self.seed_test_flight()
        pilot_id = self.seed_test_pilot()

        assign_pilot_to_existing_flight(self.connection, flight_id, pilot_id)

        pilots = get_flight_counts_by_pilot(self.connection)

        self.assertEqual(pilots[0], ("John", "Smith", 1))

    def test_get_flight_counts_by_pilot_includes_pilots_with_no_flights(self):
        self.seed_test_pilot()

        pilots = get_flight_counts_by_pilot(self.connection)

        self.assertEqual(len(pilots), 1)
        self.assertEqual(pilots[0], ("John", "Smith", 0))

    def test_get_flight_counts_by_destination_includes_destinations_with_no_flights(
        self,
    ):
        self.seed_test_destination()

        destinations = get_flight_counts_by_destination(self.connection)

        self.assertEqual(len(destinations), 1)
        self.assertEqual(destinations[0], ("London", "United Kingdom", 0))
