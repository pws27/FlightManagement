"""
Database setup and seed data for the flight management system.

This module creates the SQLite schema, opens database connections,
and inserts sample data used by the CLI application.
"""

import os
import random
import sqlite3
from datetime import datetime, timedelta

from constants import DATE_FORMAT, DB_NAME, DATETIME_FORMAT, FLIGHT_STATUSES

FIRST_NAMES = [
    "Brooke",
    "Carrie",
    "Grant",
    "Hamish",
    "Harry",
    "Jamie",
    "Johnny",
    "Joy",
    "Julie",
    "Keren",
    "Kyron",
    "Paul",
    "Terry",
    "Thomas",
    "William",
]

LAST_NAMES = [
    "Amphlett",
    "Brice",
    "Christie",
    "Cobain",
    "Harper",
    "McGalloway",
    "O'Kane",
    "Simpson",
    "Smith",
    "Strang",
    "Thompson",
    "Wilson",
    "Young",
]

AIRPORTS = [
    ("AMS", "Amsterdam", "Netherlands"),
    ("ARN", "Stockholm", "Sweden"),
    ("BCN", "Barcelona", "Spain"),
    ("BER", "Berlin", "Germany"),
    ("CDG", "Paris", "France"),
    ("DUB", "Dublin", "Ireland"),
    ("DXB", "Dubai", "United Arab Emirates"),
    ("EDI", "Edinburgh", "United Kingdom"),
    ("HND", "Tokyo", "Japan"),
    ("JFK", "New York", "United States"),
    ("KIX", "Osaka", "Japan"),
    ("LAX", "Los Angeles", "United States"),
    ("LHR", "London", "United Kingdom"),
    ("MAD", "Madrid", "Spain"),
    ("MAN", "Manchester", "United Kingdom"),
    ("MEL", "Melbourne", "Australia"),
    ("MUC", "Munich", "Germany"),
    ("MXP", "Milan", "Italy"),
    ("NCE", "Nice", "France"),
    ("ORD", "Chicago", "United States"),
    ("SYD", "Sydney", "Australia"),
    ("YVR", "Vancouver", "Canada"),
    ("YYZ", "Toronto", "Canada"),
]


def initialise_database(reset=False):
    """
    Creates and seeds the database when needed.

    If reset is True, existing tables are dropped and recreated.
    Otherwise, the existing database is reused if it already exists.
    """
    if reset:
        connection = get_connection()

        drop_tables(connection)
        create_tables(connection)
        seed_data(connection)

        connection.close()

        return

    if database_exists():
        return

    connection = get_connection()

    create_tables(connection)
    seed_data(connection)

    connection.close()


def database_exists():
    return os.path.exists(DB_NAME)


def ensure_data_directory_exists():
    os.makedirs("data", exist_ok=True)


