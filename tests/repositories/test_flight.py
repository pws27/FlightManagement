"""
Repository tests for flight-related database operations.

These tests verify flight creation, updates, deletion,
filtering queries, and pilot assignment behaviour.
"""

import sqlite3

from repositories.destinations import add_destination
from repositories.flights import (
    add_flight,
    assign_pilot_to_flight,
    delete_flight,
    flight_number_exists,
    get_all_flight_details,
    get_all_flights_for_selection,
    find_flights,
    pilot_has_flight_on_departure_date,
    unassign_pilot_from_flight,
    update_flight_departure_datetime,
    update_flight_status,
)
from tests.database_test_case import DatabaseTestCase


class TestFlightRepository(DatabaseTestCase):

    def test_add_flight_inserts_flight(self):
        flight_id = self.seed_test_flight()

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT flight_number, destination_id, departure_datetime, status
            FROM flights
            WHERE flight_id = ?
        """,
            (flight_id,),
        )

        flight = cursor.fetchone()

        self.assertEqual(flight[0], "UOB100")
        self.assertEqual(flight[1], 1)
        self.assertEqual(flight[2], "2026-06-01 10:00")
        self.assertEqual(flight[3], "Scheduled")

    def test_add_flight_rejects_duplicate_flight_number(self):
        self.seed_test_flight()

        with self.assertRaises(sqlite3.IntegrityError):
            add_flight(
                self.connection,
                flight_number="UOB100",
                destination_id=1,
                departure_datetime="2026-06-01 12:00",
                status="Scheduled",
            )

    def test_add_flight_rejects_invalid_destination_id(self):
        with self.assertRaises(sqlite3.IntegrityError):
            add_flight(
                self.connection,
                flight_number="UOB200",
                destination_id=999,
                departure_datetime="2026-06-01 12:00",
                status="Scheduled",
            )

    def test_update_flight_status(self):
        flight_id = self.seed_test_flight()

        update_flight_status(
            self.connection,
            flight_id,
            "Delayed",
        )

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT status
            FROM flights
            WHERE flight_id = ?
        """,
            (flight_id,),
        )

        flight = cursor.fetchone()

        self.assertEqual(flight[0], "Delayed")

    def test_assign_pilot_to_flight_updates_pilot_id(self):
        flight_id = self.seed_test_flight()
        pilot_id = self.seed_test_pilot()

        assign_pilot_to_flight(
            self.connection,
            flight_id,
            pilot_id,
        )

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

        self.assertEqual(flight[0], pilot_id)

    def test_unassign_pilot_from_flight_sets_pilot_id_to_null(self):
        flight_id = self.seed_test_flight()
        pilot_id = self.seed_test_pilot()

        assign_pilot_to_flight(
            self.connection,
            flight_id,
            pilot_id,
        )

        updated_rows = unassign_pilot_from_flight(
            self.connection,
            flight_id,
        )

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

        self.assertEqual(updated_rows, 1)
        self.assertIsNone(flight[0])

    def test_delete_flight_deletes_flight(self):
        flight_id = self.seed_test_flight()

        updated_rows = delete_flight(
            self.connection,
            flight_id,
        )

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM flights
            WHERE flight_id = ?
        """,
            (flight_id,),
        )

        flight = cursor.fetchone()

        self.assertEqual(updated_rows, 1)
        self.assertEqual(flight[0], 0)

    def test_delete_flight_returns_zero_for_missing_flight(self):
        updated_rows = delete_flight(self.connection, 999)

        self.assertEqual(updated_rows, 0)

    def test_find_flights_filters_by_destination_id(self):
        london_destination_id = self.seed_test_destination()

        new_york_destination_id = add_destination(
            self.connection,
            airport_code="JFK",
            city="New York",
            country="United States",
        )

        add_flight(
            self.connection,
            flight_number="UOB100",
            destination_id=london_destination_id,
            departure_datetime="2026-06-01 10:00",
            status="Scheduled",
        )

        add_flight(
            self.connection,
            flight_number="UOB200",
            destination_id=new_york_destination_id,
            departure_datetime="2026-06-01 12:00",
            status="Delayed",
        )

        flights = find_flights(
            self.connection,
            destination_id=new_york_destination_id,
        )

        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0][0], "UOB200")
        self.assertEqual(flights[0][1], "New York")
        self.assertEqual(flights[0][4], "Delayed")

    def test_find_flights_filters_by_departure_datetime_range(self):
        destination_id = self.seed_test_destination()

        add_flight(
            self.connection,
            flight_number="UOB100",
            destination_id=destination_id,
            departure_datetime="2026-06-01 10:00",
            status="Scheduled",
        )

        add_flight(
            self.connection,
            flight_number="UOB200",
            destination_id=destination_id,
            departure_datetime="2026-06-02 12:00",
            status="Scheduled",
        )

        flights = find_flights(
            self.connection,
            departure_start="2026-06-02 00:00",
            departure_end="2026-06-03 00:00",
        )

        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0][0], "UOB200")

    def test_find_flights_filters_by_status(self):
        destination_id = self.seed_test_destination()

        add_flight(
            self.connection,
            flight_number="UOB100",
            destination_id=destination_id,
            departure_datetime="2026-06-01 10:00",
            status="Scheduled",
        )

        add_flight(
            self.connection,
            flight_number="UOB200",
            destination_id=destination_id,
            departure_datetime="2026-06-01 12:00",
            status="Delayed",
        )

        flights = find_flights(
            self.connection,
            status="Delayed",
        )

        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0][0], "UOB200")
        self.assertEqual(flights[0][4], "Delayed")

    def test_flight_number_exists_returns_true_when_flight_exists(self):
        self.seed_test_flight()

        exists = flight_number_exists(
            self.connection,
            flight_number="UOB100",
        )

        self.assertTrue(exists)

    def test_flight_number_exists_returns_false_when_flight_does_not_exist(self):
        self.seed_test_flight()

        exists = flight_number_exists(
            self.connection,
            flight_number="UOB999",
        )

        self.assertFalse(exists)

    def test_add_flight_rejects_invalid_status(self):
        destination_id = self.seed_test_destination()

        with self.assertRaises(sqlite3.IntegrityError):
            add_flight(
                self.connection,
                flight_number="UOB200",
                destination_id=destination_id,
                departure_datetime="2026-06-01 12:00",
                status="Unknown",
            )

    def test_update_flight_status_rejects_invalid_status(self):
        flight_id = self.seed_test_flight()

        with self.assertRaises(sqlite3.IntegrityError):
            update_flight_status(
                self.connection,
                flight_id,
                status="Unknown",
            )

    def test_add_flight_rejects_invalid_departure_datetime_format(self):
        destination_id = self.seed_test_destination()

        with self.assertRaises(sqlite3.IntegrityError):
            add_flight(
                self.connection,
                flight_number="UOB200",
                destination_id=destination_id,
                departure_datetime="2026/06/01 12:00",
                status="Scheduled",
            )

    def test_find_flights_applies_multiple_filters(self):
        london_destination_id = self.seed_test_destination()

        paris_destination_id = add_destination(
            self.connection,
            airport_code="CDG",
            city="Paris",
            country="France",
        )

        add_flight(
            self.connection,
            flight_number="UOB100",
            destination_id=london_destination_id,
            departure_datetime="2026-06-02 10:00",
            status="Scheduled",
        )

        add_flight(
            self.connection,
            flight_number="UOB200",
            destination_id=london_destination_id,
            departure_datetime="2026-06-02 12:00",
            status="Delayed",
        )

        add_flight(
            self.connection,
            flight_number="UOB300",
            destination_id=paris_destination_id,
            departure_datetime="2026-06-02 14:00",
            status="Scheduled",
        )

        flights = find_flights(
            self.connection,
            destination_id=london_destination_id,
            status="Scheduled",
            departure_start="2026-06-02 00:00",
            departure_end="2026-06-03 00:00",
        )

        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0][0], "UOB100")

    def test_update_flight_status_returns_zero_for_missing_flight(self):
        updated_rows = update_flight_status(
            self.connection,
            flight_id=999,
            status="Delayed",
        )

        self.assertEqual(updated_rows, 0)

    def test_unassign_pilot_from_flight_returns_zero_for_missing_flight(self):
        updated_rows = unassign_pilot_from_flight(
            self.connection,
            flight_id=999,
        )

        self.assertEqual(updated_rows, 0)

    def test_update_flight_departure_datetime_returns_zero_for_missing_flight(self):
        updated_rows = update_flight_departure_datetime(
            self.connection,
            flight_id=999,
            departure_datetime="2026-06-02 14:30",
        )

        self.assertEqual(updated_rows, 0)

    def test_assign_pilot_to_flight_returns_zero_for_missing_flight(self):
        pilot_id = self.seed_test_pilot()

        updated_rows = assign_pilot_to_flight(
            self.connection,
            flight_id=999,
            pilot_id=pilot_id,
        )

        self.assertEqual(updated_rows, 0)

    def test_pilot_has_flight_on_departure_date_returns_true_when_booked(self):
        flight_id = self.seed_test_flight()
        pilot_id = self.seed_test_pilot()

        assign_pilot_to_flight(
            self.connection,
            flight_id,
            pilot_id,
        )

        exists = pilot_has_flight_on_departure_date(
            self.connection,
            pilot_id,
            departure_datetime="2026-06-01 12:00",
        )

        self.assertTrue(exists)

    def test_pilot_has_flight_on_departure_date_excludes_current_flight(self):
        flight_id = self.seed_test_flight()
        pilot_id = self.seed_test_pilot()

        assign_pilot_to_flight(
            self.connection,
            flight_id,
            pilot_id,
        )

        exists = pilot_has_flight_on_departure_date(
            self.connection,
            pilot_id,
            departure_datetime="2026-06-01 12:00",
            exclude_flight_id=flight_id,
        )

        self.assertFalse(exists)

    def test_assign_pilot_to_flight_rejects_same_pilot_on_same_date(self):
        destination_id = self.seed_test_destination()
        pilot_id = self.seed_test_pilot()

        add_flight(
            self.connection,
            flight_number="UOB100",
            destination_id=destination_id,
            departure_datetime="2026-06-01 10:00",
            status="Scheduled",
            pilot_id=pilot_id,
        )

        second_flight_id = add_flight(
            self.connection,
            flight_number="UOB200",
            destination_id=destination_id,
            departure_datetime="2026-06-01 12:00",
            status="Scheduled",
        )

        with self.assertRaises(sqlite3.IntegrityError):
            assign_pilot_to_flight(
                self.connection,
                flight_id=second_flight_id,
                pilot_id=pilot_id,
            )

    def test_get_all_flight_details_returns_joined_flight_data(self):
        destination_id = self.seed_test_destination()
        pilot_id = self.seed_test_pilot()

        add_flight(
            self.connection,
            flight_number="UOB100",
            destination_id=destination_id,
            departure_datetime="2026-06-01 10:00",
            status="Scheduled",
            pilot_id=pilot_id,
        )

        flights = get_all_flight_details(self.connection)

        self.assertEqual(len(flights), 1)

        self.assertEqual(
            flights[0],
            (
                "UOB100",
                "London",
                "United Kingdom",
                "2026-06-01 10:00",
                "Scheduled",
                "John",
                "Smith",
            ),
        )

    def test_get_all_flights_for_selection_returns_selection_data(self):
        flight_id = self.seed_test_flight()

        flights = get_all_flights_for_selection(self.connection)

        self.assertEqual(
            flights,
            [
                (
                    flight_id,
                    "UOB100",
                    "2026-06-01 10:00",
                    "Scheduled",
                ),
            ],
        )
