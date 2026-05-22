"""
Shared application constants and configuration values.

This module defines reusable values such as database
settings, date formats, and valid flight statuses.
"""

DB_NAME = "flight_management.db"

DATETIME_FORMAT = "%Y-%m-%d %H:%M"
DATE_FORMAT = "%Y-%m-%d"

FLIGHT_STATUSES = [
    "Scheduled",
    "Delayed",
    "Cancelled",
    "Boarding",
    "Departed",
]