def get_connection():

    ensure_data_directory_exists()

    connection = sqlite3.connect(DB_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def drop_tables(connection):
    connection.execute("DROP TABLE IF EXISTS flights")
    connection.execute("DROP TABLE IF EXISTS pilots")
    connection.execute("DROP TABLE IF EXISTS destinations")
    connection.commit()


def create_tables(connection):
    """
    Creates the application database schema.
    """

    # CHECK constraints enforce key data rules at database level,
    # so invalid data is rejected even if it bypasses application validation.

    # Surrogate integer primary keys are used for relationships,
    # while airport codes and flight numbers are enforced as
    # alternate candidate keys through UNIQUE constraints.
    connection.execute("""
        CREATE TABLE destinations (
            destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
            airport_code TEXT UNIQUE NOT NULL     
                CHECK (
                length(airport_code) = 3
                AND airport_code = upper(airport_code)
            ),
            city TEXT NOT NULL,
            country TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE pilots (
            pilot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL
        )
    """)

    status_values = build_flight_status_check_values()

    # Foreign keys model the relationships between flights,
    # destinations, and pilots. The destination is required,
    # while pilot_id is nullable so flights can be unassigned.

    # Flight status is constrained to the same allowed values used by
    # the application, keeping database integrity aligned with the UI.

    # SQLite stores datetimes as TEXT in this schema.
    # The CHECK constraint enforces the expected storage format,
    # while semantic datetime validation is performed in the
    # application layer using datetime parsing.
    connection.execute(f"""
        CREATE TABLE flights (
            flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_number TEXT UNIQUE NOT NULL,
            destination_id INTEGER NOT NULL,
            pilot_id INTEGER,
            departure_datetime TEXT NOT NULL
                CHECK (
                    departure_datetime GLOB '????-??-?? ??:??'
                ),
            status TEXT NOT NULL
                CHECK (
                    status IN ({status_values})
                ),

            FOREIGN KEY (destination_id)
                REFERENCES destinations(destination_id),

            FOREIGN KEY (pilot_id)
                REFERENCES pilots(pilot_id)
                ON DELETE SET NULL
        )
    """)

    # Enforces one assigned flight per pilot per calendar date.
    # Unassigned flights are allowed because pilot_id can be NULL.
    connection.execute("""
        CREATE UNIQUE INDEX idx_unique_pilot_departure_date
        ON flights(pilot_id, date(departure_datetime))
        WHERE pilot_id IS NOT NULL
    """)

    # Indexes support the main search and reporting queries.
    # Composite indexes are used for the optional flight search
    # filters without creating every possible index combination.
    connection.execute("""
        CREATE INDEX idx_flights_destination_status_departure
        ON flights(destination_id, status, departure_datetime)
    """)

    # Composite indexes are arranged with different left-most columns
    # so the query planner can support different combinations of the
    # optional flight search filters without indexing every permutation.
    connection.execute("""
        CREATE INDEX idx_flights_status_departure_destination
        ON flights(status, departure_datetime, destination_id)
    """)

    # The full departure datetime is indexed so range-based
    # searches can efficiently filter flights by date.
    connection.execute("""
        CREATE INDEX idx_flights_departure_destination_status
        ON flights(departure_datetime, destination_id, status)
    """)

    # Supports pilot schedule lookups and flight counts by pilot.
    connection.execute("""
        CREATE INDEX idx_flights_pilot_id
        ON flights(pilot_id)
    """)

    connection.commit()


def seed_data(connection):
    """
    Seeds the database with sample destinations,
    pilots, and flights.
    """

    seed_destinations(connection)
    seed_pilots(connection, 12)
    seed_flights(connection, 15)


def seed_destinations(connection):
    connection.executemany(
        """
        INSERT INTO destinations (
            airport_code,
            city,
            country
        )
        VALUES (?, ?, ?)
    """,
        AIRPORTS,
    )

    connection.commit()


def seed_pilots(connection, number_of_pilots):
    pilot_data = generate_pilot_data(number_of_pilots)

    connection.executemany(
        """
        INSERT INTO pilots (
            first_name,
            last_name
        )
        VALUES (?, ?)
    """,
        pilot_data,
    )

    connection.commit()


def seed_flights(connection, number_of_flights):
    flight_data = generate_flight_data(number_of_flights)

    connection.executemany(
        """
        INSERT INTO flights (
            flight_number,
            destination_id,
            pilot_id,
            departure_datetime,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """,
        flight_data,
    )

    connection.commit()


def generate_pilot_data(number_of_pilots):
    pilots = []

    for _ in range(number_of_pilots):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)

        pilots.append((first_name, last_name))

    return pilots


def generate_flight_data(number_of_flights):
    flights = []

    # Tracks pilot assignments by calendar date so generated
    # seed data does not violate the unique pilot/date constraint.
    assigned_pilots_by_date = {}

    today = datetime.today().date()
    start_date = today - timedelta(days=2)

    for index in range(number_of_flights):
        flight_number = f"UOB{100 + index}"
        destination_id = random.randint(1, len(AIRPORTS))

        departure_date = start_date + timedelta(days=index // 3)

        departure_time = datetime.min.time().replace(
            hour=6 + (index % 3) * 4,
            minute=0,
        )

        departure_datetime = datetime.combine(
            departure_date,
            departure_time,
        )

        departure_date_key = departure_datetime.strftime(DATE_FORMAT)

        assigned_pilots = assigned_pilots_by_date.setdefault(
            departure_date_key,
            set(),
        )

        available_pilots = [
            pilot_id for pilot_id in range(1, 13) if pilot_id not in assigned_pilots
        ]

        pilot_id = random.choice([None] + available_pilots)

        if pilot_id is not None:
            assigned_pilots.add(pilot_id)

        if departure_date < today:
            available_statuses = [
                "Departed",
                "Cancelled",
            ]
        elif departure_date == today:
            available_statuses = FLIGHT_STATUSES
        else:
            available_statuses = [
                "Scheduled",
                "Cancelled",
            ]

        status = random.choice(available_statuses)

        flights.append(
            (
                flight_number,
                destination_id,
                pilot_id,
                departure_datetime.strftime(DATETIME_FORMAT),
                status,
            )
        )

    return flights


def build_flight_status_check_values():
    """
    Formats the allowed flight statuses into a quoted SQL list
    for the flight status CHECK constraint.
    """
    return ", ".join(f"'{status}'" for status in FLIGHT_STATUSES)
