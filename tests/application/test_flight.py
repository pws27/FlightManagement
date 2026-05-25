"""
Application tests for flight-related use cases.

These tests verify application-layer behaviour such as
duplicate flight validation, search behaviour, update
success booleans, and pilot assignment operations.
"""

import sqlite3

from application.exceptions.flight_number_already_exists import (
    FlightNumberAlreadyExists,
)

from application.exceptions.pilot_already_assigned_on_date import (
    PilotAlreadyAssignedOnDate,
)

from application.flights import (
    assign_pilot_to_existing_flight,
    change_flight_departure_datetime,
    change_flight_status,
    create_flight,
    get_departure_datetime_range,
    list_flights,
    list_flights_for_selection,
    remove_flight,
    search_flights,
    unassign_pilot_from_existing_flight,
)

from application.pilots import get_pilot_schedule
from repositories.destinations import add_destination
from tests.database_test_case import DatabaseTestCase


class TestFlightApplication(DatabaseTestCase):

    def test_create_flight_returns_flight_id(self):
        flight_id = self.seed_test_flight()

        self.assertGreater(flight_id, 0)

    def test_search_flights_returns_matching_flights(self):
        self.seed_test_flight()

        flights = search_flights(self.connection, status="Scheduled")

        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0][0], "UOB100")

    def test_search_flights_treats_any_status_as_no_filter(self):
        self.seed_test_flight()

        flights = search_flights(self.connection, status="Any")

        self.assertEqual(len(flights), 1)

    def test_list_flights_returns_all_flights(self):
        self.seed_test_flight()

        flights = list_flights(self.connection)

        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0][0], "UOB100")

    def test_list_flights_for_selection_returns_selection_data(self):
        self.seed_test_flight()

        flights = list_flights_for_selection(self.connection)

        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0][1], "UOB100")

    def test_change_flight_status_returns_true_when_flight_exists(self):
        flight_id = self.seed_test_flight()

        success = change_flight_status(
            self.connection,
            flight_id,
            status="Delayed",
        )

        self.assertTrue(success)

    def test_change_flight_status_returns_false_when_flight_missing(self):
        success = change_flight_status(
            self.connection,
            flight_id=999,
            status="Delayed",
        )

        self.assertFalse(success)

    def test_change_flight_departure_datetime_returns_true_when_flight_exists(self):
        flight_id = self.seed_test_flight()

        success = change_flight_departure_datetime(
            self.connection,
            flight_id,
            departure_datetime="2026-06-02 14:30",
        )

        self.assertTrue(success)

    def test_change_flight_departure_datetime_returns_false_when_flight_missing(self):
        success = change_flight_departure_datetime(
            self.connection,
            flight_id=999,
            departure_datetime="2026-06-02 14:30",
        )

        self.assertFalse(success)

    def test_remove_flight_returns_true_when_flight_exists(self):
        flight_id = self.seed_test_flight()

        success = remove_flight(self.connection, flight_id)

        self.assertTrue(success)

    def test_remove_flight_returns_false_when_flight_missing(self):
        success = remove_flight(
            self.connection,
            flight_id=999,
        )

        self.assertFalse(success)

    def test_assign_pilot_to_existing_flight_returns_true_when_flight_exists(self):
        flight_id = self.seed_test_flight()
        pilot_id = self.seed_test_pilot()

        success = assign_pilot_to_existing_flight(self.connection, flight_id, pilot_id)

        self.assertTrue(success)

    def test_assign_pilot_to_existing_flight_returns_false_when_flight_missing(
        self,
    ):
        pilot_id = self.seed_test_pilot()

        success = assign_pilot_to_existing_flight(
            self.connection,
            flight_id=999,
            pilot_id=pilot_id,
        )

        self.assertFalse(success)

    def test_create_flight_rejects_duplicate_flight_number(self):
        self.seed_test_flight()

        destination_id = add_destination(
            self.connection,
            airport_code="JFK",
            city="New York",
            country="United States",
        )

        with self.assertRaises(FlightNumberAlreadyExists):
            create_flight(
                self.connection,
                flight_number="UOB100",
                destination_id=destination_id,
                departure_datetime="2026-06-01 12:00",
                status="Scheduled",
            )

    def test_search_flights_filters_by_departure_date(self):
        destination_id = self.seed_test_destination()

        create_flight(
            self.connection,
            flight_number="UOB200",
            destination_id=destination_id,
            departure_datetime="2026-06-02 12:00",
            status="Scheduled",
        )

        flights = search_flights(
            self.connection,
            departure_date="2026-06-02",
        )

        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0][0], "UOB200")

    def test_unassign_pilot_from_existing_flight_returns_true_when_flight_exists(self):
        flight_id = self.seed_test_flight()
        pilot_id = self.seed_test_pilot()

        assign_pilot_to_existing_flight(
            self.connection,
            flight_id,
            pilot_id,
        )

        success = unassign_pilot_from_existing_flight(
            self.connection,
            flight_id,
        )

        self.assertTrue(success)

    def test_unassign_pilot_from_existing_flight_returns_false_when_flight_missing(
        self,
    ):
        success = unassign_pilot_from_existing_flight(
            self.connection,
            flight_id=999,
        )

        self.assertFalse(success)

    def test_get_departure_datetime_range_returns_start_and_next_day(self):
        start, end = get_departure_datetime_range("2026-06-02")

        self.assertEqual(start, "2026-06-02 00:00")
        self.assertEqual(end, "2026-06-03 00:00")

    def test_search_flights_applies_combined_filters(self):
        london_destination_id = self.seed_test_destination()

        paris_destination_id = add_destination(
            self.connection,
            airport_code="CDG",
            city="Paris",
            country="France",
        )

        create_flight(
            self.connection,
            flight_number="UOB200",
            destination_id=london_destination_id,
            departure_datetime="2026-06-02 10:00",
            status="Scheduled",
        )

        create_flight(
            self.connection,
            flight_number="UOB201",
            destination_id=london_destination_id,
            departure_datetime="2026-06-02 12:00",
            status="Delayed",
        )

        create_flight(
            self.connection,
            flight_number="UOB202",
            destination_id=paris_destination_id,
            departure_datetime="2026-06-02 14:00",
            status="Scheduled",
        )

        flights = search_flights(
            self.connection,
            destination_id=london_destination_id,
            status="Scheduled",
            departure_date="2026-06-02",
        )

        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0][0], "UOB200")

    def test_unassign_pilot_removes_flight_from_pilot_schedule(self):
        flight_id = self.seed_test_flight()
        pilot_id = self.seed_test_pilot()

        assign_pilot_to_existing_flight(
            self.connection,
            flight_id,
            pilot_id,
        )

        unassign_pilot_from_existing_flight(
            self.connection,
            flight_id,
        )

        flights = get_pilot_schedule(
            self.connection,
            pilot_id,
        )

        self.assertEqual(len(flights), 0)

    def test_create_flight_rejects_invalid_status(self):
        destination_id = self.seed_test_destination()

        with self.assertRaises(sqlite3.IntegrityError):
            create_flight(
                self.connection,
                flight_number="UOB200",
                destination_id=destination_id,
                departure_datetime="2026-06-01 12:00",
                status="Unknown",
            )

    def test_change_flight_status_rejects_invalid_status(self):
        flight_id = self.seed_test_flight()

        with self.assertRaises(sqlite3.IntegrityError):
            change_flight_status(
                self.connection,
                flight_id,
                status="Unknown",
            )

    def test_assign_pilot_to_existing_flight_rejects_same_pilot_on_same_date(self):
        destination_id = self.seed_test_destination()
        pilot_id = self.seed_test_pilot()

        create_flight(
            self.connection,
            flight_number="UOB200",
            destination_id=destination_id,
            departure_datetime="2026-06-01 10:00",
            status="Scheduled",
            pilot_id=pilot_id,
        )

        second_flight_id = create_flight(
            self.connection,
            flight_number="UOB201",
            destination_id=destination_id,
            departure_datetime="2026-06-01 12:00",
            status="Scheduled",
        )

        with self.assertRaises(PilotAlreadyAssignedOnDate):
            assign_pilot_to_existing_flight(
                self.connection,
                second_flight_id,
                pilot_id,
            )
