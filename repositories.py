def view_all_flights(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            f.flight_id,
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

def get_flights_by_criteria(connection, destination_city=None, status=None, departure_date=None):
    cursor = connection.cursor()

    query = """
        SELECT
            f.flight_id,
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

    if destination_city:
        query += " AND d.city LIKE ?"
        params.append(f"%{destination_city}%")

    if status:
        query += " AND f.status = ?"
        params.append(status)

    if departure_date:
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