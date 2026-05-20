import random
import sqlite3
from datetime import datetime, timedelta

DB_NAME = "flight_management.db"

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
    ("JFK", "New York", "United States"),
    ("CDG", "Paris", "France"),
    ("MAD", "Madrid", "Spain"),
    ("FCO", "Rome", "Italy"),
    ("AMS", "Amsterdam", "Netherlands"),
    ("BER", "Berlin", "Germany"),
    ("DXB", "Dubai", "United Arab Emirates"),
    ("HND", "Tokyo", "Japan"),
    ("SYD", "Sydney", "Australia"),
    ("DUB", "Dublin", "Ireland"),
    ("YYZ", "Toronto", "Canada")
]

FLIGHT_STATUSES = [
    "Scheduled",
    "Delayed",
    "Cancelled",
    "Boarding",
    "Departed"
]


def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_database():
    connection = get_connection()

    drop_tables(connection)
    create_tables(connection)
    seed_data(connection)

    connection.close()


def drop_tables(connection):
    connection.execute("DROP TABLE IF EXISTS flights")
    connection.execute("DROP TABLE IF EXISTS pilots")
    connection.execute("DROP TABLE IF EXISTS destinations")
    connection.commit()


def create_tables(connection):
    connection.execute("""
        CREATE TABLE destinations (
            destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
            airport_code TEXT UNIQUE NOT NULL,
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

    connection.execute("""
        CREATE TABLE flights (
            flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_number TEXT UNIQUE NOT NULL,
            destination_id INTEGER NOT NULL,
            pilot_id INTEGER,
            departure_datetime TEXT NOT NULL,
            status TEXT NOT NULL,

            FOREIGN KEY (destination_id)
                REFERENCES destinations(destination_id),

            FOREIGN KEY (pilot_id)
                REFERENCES pilots(pilot_id)
        )
    """)

    connection.commit()


def seed_data(connection):
    random.seed(42)

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
            departure_datetime.strftime("%Y-%m-%d %H:%M"),
            status
        ))

    return flights
