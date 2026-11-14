from datetime import date


def test_dashboard_opens_successfully(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"GreenLife" in response.data


def test_dashboard_returns_html(client):
    response = client.get("/")
    assert response.content_type.startswith("text/html")


def test_multiple_activities_can_be_added(client):
    activities = [
        ("Electricity", "10"),
        ("Car", "20"),
        ("Bus", "15")
    ]

    for activity, amount in activities:
        response = client.post("/add", data={
            "activity_type": activity,
            "amount": amount,
            "activity_date": date.today().isoformat(),
            "notes": "System testing"
        }, follow_redirects=True)

        assert response.status_code == 200


def test_invalid_input_does_not_crash_application(client):
    response = client.post("/add", data={
        "activity_type": "Electricity",
        "amount": "invalid",
        "activity_date": date.today().isoformat()
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"valid positive amount" in response.data


def test_invalid_url_returns_404(client):
    response = client.get("/invalid-page")
    assert response.status_code == 404


def test_dashboard_remains_available_after_operations(client):
    client.post("/add", data={
        "activity_type": "Electricity",
        "amount": "10",
        "activity_date": date.today().isoformat(),
        "notes": "System test"
    })

    response = client.get("/")

    assert response.status_code == 200
    assert b"GreenLife" in response.data