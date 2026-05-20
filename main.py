from database import create_database, get_connection
from menu import run_menu

def main():
    create_database()
    print("Database created and seeded successfully.")

    connection = get_connection()
    run_menu(connection)
    connection.close()

    print("Database connection closed")

if __name__ == "__main__":
    main()
