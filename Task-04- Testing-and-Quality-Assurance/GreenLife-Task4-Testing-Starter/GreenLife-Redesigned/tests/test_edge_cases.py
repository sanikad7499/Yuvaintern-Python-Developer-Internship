import sqlite3
from datetime import date


def test_missing_amount_is_rejected(client, database_path):

    response = client.post("/add", data={
        "activity_type": "Electricity",
        "amount": "",
        "activity_date": date.today().isoformat()
    }, follow_redirects=True)

    assert response.status_code == 200

    with sqlite3.connect(database_path) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM activities"
        ).fetchone()[0]

    assert count == 0


def test_missing_activity_date_is_rejected(client, database_path):

    response = client.post("/add", data={
        "activity_type": "Car",
        "amount": "10",
        "activity_date": ""
    }, follow_redirects=True)

    assert response.status_code == 200

    with sqlite3.connect(database_path) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM activities"
        ).fetchone()[0]

    assert count == 0