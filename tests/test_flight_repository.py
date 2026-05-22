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
    get_flights_by_criteria,
    update_flight_status,
    flight_number_exists,
)
from tests.database_test_case import DatabaseTestCase


class TestFlightRepository(DatabaseTestCase):

    def test_add_flight_inserts_flight(self):
        flight_id = self.seed_test_flight()

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT flight_number, destination_id, departure_datetime, status
            FROM flights
            WHERE flight_id = ?
        """, (flight_id,))

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
                "UOB100",
                1,
                "2026-06-01 12:00",
                "Scheduled",
            )

    def test_add_flight_rejects_invalid_destination_id(self):
        with self.assertRaises(sqlite3.IntegrityError):
            add_flight(
                self.connection,
                "UOB200",
                999,
                "2026-06-01 12:00",
                "Scheduled",
            )

    def test_update_flight_status(self):
        flight_id = self.seed_test_flight()

        update_flight_status(
            self.connection,
            flight_id,
            "Delayed",
        )

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT status
            FROM flights
            WHERE flight_id = ?
        """, (flight_id,))

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

        cursor.execute("""
            SELECT pilot_id
            FROM flights
            WHERE flight_id = ?
        """, (flight_id,))

        flight = cursor.fetchone()

        self.assertEqual(flight[0], pilot_id)

    def test_delete_flight_deletes_flight(self):
        flight_id = self.seed_test_flight()

        updated_rows = delete_flight(
            self.connection,
            flight_id,
        )

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM flights
            WHERE flight_id = ?
        """, (flight_id,))

        flight = cursor.fetchone()

        self.assertEqual(updated_rows, 1)
        self.assertEqual(flight[0], 0)

    def test_delete_flight_returns_zero_for_missing_flight(self):
        updated_rows = delete_flight(self.connection, 999)

        self.assertEqual(updated_rows, 0)

    def test_get_flights_by_criteria_filters_by_destination_id(self):
        london_destination_id = self.seed_test_destination()

        new_york_destination_id = add_destination(
            self.connection,
            "JFK",
            "New York",
            "United States",
        )

        add_flight(
            self.connection,
            "UOB100",
            london_destination_id,
            "2026-06-01 10:00",
            "Scheduled",
        )

        add_flight(
            self.connection,
            "UOB200",
            new_york_destination_id,
            "2026-06-01 12:00",
            "Delayed",
        )

        flights = get_flights_by_criteria(
            self.connection,
            destination_id=new_york_destination_id,
        )

        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0][0], "UOB200")
        self.assertEqual(flights[0][1], "New York")
        self.assertEqual(flights[0][4], "Delayed")

        
    def test_flight_number_exists_returns_true_when_flight_exists(self):
        self.seed_test_flight()

        exists = flight_number_exists(
            self.connection,
            "UOB100",
        )

        self.assertTrue(exists)


    def test_flight_number_exists_returns_false_when_flight_does_not_exist(self):
        self.seed_test_flight()

        exists = flight_number_exists(
            self.connection,
            "UOB999",
        )

        self.assertFalse(exists)


    def test_add_flight_rejects_invalid_status(self):
        destination_id = self.seed_test_destination()

        with self.assertRaises(sqlite3.IntegrityError):
            add_flight(
                self.connection,
                "UOB200",
                destination_id,
                "2026-06-01 12:00",
                "Unknown",
            )


    def test_update_flight_status_rejects_invalid_status(self):
        flight_id = self.seed_test_flight()

        with self.assertRaises(sqlite3.IntegrityError):
            update_flight_status(
                self.connection,
                flight_id,
                "Unknown",
            )