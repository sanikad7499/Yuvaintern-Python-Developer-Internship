import sqlite3
from datetime import date


def add_activity(client, activity_type, amount, notes):
    """Helper function to add an activity through Flask."""

    return client.post("/add", data={
        "activity_type": activity_type,
        "amount": str(amount),
        "activity_date": date.today().isoformat(),
        "notes": notes
    }, follow_redirects=True)


def test_activity_is_saved_and_displayed_on_dashboard(client, database_path):

    response = add_activity(
        client, "Electricity", 10, "Integration electricity test"
    )

    assert response.status_code == 200
    assert b"Integration electricity test" in response.data
    assert b"7.00" in response.data

    with sqlite3.connect(database_path) as connection:
        record = connection.execute(
            "SELECT activity_type, amount, co2_kg FROM activities"
        ).fetchone()

    assert record == ("Electricity", 10.0, 7.0)


def test_dashboard_calculates_multiple_activities(client):

    add_activity(client, "Electricity", 10, "Electricity usage")
    add_activity(client, "Car", 20, "Car travel")

    response = client.get("/")

    assert response.status_code == 200

    # Electricity: 10 x 0.70 = 7.00
    # Car: 20 x 0.18 = 3.60
    # Total emissions = 10.60

    assert b"10.60" in response.data
    assert b"2" in response.data
    assert b"10.00" in response.data
    assert b"3.60" in response.data


def test_activity_history_updates_after_new_record(client):

    add_activity(client, "Bus", 15, "Bus integration test")

    response = client.get("/")

    assert b"Bus integration test" in response.data
    assert b"Bus" in response.data


def test_deleted_activity_disappears_from_dashboard(client, database_path):

    add_activity(client, "Car", 10, "Activity to delete")

    with sqlite3.connect(database_path) as connection:
        activity_id = connection.execute(
            "SELECT id FROM activities"
        ).fetchone()[0]

    response = client.post(
        f"/delete/{activity_id}",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Activity deleted successfully" in response.data
    assert b"Activity to delete" not in response.data

    with sqlite3.connect(database_path) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM activities"
        ).fetchone()[0]

    assert count == 0