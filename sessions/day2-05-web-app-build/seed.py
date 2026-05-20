"""
seed.py — create the SQLite database and insert sample trip data.

Run once before starting the app for the first time:
    python seed.py

Safe to re-run: drops and recreates the trips table each time.
"""

import db

SAMPLE_TRIPS = [
    ("2024-04-01", "TX-4801", "San Antonio, TX", "Houston, TX", 197.3),
    ("2024-04-02", "TX-4805", "Houston, TX", "Beaumont, TX", 85.4),
    ("2024-04-03", "TX-4801", "Houston, TX", "Dallas, TX", 239.6),
    ("2024-04-04", "LA-2210", "Baton Rouge, LA", "New Orleans, LA", 81.2),
    ("2024-04-05", "TX-4812", "Dallas, TX", "Amarillo, TX", 362.1),
    ("2024-04-07", "TX-4805", "Beaumont, TX", "Port Arthur, TX", 17.8),
    ("2024-04-08", "LA-2210", "New Orleans, LA", "Lake Charles, LA", 203.5),
    ("2024-04-09", "TX-4801", "Dallas, TX", "Lubbock, TX", 320.4),
    ("2024-04-10", "TX-4812", "Amarillo, TX", "Oklahoma City, OK", 261.7),
    ("2024-04-11", "LA-2215", "Shreveport, LA", "Jackson, MS", 188.9),
]


def seed():
    conn = db.get_connection()
    try:
        conn.execute("DROP TABLE IF EXISTS trips")
        db.init_db(conn)
        conn.executemany(
            """
            INSERT INTO trips (trip_date, vehicle, start_location, end_location, miles)
            VALUES (?, ?, ?, ?, ?)
            """,
            SAMPLE_TRIPS,
        )
        conn.commit()
        print(f"Seeded {len(SAMPLE_TRIPS)} trips into {db.DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    seed()
