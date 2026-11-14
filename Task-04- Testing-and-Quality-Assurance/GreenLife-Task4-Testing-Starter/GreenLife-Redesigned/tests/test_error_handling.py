import sqlite3
from datetime import date


def test_invalid_route_returns_404(client):
    response = client.get("/unknown-page")

    assert response.status_code == 404


def test_invalid_amount_shows_error_message(client):
    response = client.post("/add", data={
        "activity_type": "Electricity",
        "amount": "abc",
        "activity_date": date.today().isoformat()
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"valid positive amount" in response.data


def test_database_does_not_store_invalid_activity(client, database_path):
    client.post("/add", data={
        "activity_type": "Electricity",
        "amount": "-100",
        "activity_date": date.today().isoformat()
    })

    with sqlite3.connect(database_path) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM activities"
        ).fetchone()[0]

    assert count == 0