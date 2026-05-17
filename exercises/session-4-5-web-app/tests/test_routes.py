"""
test_routes.py — integration tests for the Mileage Logbook routes.
"""


def test_list_trips_returns_200(client):
    """GET / returns HTTP 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_list_trips_shows_seeded_trips(client):
    """Trips inserted directly into the DB appear on the list page."""
    import db

    conn = db.get_connection()
    try:
        db.create_trip(
            conn,
            trip_date="2024-04-01",
            vehicle="TX-4801",
            start_location="San Antonio, TX",
            end_location="Houston, TX",
            miles=197.3,
        )
    finally:
        conn.close()

    response = client.get("/")
    assert response.status_code == 200
    assert "TX-4801" in response.text
    assert "San Antonio, TX" in response.text
    assert "Houston, TX" in response.text


def test_create_trip_persists_and_redirects(client):
    """POST /trips saves the trip and redirects to the list."""
    response = client.post(
        "/trips",
        data={
            "trip_date": "2024-04-05",
            "vehicle": "LA-2210",
            "start_location": "Baton Rouge, LA",
            "end_location": "New Orleans, LA",
            "miles": "81.2",
        },
        follow_redirects=False,
    )
    # FastAPI returns 303 See Other for the redirect
    assert response.status_code == 303
    assert response.headers["location"] == "/"

    # Follow the redirect and confirm the trip appears
    list_response = client.get("/")
    assert "LA-2210" in list_response.text
    assert "Baton Rouge, LA" in list_response.text
