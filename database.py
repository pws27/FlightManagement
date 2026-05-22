"""
Database setup and seed data for the flight management system.

This module creates the SQLite schema, opens database connections,
and inserts sample data used by the CLI application.
"""

import random
import sqlite3
import os
from datetime import datetime, timedelta
from constants import DB_NAME, DATETIME_FORMAT, FLIGHT_STATUSES

FIRST_NAMES = [
    "Peter", "Julie", "Hamish", "Terry", "Joy",
    "Grant", "Kyron", "Brooke", "Paul", "Johnny",
    "Harry", "William", "Thomas", "Keren", "Carrie"
]

LAST_NAMES = [
    "Somerville", "Amphlett", "Brice", "Harper", "Wilson",
    "Smith", "Cobain", "Thompson", "McGalloway", "Simpson",
    "Young", "Christie", "Carmichael", "Strang", "Jameson"
]

AIRPORTS = [
    ("LHR", "London", "United Kingdom"),
    ("MAN", "Manchester", "United Kingdom"),
    ("EDI", "Edinburgh", "United Kingdom"),
    ("JFK", "New York", "United States"),
    ("LAX", "Los Angeles", "United States"),
    ("ORD", "Chicago", "United States"),
    ("CDG", "Paris", "France"),
    ("NCE", "Nice", "France"),
    ("MAD", "Madrid", "Spain"),
    ("BCN", "Barcelona", "Spain"),
    ("FCO", "Rome", "Italy"),
    ("MXP", "Milan", "Italy"),
    ("AMS", "Amsterdam", "Netherlands"),
    ("BER", "Berlin", "Germany"),
    ("MUC", "Munich", "Germany"),
    ("DXB", "Dubai", "United Arab Emirates"),
    ("HND", "Tokyo", "Japan"),
    ("KIX", "Osaka", "Japan"),
    ("SYD", "Sydney", "Australia"),
    ("MEL", "Melbourne", "Australia"),
    ("DUB", "Dublin", "Ireland"),
    ("YYZ", "Toronto", "Canada"),
    ("YVR", "Vancouver", "Canada"),
    ("GRU", "Sao Paulo", "Brazil"),
    ("ARN", "Stockholm", "Sweden"),
    ("SIN", "Singapore", "Singapore")
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


def get_connection():
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

    status_values = to_sql_text_list(FLIGHT_STATUSES)

    connection.execute(f"""
        CREATE TABLE flights (
            flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_number TEXT UNIQUE NOT NULL,
            destination_id INTEGER NOT NULL,
            pilot_id INTEGER,
            departure_datetime TEXT NOT NULL,

            status TEXT NOT NULL
                CHECK (
                    status IN ({status_values})
                ),

            FOREIGN KEY (destination_id)
                REFERENCES destinations(destination_id),

            FOREIGN KEY (pilot_id)
                REFERENCES pilots(pilot_id)
        )
    """)

    connection.commit()


def seed_data(connection):
    """
    Seeds the database with sample destinations,
    pilots, and flights.
    """

    random.seed(42) # comment out for non-deterministic data...

    seed_destinations(connection)
    seed_pilots(connection, 12)
    seed_flights(connection, 15)


def seed_destinations(connection):
    connection.executemany("""
        INSERT INTO destinations (
            airport_code,
            city,
            country
        )
        VALUES (?, ?, ?)
    """, AIRPORTS)

    connection.commit()


def seed_pilots(connection, number_of_pilots):
    pilot_data = generate_pilot_data(number_of_pilots)

    connection.executemany("""
        INSERT INTO pilots (
            first_name,
            last_name
        )
        VALUES (?, ?)
    """, pilot_data)

    connection.commit()


def seed_flights(connection, number_of_flights):
    flight_data = generate_flight_data(number_of_flights)

    connection.executemany("""
        INSERT INTO flights (
            flight_number,
            destination_id,
            pilot_id,
            departure_datetime,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, flight_data)

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

    start_datetime = datetime(2026, 6, 1, 6, 0)

    for index in range(number_of_flights):
        flight_number = f"UOB{100 + index}"
        destination_id = random.randint(1, len(AIRPORTS))
        pilot_id = random.choice([None] + list(range(1, 13)))

        departure_datetime = start_datetime + timedelta(hours=index * 3)
        status = random.choice(FLIGHT_STATUSES)

        flights.append((
            flight_number,
            destination_id,
            pilot_id,
            departure_datetime.strftime(DATETIME_FORMAT),
            status
        ))

    return flights


def to_sql_text_list(values):
    return ", ".join(
        f"'{value}'"
        for value in values
    )