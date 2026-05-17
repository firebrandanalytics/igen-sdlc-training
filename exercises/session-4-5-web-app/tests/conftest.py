"""
conftest.py — pytest fixtures for the Mileage Logbook tests.

Each test gets its own isolated SQLite database so tests don't interfere
with each other and there are no leftover files after the suite finishes.
"""

import sqlite3

import pytest
from fastapi.testclient import TestClient

import db


@pytest.fixture
def mem_conn():
    """In-memory SQLite connection with the schema initialised."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    db.init_db(conn)
    yield conn
    conn.close()


@pytest.fixture
def client(tmp_path, monkeypatch):
    """
    TestClient backed by a temp-file database.

    Using tmp_path (not :memory:) because each route handler opens its own
    connection via db.get_connection(), so all calls must hit the same file.
    monkeypatch swaps DB_PATH before the app is imported to ensure the
    lifespan startup and the route handlers all use the temp file.
    """
    db_file = str(tmp_path / "test_logbook.db")
    monkeypatch.setattr(db, "DB_PATH", db_file)

    from main import app

    with TestClient(app, raise_server_exceptions=True) as c:
        yield c
