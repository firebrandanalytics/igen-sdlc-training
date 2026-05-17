"""
db.py — thin database helpers for the Mileage Logbook.

Opens a SQLite connection and provides two small helpers used by the routes.
Query logic lives here rather than in main.py so routes stay readable, but
there is no service layer or repository abstraction — that comes later.
"""

import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", "logbook.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection | None = None) -> None:
    """Create the trips table if it doesn't exist."""
    close_after = conn is None
    if conn is None:
        conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS trips (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_date      TEXT    NOT NULL,
            vehicle        TEXT    NOT NULL,
            start_location TEXT    NOT NULL,
            end_location   TEXT    NOT NULL,
            miles          REAL    NOT NULL
        )
        """
    )
    conn.commit()
    if close_after:
        conn.close()


def get_all_trips(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    cursor = conn.execute(
        "SELECT * FROM trips ORDER BY trip_date DESC, id DESC"
    )
    return cursor.fetchall()


def create_trip(
    conn: sqlite3.Connection,
    trip_date: str,
    vehicle: str,
    start_location: str,
    end_location: str,
    miles: float,
) -> int:
    cursor = conn.execute(
        """
        INSERT INTO trips (trip_date, vehicle, start_location, end_location, miles)
        VALUES (?, ?, ?, ?, ?)
        """,
        (trip_date, vehicle, start_location, end_location, miles),
    )
    conn.commit()
    return cursor.lastrowid
