from datetime import date, timedelta
import sqlite3

import pytest
import app as greenlife_app


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"GreenLife" in response.data


def test_emission_calculation_for_electricity():
    assert greenlife_app.calculate_emissions("Electricity", 10) == 7.0


def test_emission_calculation_for_car():
    assert greenlife_app.calculate_emissions("Car", 20) == 3.6


def test_previous_months_returns_requested_count():
    months = greenlife_app.previous_months(date(2026, 11, 11), 6)
    assert len(months) == 6
    assert months[-1] == date(2026, 11, 1)


def test_add_valid_activity_is_saved(client, database_path):
    response = client.post("/add", data={
        "activity_type": "Electricity",
        "amount": "10",
        "activity_date": date.today().isoformat(),
        "notes": "Unit test activity",
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Activity added successfully" in response.data
    with sqlite3.connect(database_path) as connection:
        row = connection.execute(
            "SELECT activity_type, amount, co2_kg FROM activities"
        ).fetchone()
    assert row == ("Electricity", 10.0, 7.0)


@pytest.mark.parametrize("amount", ["", "abc", "0", "-5", "nan", "inf"])
def test_invalid_amount_is_rejected(client, database_path, amount):
    response = client.post("/add", data={
        "activity_type": "Electricity",
        "amount": amount,
        "activity_date": date.today().isoformat(),
        "notes": "Invalid amount test",
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"valid positive amount" in response.data
    with sqlite3.connect(database_path) as connection:
        count = connection.execute("SELECT COUNT(*) FROM activities").fetchone()[0]
    assert count == 0


def test_invalid_activity_category_is_rejected(client, database_path):
    response = client.post("/add", data={
        "activity_type": "Rocket",
        "amount": "10",
        "activity_date": date.today().isoformat(),
    }, follow_redirects=True)
    assert b"select a valid activity" in response.data.lower()
    with sqlite3.connect(database_path) as connection:
        assert connection.execute("SELECT COUNT(*) FROM activities").fetchone()[0] == 0


def test_future_date_is_rejected(client, database_path):
    future_date = (date.today() + timedelta(days=1)).isoformat()
    response = client.post("/add", data={
        "activity_type": "Car",
        "amount": "5",
        "activity_date": future_date,
    }, follow_redirects=True)
    assert b"Future dates are not allowed" in response.data
    with sqlite3.connect(database_path) as connection:
        assert connection.execute("SELECT COUNT(*) FROM activities").fetchone()[0] == 0


def test_notes_over_200_characters_are_rejected(client, database_path):
    response = client.post("/add", data={
        "activity_type": "Bus",
        "amount": "5",
        "activity_date": date.today().isoformat(),
        "notes": "x" * 201,
    }, follow_redirects=True)
    assert b"must not exceed 200 characters" in response.data
    with sqlite3.connect(database_path) as connection:
        assert connection.execute("SELECT COUNT(*) FROM activities").fetchone()[0] == 0


def test_delete_existing_activity(client, database_path):
    with sqlite3.connect(database_path) as connection:
        cursor = connection.execute(
            "INSERT INTO activities (activity_type, amount, activity_date, notes, co2_kg) VALUES (?, ?, ?, ?, ?)",
            ("Car", 10, date.today().isoformat(), "Delete test", 1.8),
        )
        activity_id = cursor.lastrowid

    response = client.post(f"/delete/{activity_id}", follow_redirects=True)
    assert b"Activity deleted successfully" in response.data
    with sqlite3.connect(database_path) as connection:
        assert connection.execute("SELECT COUNT(*) FROM activities").fetchone()[0] == 0


def test_delete_nonexistent_activity(client):
    response = client.post("/delete/99999", follow_redirects=True)
    assert b"Activity not found" in response.data
