# Mileage Logbook

A minimal web app for logging fuel-hauler trips. Built with FastAPI, Jinja2, and SQLite.

This is the starter app for **Hours 8 and 9**. It runs out of the box — your job is to extend it.

**Start with `LAB-GUIDE.md`** in this folder — it walks the Hour 8 build (features F2–F4). Hour 9 continues this *same app* in this folder; the Hour 9 lab guide is in `../hour-09-web-app-frontend-deploy/`.

---

## What it does

- View a list of all trips
- Add a new trip via a form

That's it. Everything else is for you to build.

---

## Setup

### Windows (Git Bash)

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python seed.py
uvicorn main:app --reload
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python seed.py
uvicorn main:app --reload
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## Running the tests

With your virtual environment activated:

```bash
pytest
```

All tests run against a temporary in-memory or temp-file database — no side effects on your `logbook.db`.

---

## Project layout

```
.
├── main.py            # FastAPI app — routes live here
├── db.py              # SQLite helpers (open connection, init schema, queries)
├── seed.py            # Create the DB and insert sample data
├── requirements.txt
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── trips_list.html
│   └── trip_form.html
└── tests/
    ├── conftest.py
    ├── test_routes.py  # HTTP-level tests via TestClient
    └── test_db.py      # Data-layer unit tests
```

---

## Data model

**Trip**

| Field          | Type | Notes                     |
|----------------|------|---------------------------|
| id             | int  | Auto-assigned primary key |
| trip_date      | text | YYYY-MM-DD                |
| vehicle        | text | Fleet ID, e.g. TX-4801    |
| start_location | text | City, State               |
| end_location   | text | City, State               |
| miles          | real | Decimal miles             |

---

## Notes

- The database file (`logbook.db`) is excluded from version control via `.gitignore`. Run `python seed.py` to recreate it at any time.
- There is no authentication, no delete, no edit, no reporting — those are the features you will add in the exercises.
