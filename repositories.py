def get_all_flight_details(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            f.flight_number,
            d.city,
            d.country,
            f.departure_datetime,
            f.status,
            p.first_name,
            p.last_name
        FROM flights f
        JOIN destinations d
            ON f.destination_id = d.destination_id
        LEFT JOIN pilots p
            ON f.pilot_id = p.pilot_id
        ORDER BY f.departure_datetime
    """)

    return cursor.fetchall()

def get_flights_by_criteria(connection, destination_id=None, status=None, departure_date=None):
    cursor = connection.cursor()

    query = """
        SELECT
            f.flight_number,
            d.city,
            d.country,
            f.departure_datetime,
            f.status,
            p.first_name,
            p.last_name
        FROM flights f
        JOIN destinations d
            ON f.destination_id = d.destination_id
        LEFT JOIN pilots p
            ON f.pilot_id = p.pilot_id
        WHERE 1 = 1
    """

    params = []

    if destination_id is not None:
        query += " AND f.destination_id = ?"
        params.append(destination_id)

    if status is not None:
        query += " AND f.status = ?"
        params.append(status)

    if departure_date is not None:
        query += " AND DATE(f.departure_datetime) = ?"
        params.append(departure_date)

    query += " ORDER BY f.departure_datetime"

    cursor.execute(query, params)

    return cursor.fetchall()


def count_flights_by_destination(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            d.city,
            d.country,
            COUNT(f.flight_id) AS number_of_flights
        FROM destinations d
        LEFT JOIN flights f
            ON d.destination_id = f.destination_id
        GROUP BY d.destination_id
        ORDER BY number_of_flights DESC
    """)

    return cursor.fetchall()

def count_flights_by_pilot(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            p.first_name,
            p.last_name,
            COUNT(f.flight_id) AS number_of_flights
        FROM pilots p
        LEFT JOIN flights f
            ON p.pilot_id = f.pilot_id
        GROUP BY p.pilot_id
        ORDER BY number_of_flights DESC
    """)

    return cursor.fetchall()

def add_flight(
    connection,
    flight_number,
    destination_id,
    departure_datetime,
    status,
    pilot_id=None,
):
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO flights (
            flight_number,
            destination_id,
            pilot_id,
            departure_datetime,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        flight_number,
        destination_id,
        pilot_id,
        departure_datetime,
        status,
    ))

    connection.commit()

    return cursor.lastrowid

def add_destination(
    connection,
    airport_code,
    city,
    country,
):
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO destinations (
            airport_code,
            city,
            country
        )
        VALUES (?, ?, ?)
    """, (
        airport_code,
        city,
        country,
    ))

    connection.commit()

    return cursor.lastrowid

def get_all_pilots(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            pilot_id,
            first_name,
            last_name
        FROM pilots
        ORDER BY pilot_id
    """)

    return cursor.fetchall()

def get_all_destinations_by_airport_code(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            airport_code,
            city,
            country,
            destination_id
        FROM destinations
        ORDER BY airport_code
    """)

    return cursor.fetchall()

def get_flights_by_pilot_id(connection, pilot_id):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            f.flight_number,
            d.city,
            d.country,
            f.departure_datetime,
            f.status,
            p.first_name,
            p.last_name
        FROM flights f
        JOIN destinations d
            ON f.destination_id = d.destination_id
        JOIN pilots p
            ON f.pilot_id = p.pilot_id
        WHERE p.pilot_id = ?
        ORDER BY f.departure_datetime
    """, (pilot_id,))

    return cursor.fetchall()


def get_all_flights_for_selection(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            flight_id,
            flight_number,
            departure_datetime,
            status
        FROM flights
        ORDER BY flight_id
    """)

    return cursor.fetchall()


def update_flight_status(connection, flight_id, status):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE flights
        SET status = ?
        WHERE flight_id = ?
    """, (status, flight_id))

    connection.commit()

    return cursor.rowcount


def update_flight_departure_datetime(
    connection,
    flight_id,
    departure_datetime,
):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE flights
        SET departure_datetime = ?
        WHERE flight_id = ?
    """, (departure_datetime, flight_id))

    connection.commit()

    return cursor.rowcount


def delete_flight(connection, flight_id):
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM flights
        WHERE flight_id = ?
    """, (flight_id,))

    connection.commit()

    return cursor.rowcount


def assign_pilot_to_flight(connection, flight_id, pilot_id):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE flights
        SET pilot_id = ?
        WHERE flight_id = ?
    """, (pilot_id, flight_id))

    connection.commit()

    return cursor.rowcount


def update_destination_airport_code(connection, destination_id, airport_code):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE destinations
        SET airport_code = ?
        WHERE destination_id = ?
    """, (airport_code, destination_id))

    connection.commit()

    return cursor.rowcount


def update_destination_city(connection, destination_id, city):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE destinations
        SET city = ?
        WHERE destination_id = ?
    """, (city, destination_id))

    connection.commit()

    return cursor.rowcount


def update_destination_country(connection, destination_id, country):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE destinations
        SET country = ?
        WHERE destination_id = ?
    """, (country, destination_id))

    connection.commit()

    return cursor.rowcount


def airport_code_exists_for_other_destination(connection, airport_code, destination_id):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 1
        FROM destinations
        WHERE airport_code = ?
          AND destination_id != ?
    """, (airport_code, destination_id))

    return cursor.fetchone() is not None