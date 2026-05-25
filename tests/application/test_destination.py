"""
Application tests for destination-related use cases.

These tests verify application-layer behaviour such as
business rule enforcement and row-count to success-boolean
translation.
"""

from application.destinations import (
    change_destination_airport_code,
    change_destination_city,
    change_destination_country,
    create_destination,
)

from application.exceptions.airport_code_already_exists import (
    AirportCodeAlreadyExists,
)
from tests.database_test_case import DatabaseTestCase


class TestDestinationApplication(DatabaseTestCase):

    def test_create_destination_returns_destination_id(self):
        destination_id = create_destination(
            self.connection,
            airport_code="JFK",
            city="New York",
            country="United States",
        )

        self.assertGreater(destination_id, 0)

    def test_change_destination_airport_code_returns_true_when_destination_exists(self):
        destination_id = self.seed_test_destination()

        success = change_destination_airport_code(
            self.connection,
            destination_id,
            airport_code="JFK",
        )

        self.assertTrue(success)

    def test_change_destination_airport_code_returns_false_when_destination_missing(
        self,
    ):
        success = change_destination_airport_code(
            self.connection,
            destination_id=999,
            airport_code="JFK",
        )

        self.assertFalse(success)

    def test_change_destination_airport_code_rejects_duplicate_code(self):
        self.seed_test_destination()

        other_destination_id = create_destination(
            self.connection,
            airport_code="JFK",
            city="New York",
            country="United States",
        )

        with self.assertRaises(AirportCodeAlreadyExists):
            change_destination_airport_code(
                self.connection,
                other_destination_id,
                airport_code="LHR",
            )

    def test_change_destination_city_returns_true_when_destination_exists(self):
        destination_id = self.seed_test_destination()

        success = change_destination_city(
            self.connection,
            destination_id,
            city="Manchester",
        )

        self.assertTrue(success)

    def test_change_destination_city_returns_false_when_destination_missing(self):
        success = change_destination_city(
            self.connection,
            destination_id=999,
            city="Manchester",
        )

        self.assertFalse(success)

    def test_change_destination_country_returns_true_when_destination_exists(self):
        destination_id = self.seed_test_destination()

        success = change_destination_country(
            self.connection,
            destination_id,
            country="France",
        )

        self.assertTrue(success)

    def test_change_destination_country_returns_false_when_destination_missing(self):
        success = change_destination_country(
            self.connection,
            destination_id=999,
            country="France",
        )

        self.assertFalse(success)

    def test_create_destination_rejects_duplicate_airport_code(self):
        self.seed_test_destination()

        with self.assertRaises(AirportCodeAlreadyExists):
            create_destination(
                self.connection,
                airport_code="LHR",
                city="Another London",
                country="UK",
            )

    def test_change_destination_airport_code_allows_existing_code_for_same_destination(
        self,
    ):
        destination_id = self.seed_test_destination()

        success = change_destination_airport_code(
            self.connection,
            destination_id,
            airport_code="LHR",
        )

        self.assertTrue(success)
