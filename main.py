import sys

from cli.app import run_cli
from database import (
    get_connection,
    initialise_database,
)


def main():
    reset = "--reset" in sys.argv

    initialise_database(reset=reset)

    connection = get_connection()

    try:
        run_cli(connection)
    finally:
        connection.close()


if __name__ == "__main__":
    main()