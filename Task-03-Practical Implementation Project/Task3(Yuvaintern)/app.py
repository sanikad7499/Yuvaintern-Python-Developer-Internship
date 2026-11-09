from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
import math
from datetime import date

app = Flask(__name__)
app.secret_key = "greenlife-local-development-key"
DATABASE = os.path.join(app.root_path, "greenlife.db")

# Illustrative project assumptions, not official verified emission factors.
EMISSION_FACTORS = {
    "Electricity": 0.70,  # kg CO2e per kWh
    "Car": 0.18,          # kg CO2e per km
    "Two Wheeler": 0.10,  # kg CO2e per km
    "Bus": 0.08,          # kg CO2e per km
    "Train": 0.04         # kg CO2e per km
}
TRAVEL_TYPES = ("Car", "Two Wheeler", "Bus", "Train")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                activity_type TEXT NOT NULL,
                amount REAL NOT NULL,
                activity_date TEXT NOT NULL,
                notes TEXT,
                co2_kg REAL NOT NULL
            )
        """)


def calculate_emissions(activity_type, amount):
    return round(amount * EMISSION_FACTORS[activity_type], 2)


def previous_months(today, count=6):
    """Return the first day of each month, oldest first, including this month."""
    year, month = today.year, today.month
    result = []
    for offset in reversed(range(count)):
        index = year * 12 + month - 1 - offset
        y, m0 = divmod(index, 12)
        result.append(date(y, m0 + 1, 1))
    return result


@app.route("/")
def index():
    today = date.today()
    month_start = today.replace(day=1).isoformat()
    if today.month == 12:
        next_month = date(today.year + 1, 1, 1)
    else:
        next_month = date(today.year, today.month + 1, 1)
    month_end = next_month.isoformat()

    with get_db() as conn:
        monthly_total = conn.execute("""
            SELECT COALESCE(SUM(co2_kg), 0) FROM activities
            WHERE activity_date >= ? AND activity_date < ?
        """, (month_start, month_end)).fetchone()[0]

        total_activities = conn.execute(
            "SELECT COUNT(*) FROM activities"
        ).fetchone()[0]

        categories = conn.execute("""
            SELECT activity_type, SUM(co2_kg) AS total
            FROM activities
            WHERE activity_date >= ? AND activity_date < ?
            GROUP BY activity_type ORDER BY total DESC
        """, (month_start, month_end)).fetchall()

        electricity_usage = conn.execute("""
            SELECT COALESCE(SUM(amount), 0) FROM activities
            WHERE activity_type = 'Electricity'
              AND activity_date >= ? AND activity_date < ?
        """, (month_start, month_end)).fetchone()[0]

        travel_emissions = conn.execute("""
            SELECT COALESCE(SUM(co2_kg), 0) FROM activities
            WHERE activity_type IN ('Car', 'Two Wheeler', 'Bus', 'Train')
              AND activity_date >= ? AND activity_date < ?
        """, (month_start, month_end)).fetchone()[0]

        activities = conn.execute("""
            SELECT * FROM activities
            ORDER BY activity_date DESC, id DESC LIMIT 10
        """).fetchall()

        # Monthly totals for the last six calendar months.
        months = previous_months(today, 6)
        trend_labels = []
        trend_values = []
        for month_date in months:
            if month_date.month == 12:
                end_date = date(month_date.year + 1, 1, 1)
            else:
                end_date = date(month_date.year, month_date.month + 1, 1)
            total = conn.execute("""
                SELECT COALESCE(SUM(co2_kg), 0) FROM activities
                WHERE activity_date >= ? AND activity_date < ?
            """, (month_date.isoformat(), end_date.isoformat())).fetchone()[0]
            trend_labels.append(month_date.strftime("%b"))
            trend_values.append(round(total, 2))

    labels = [row["activity_type"] for row in categories]
    values = [round(row["total"], 2) for row in categories]

    return render_template(
        "index.html",
        today=today.isoformat(),
        month_label=today.strftime("%B %Y"),
        monthly_total=round(monthly_total, 2),
        total_activities=total_activities,
        electricity_usage=round(electricity_usage, 2),
        travel_emissions=round(travel_emissions, 2),
        activities=activities,
        labels=labels,
        values=values,
        trend_labels=trend_labels,
        trend_values=trend_values,
        factors=EMISSION_FACTORS,
    )


@app.route("/add", methods=["POST"])
def add_activity():
    activity_type = request.form.get("activity_type", "")
    amount_text = request.form.get("amount", "")
    activity_date = request.form.get("activity_date", "")
    notes = request.form.get("notes", "").strip()

    if activity_type not in EMISSION_FACTORS:
        flash("Please select a valid activity.", "error")
        return redirect(url_for("index"))

    try:
        amount = float(amount_text)
        if not math.isfinite(amount) or amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        flash("Please enter a valid positive amount.", "error")
        return redirect(url_for("index"))

    try:
        selected_date = date.fromisoformat(activity_date)
        if selected_date > date.today():
            flash("Future dates are not allowed.", "error")
            return redirect(url_for("index"))
    except (ValueError, TypeError):
        flash("Please enter a valid date.", "error")
        return redirect(url_for("index"))

    if len(notes) > 200:
        flash("Notes must not exceed 200 characters.", "error")
        return redirect(url_for("index"))

    co2 = calculate_emissions(activity_type, amount)
    with get_db() as conn:
        conn.execute("""
            INSERT INTO activities
            (activity_type, amount, activity_date, notes, co2_kg)
            VALUES (?, ?, ?, ?, ?)
        """, (activity_type, amount, activity_date, notes, co2))

    flash("Activity added successfully!", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:activity_id>", methods=["POST"])
def delete_activity(activity_id):
    with get_db() as conn:
        cursor = conn.execute(
            "DELETE FROM activities WHERE id = ?", (activity_id,)
        )
    if cursor.rowcount:
        flash("Activity deleted successfully.", "success")
    else:
        flash("Activity not found.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
