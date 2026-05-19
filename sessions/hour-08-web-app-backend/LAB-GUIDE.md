# Lab Guide: Mileage Logbook — Hour 8 (Backend)

iGEN Developer AI Training · Hour 8

---

## What You Are Building

You are extending the Mileage Logbook starter — a minimal FastAPI + SQLite + Jinja2
app that can already list and create trips. In Hour 8 you add the three backend
features (F2–F4) by directing Claude Code through a structured build. Hour 9
continues the *same app* with F5–F8 — that lab guide is in
`../hour-09-web-app-frontend-deploy/LAB-GUIDE.md`.

Read the starter app's `README.md` before you do anything else. It describes the
data model, project layout, and how to run the existing tests.

**Time:** approximately 50 minutes.

---

## Environment Setup

Do this once, before any Claude Code sessions. Run from the repo root.

### Windows (Git Bash)

```bash
cd sessions/hour-08-web-app-backend
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python seed.py
uvicorn main:app --reload
```

### macOS / Linux

```bash
cd sessions/hour-08-web-app-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python seed.py
uvicorn main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) and confirm you see a table of
trips. The app starts with no CLAUDE.md — you will write one as part of the
exercise.

**Verify the starter tests pass before you add anything:**

```bash
pytest -v
```

Expected: 4 tests pass, 0 failures. If any fail, the environment is not set up
correctly — do not proceed until they pass.

---

## A Note on Approach

Each feature below is a vertical slice: route, data layer, template, tests. Direct
Claude Code to handle the whole slice at once — this is the agentic loop in
practice, not tab-completing one file at a time.

**The review discipline:** before each `pytest` run, read the diff. Claude Code
occasionally adds an import it doesn't need, renames something that was already
named consistently, or writes a test that doesn't actually exercise the code path it
claims to. These are the things the C10 rubric is for.

---

## Warm-Up — Write a CLAUDE.md

Before directing Claude Code to write any feature code, give it the context it
needs to operate in this project. Open a Claude Code session in this folder
(`sessions/hour-08-web-app-backend/`) and ask it to write a `CLAUDE.md` that covers:

- Project purpose and stack (FastAPI, SQLite, Jinja2, Python 3.10+)
- The existing module layout (main.py, db.py, seed.py, templates/, tests/)
- Testing convention (pytest; `client` fixture in `tests/conftest.py` provides a
  TestClient backed by a temp database; do not use the live `logbook.db`)
- Style conventions you care about (e.g. "query logic lives in db.py, not in route
  handlers")

This takes 5–10 minutes. A good CLAUDE.md is the difference between an agent that
guesses at your conventions and one that follows them consistently.

---

## F2 — Delete a Trip

**Goal:** `POST /trips/{id}/delete` removes the trip and redirects to `/`.

**What this teaches:** a complete vertical slice — data layer helper, route, and
template change — directed as a single Claude Code task. This is the pattern you
will repeat for F3 and F4.

**Direct Claude Code to:**
- Add `delete_trip(conn, trip_id)` to `db.py`
- Add the `POST /trips/{trip_id}/delete` route to `main.py`
- Add a Delete button (or link-as-form) to the trips list template

**Spec the task with C7 (or give a direct instruction):**
> "Files to read first: `main.py`, `db.py`, `templates/trips_list.html`. Files to
> modify: `db.py` (add delete_trip), `main.py` (add delete route), `trips_list.html`
> (add delete button). Do not add authentication or confirmation dialogs."

**Verify:**
```bash
pytest -v
```

Also manually: add a trip via the form, delete it, confirm it disappears from the list.

> **If the delete button submits a GET instead of a POST:** HTML forms only support
> GET and POST. The route uses POST. Make sure the template uses `method="post"` and
> wraps the button in a `<form>` tag.

**Checkpoint H8-1:** `pytest -v` passes; trips can be deleted via the browser.

---

## F3 — Edit a Trip

**Goal:** `GET /trips/{id}/edit` shows a pre-filled form; `POST /trips/{id}/edit`
saves changes and redirects.

**What this teaches:** reusing the existing add-trip pattern. The trip form template
already handles validation errors — F3 should extend it rather than duplicate it.

**Direct Claude Code to:**
- Add `get_trip(conn, trip_id)` and `update_trip(conn, trip_id, ...)` to `db.py`
- Add the GET and POST `/trips/{trip_id}/edit` routes to `main.py`
- Extend `trip_form.html` so that when a `trip` object is passed in, form fields are
  pre-populated

**Review prompt for Claude Code:** "The add-trip route in `main.py` and the
`trip_form.html` template already handle form validation. F3 should reuse that form
template, not create a new one. Please read both before writing anything."

**Verify:**
```bash
pytest -v
```

Manual check: edit an existing trip; change the vehicle field; confirm the change
appears in the list. Also verify that an edit with invalid data (e.g. empty vehicle)
shows the form again with an error message — not a 500.

> **If the edit form shows blank fields instead of the trip's current values:**
> the template is not receiving the `trip` object, or the field `value` attributes
> are not wired up. Ask Claude Code to check what context variables the route passes
> to the template.

**Checkpoint H8-2:** `pytest -v` passes; trips can be edited via the browser.

---

## F4 — Per-Jurisdiction Miles

**Goal:** Add a `trip_jurisdictions` table so each trip can record how many miles
were driven in each US state. This is the schema that makes F5 possible.

**What this teaches:** schema changes ripple — model, data layer, route, template,
tests all need updating when the data model grows.

**Direct Claude Code to:**
- Add the `trip_jurisdictions` table to `db.init_db()` in `db.py`. Schema:
  `(id, trip_id FK → trips, state_code TEXT, miles REAL, UNIQUE(trip_id, state_code))`
- Add `get_trip_jurisdictions(conn, trip_id)` and
  `set_trip_jurisdictions(conn, trip_id, jurisdiction_miles: dict[str, float])` to
  `db.py`
- Update the trip form to include optional `state_<CODE>` input fields for
  at least 3 states (e.g. `state_TX`, `state_OK`, `state_IL`) that the create and
  edit routes will read and persist
- Update `create_trip` and `update_trip` routes to call `set_trip_jurisdictions`
  with whatever state miles are present in the form

**Anti-goal to include in your prompt:** "Do not require jurisdiction miles — they
are optional per trip. A trip with no jurisdiction fields is still valid."

**Verify:**
```bash
pytest -v
```

Manual check: create a trip, enter miles for two states, save, edit that trip, and
confirm the state miles are pre-filled.

> **If the existing tests fail after adding the new table:** `db.init_db()` uses
> `CREATE TABLE IF NOT EXISTS`, so the new table should not break existing behaviour.
> If tests fail, check that `init_db()` was not accidentally changed to drop and
> recreate existing tables.

**Checkpoint H8-3:** `pytest -v` passes; jurisdiction miles are stored and retrievable.

---

## Hour 8 Complete — End-State Check

```bash
pytest -v
```

Expected: all tests pass. Then verify in the browser:

- [ ] Delete button removes a trip from the list
- [ ] Edit form pre-fills the existing data and saves changes
- [ ] A trip can record miles for individual states, saved and shown again on edit

If any of these are missing, fix them before Hour 9.

When all three pass, continue with the **Hour 9 lab guide** in
`../hour-09-web-app-frontend-deploy/LAB-GUIDE.md` — you keep working in this same
folder, with the code, database, and CLAUDE.md you produced here.

---

## Appendix — Quick Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `uvicorn: command not found` | venv not activated | `source venv/Scripts/activate` (Windows) or `source venv/bin/activate` (macOS/Linux) |
| `pytest` fails with import error | Package not in venv | `pip install -r requirements.txt` with venv active |
| Delete button has no effect | Form method is GET, not POST | Check `<form method="post">` in template |
| Edit form shows blank fields | Route not passing `trip` object to template | Check context dict in the GET route |
| Claude Code adds SQLAlchemy | Training data bias toward ORMs | Anti-goal: "Do not add SQLAlchemy — use the existing `sqlite3` helpers in db.py" |
