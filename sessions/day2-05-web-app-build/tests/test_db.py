"""
test_db.py — unit tests for the db module (data layer).
"""

import pytest
import db


def test_create_and_retrieve_trip(mem_conn):
    """A trip inserted via create_trip can be retrieved via get_all_trips."""
    db.create_trip(
        mem_conn,
        trip_date="2024-04-09",
        vehicle="TX-4801",
        start_location="Dallas, TX",
        end_location="Lubbock, TX",
        miles=320.4,
    )
    trips = db.get_all_trips(mem_conn)
    assert len(trips) == 1
    trip = trips[0]
    assert trip["vehicle"] == "TX-4801"
    assert trip["start_location"] == "Dallas, TX"
    assert trip["end_location"] == "Lubbock, TX"
    assert trip["miles"] == pytest.approx(320.4)
