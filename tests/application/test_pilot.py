"""
Application tests for pilot-related use cases.

These tests verify application-layer behaviour such as
pilot creation, update success booleans, and schedule retrieval.
"""

from application.flights import assign_pilot_to_existing_flight

from application.pilots import (
    change_pilot_first_name,
    change_pilot_last_name,
    create_pilot,
    get_pilot_schedule,
    remove_pilot,
)
from tests.database_test_case import DatabaseTestCase


class TestPilotApplication(DatabaseTestCase):

    def test_create_pilot_returns_pilot_id(self):
        pilot_id = create_pilot(
            self.connection,
            first_name="John",
            last_name="Smith",
        )

        self.assertGreater(pilot_id, 0)

    def test_change_pilot_first_name_returns_true_when_pilot_exists(self):
        pilot_id = self.seed_test_pilot()

        success = change_pilot_first_name(
            self.connection,
            pilot_id,
            first_name="Julie",
        )

        self.assertTrue(success)

    def test_change_pilot_first_name_returns_false_when_pilot_missing(self):
        success = change_pilot_first_name(
            self.connection,
            pilot_id=999,
            first_name="Julie",
        )

        self.assertFalse(success)

    def test_change_pilot_last_name_returns_true_when_pilot_exists(self):
        pilot_id = self.seed_test_pilot()

        success = change_pilot_last_name(
            self.connection,
            pilot_id,
            last_name="Amphlett",
        )

        self.assertTrue(success)

    def test_change_pilot_last_name_returns_false_when_pilot_missing(self):
        success = change_pilot_last_name(
            self.connection,
            pilot_id=999,
            last_name="Amphlett",
        )

        self.assertFalse(success)

    def test_get_pilot_schedule_returns_assigned_flights(self):
        flight_id = self.seed_test_flight()
        pilot_id = self.seed_test_pilot()

        assign_pilot_to_existing_flight(
            self.connection,
            flight_id,
            pilot_id,
        )

        flights = get_pilot_schedule(
            self.connection,
            pilot_id,
        )

        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0][0], "UOB100")

    def test_remove_pilot_returns_true_when_pilot_exists(self):
        pilot_id = self.seed_test_pilot()

        success = remove_pilot(
            self.connection,
            pilot_id,
        )

        self.assertTrue(success)

    def test_remove_pilot_returns_false_when_pilot_missing(self):
        success = remove_pilot(
            self.connection,
            pilot_id=999,
        )

        self.assertFalse(success)
