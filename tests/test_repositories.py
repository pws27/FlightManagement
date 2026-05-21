import sqlite3
import unittest

from database import create_tables
from repositories import (
    add_destination, 
    add_flight, 
    update_flight_status, 
    assign_pilot_to_flight,
    delete_flight,
    airport_code_exists_for_other_destination,
    update_destination_airport_code,
    get_flights_by_criteria,
)


class TestRepositories(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")

        self.connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        create_tables(self.connection)

    def tearDown(self):
        self.connection.close()

    def test_add_flight_inserts_row(self):
        flight_id = self.seed_test_flight()

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT
                flight_number,
                destination_id,
                departure_datetime,
                status
            FROM flights
            WHERE flight_id = ?
        """, (flight_id,))

        row = cursor.fetchone()

        self.assertEqual(row[0], "UOB100")
        self.assertEqual(row[1], 1)
        self.assertEqual(row[2], "2026-06-01 10:00")
        self.assertEqual(row[3], "Scheduled")

    def test_add_destination_inserts_row(self):
        self.seed_test_destination()

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT
                airport_code,
                city,
                country
            FROM destinations
        """)

        row = cursor.fetchone()

        self.assertEqual(row[0], "LHR")
        self.assertEqual(row[1], "London")
        self.assertEqual(row[2], "United Kingdom")

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

        row = cursor.fetchone()

        self.assertEqual(row[0], "Delayed")


    def test_add_destination_rejects_duplicate_airport_code(self):
        self.seed_test_destination()

        with self.assertRaises(sqlite3.IntegrityError):
            add_destination(
                self.connection,
                "LHR",
                "Another London",
                "UK",
            )


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

        row = cursor.fetchone()

        self.assertEqual(row[0], pilot_id)


    def test_delete_flight_deletes_row(self):
        flight_id = self.seed_test_flight()

        deleted_rows = delete_flight(
            self.connection,
            flight_id,
        )

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM flights
            WHERE flight_id = ?
        """, (flight_id,))

        row = cursor.fetchone()

        self.assertEqual(deleted_rows, 1)
        self.assertEqual(row[0], 0)


    def test_airport_code_exists_for_other_destination_returns_true(self):
        existing_destination_id = self.seed_test_destination()

        other_destination_id = add_destination(
            self.connection,
            "JFK",
            "New York",
            "United States",
        )

        exists = airport_code_exists_for_other_destination(
            self.connection,
            "LHR",
            other_destination_id,
        )

        self.assertTrue(exists)

    def test_airport_code_exists_for_other_destination_returns_false_for_same_destination(self):
        destination_id = self.seed_test_destination()

        exists = airport_code_exists_for_other_destination(
            self.connection,
            "LHR",
            destination_id,
        )

        self.assertFalse(exists)

    def test_update_destination_airport_code_updates_code(self):
        destination_id = self.seed_test_destination()

        updated_rows = update_destination_airport_code(
            self.connection,
            destination_id,
            "JFK",
        )

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT airport_code
            FROM destinations
            WHERE destination_id = ?
        """, (destination_id,))

        row = cursor.fetchone()

        self.assertEqual(updated_rows, 1)
        self.assertEqual(row[0], "JFK")


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


    def test_delete_flight_returns_zero_for_missing_flight(self):
        deleted_rows = delete_flight(self.connection, 999)

        self.assertEqual(deleted_rows, 0)


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

        rows = get_flights_by_criteria(
            self.connection,
            destination_id=new_york_destination_id,
        )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "UOB200")
        self.assertEqual(rows[0][1], "New York")
        self.assertEqual(rows[0][4], "Delayed")


    def test_get_flights_by_criteria_filters_by_status(self):
        destination_id = self.seed_test_destination()

        add_flight(
            self.connection,
            "UOB100",
            destination_id,
            "2026-06-01 10:00",
            "Scheduled",
        )

        add_flight(
            self.connection,
            "UOB200",
            destination_id,
            "2026-06-01 12:00",
            "Delayed",
        )

        rows = get_flights_by_criteria(
            self.connection,
            status="Delayed",
        )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "UOB200")


    def test_get_flights_by_criteria_filters_by_departure_date(self):
        destination_id = self.seed_test_destination()

        add_flight(
            self.connection,
            "UOB100",
            destination_id,
            "2026-06-01 10:00",
            "Scheduled",
        )

        add_flight(
            self.connection,
            "UOB200",
            destination_id,
            "2026-06-02 12:00",
            "Scheduled",
        )

        rows = get_flights_by_criteria(
            self.connection,
            departure_date="2026-06-02",
        )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "UOB200")


    def test_get_flights_by_criteria_applies_combined_filters(self):
        london_id = self.seed_test_destination()

        new_york_id = add_destination(
            self.connection,
            "JFK",
            "New York",
            "United States",
        )

        add_flight(self.connection, "UOB100", london_id, "2026-06-01 10:00", "Scheduled")
        add_flight(self.connection, "UOB200", new_york_id, "2026-06-01 12:00", "Scheduled")
        add_flight(self.connection, "UOB300", new_york_id, "2026-06-02 12:00", "Delayed")

        rows = get_flights_by_criteria(
            self.connection,
            destination_id=new_york_id,
            status="Scheduled",
            departure_date="2026-06-01",
        )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "UOB200")


    def seed_test_destination(self):
        destination_id = add_destination(
            self.connection,
            "LHR",
            "London",
            "United Kingdom",
        )

        return destination_id

    def seed_test_flight(self):

        destination_id = self.seed_test_destination()

        flight_id = add_flight(
            self.connection,
            "UOB100",
            destination_id,
            "2026-06-01 10:00",
            "Scheduled",
        )

        return flight_id
    
    def seed_test_pilot(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO pilots (
                first_name,
                last_name
            )
            VALUES (?, ?)
        """, (
            "Peter",
            "Somerville",
        ))

        self.connection.commit()

        return cursor.lastrowid

if __name__ == "__main__":
    unittest.main()