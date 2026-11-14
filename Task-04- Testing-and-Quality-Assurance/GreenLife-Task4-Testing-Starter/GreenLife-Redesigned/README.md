# GreenLife – Sustainability Tracker

A Flask and SQLite sustainability dashboard redesigned to follow the supplied Figma Make reference. It tracks electricity and travel activities, estimates CO₂e emissions, and visualises monthly category totals and six-month trends.

## Features
- Dashboard cards populated from SQLite data
- Category-wise doughnut chart and six-month emissions chart
- Add and delete activities
- Input validation for activity type, positive amount, date, and notes
- Responsive sidebar and activity-entry modal
- Recent activity history and sustainability tips

## Run locally
1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. In the terminal, run `python -m pip install -r requirements.txt`.
4. Run `python app.py`.
5. Open `http://127.0.0.1:5000`.

The included `greenlife.db` is the database file supplied with the project, so its existing activity records are retained. Back it up before experimenting with data.

## Emission-factor note
The emission factors in `app.py` are illustrative project assumptions, not official verified factors. They are kept consistent with the original project. Update and cite authoritative factors before presenting the estimates as real-world measurements.

## External assets
Google Fonts (DM Sans) and Chart.js are loaded from their CDNs, so an internet connection is needed for those assets. The dashboard and Flask routes run locally.
