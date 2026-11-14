import time
import statistics
from datetime import date


def test_dashboard_response_time(client):

    response_times = []

    for _ in range(30):
        start = time.perf_counter()

        response = client.get("/")

        end = time.perf_counter()

        assert response.status_code == 200

        response_times.append((end - start) * 1000)

    average = statistics.mean(response_times)
    median = statistics.median(response_times)

    print(f"\nDashboard Average: {average:.2f} ms")
    print(f"Dashboard Median: {median:.2f} ms")


def test_activity_insertion_response_time(client):

    response_times = []

    for i in range(10):
        start = time.perf_counter()

        response = client.post("/add", data={
            "activity_type": "Electricity",
            "amount": "10",
            "activity_date": date.today().isoformat(),
            "notes": f"Performance test {i}"
        })

        end = time.perf_counter()

        assert response.status_code in (200, 302)

        response_times.append((end - start) * 1000)

    average = statistics.mean(response_times)

    print(f"\nActivity Insertion Average: {average:.2f} ms")


def test_dashboard_with_multiple_records(client):

    for i in range(50):
        client.post("/add", data={
            "activity_type": "Car",
            "amount": "5",
            "activity_date": date.today().isoformat(),
            "notes": f"Record {i}"
        })

    start = time.perf_counter()

    response = client.get("/")

    end = time.perf_counter()

    response_time = (end - start) * 1000

    assert response.status_code == 200

    print(f"\nDashboard with 50 records: {response_time:.2f} ms")