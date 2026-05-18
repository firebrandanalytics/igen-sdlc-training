# D7 — Lab Guide: Extend the Mileage Logbook Web App

iGEN Developer AI Training · Sessions 4 & 5 (Hours 8 and 9)

> **[Needs Tech Review]** — Docker commands (F8), pytest patterns, and FastAPI
> version-specific behaviour should be verified against the distributed environment
> before this sheet is used live. Claude Code command references should be confirmed
> against the locked demo environment. IFTA apportionment logic in F5 uses
> illustrative rates — verify with Augustus before the live session.

---

## What You Are Building

You are extending the Mileage Logbook starter — a minimal FastAPI + SQLite + Jinja2
app that can already list and create trips. Over Hours 8 and 9 you will add seven
features (F2–F8) by directing Claude Code through a structured build.

Read the starter app's `README.md` before you do anything else. It describes the
data model, project layout, and how to run the existing tests.

**Time:** approximately 50 minutes per hour block (Hour 8 / Hour 9).

Hour 8 builds the backend features (F2–F4). Hour 9 builds the frontend pages,
expands the tests, and deploys (F5–F8).

---

## Environment Setup

Do this once, before any Claude Code sessions.

### Windows (Git Bash)

```bash
cd exercises/session-4-5-web-app
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python seed.py
uvicorn main:app --reload
```

### macOS / Linux

```bash
cd exercises/session-4-5-web-app
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

## HOUR 8 — Backend: F2 through F4

---

### Warm-Up — Write a CLAUDE.md

Before directing Claude Code to write any feature code, give it the context it
needs to operate in this project. Open a Claude Code session in the
`session-4-5-web-app/` directory and ask it to write a `CLAUDE.md` that covers:

- Project purpose and stack (FastAPI, SQLite, Jinja2, Python 3.11+)
- The existing module layout (main.py, db.py, seed.py, templates/, tests/)
- Testing convention (pytest; `client` fixture in `tests/conftest.py` provides a
  TestClient backed by a temp database; do not use the live `logbook.db`)
- Style conventions you care about (e.g. "query logic lives in db.py, not in route
  handlers")

This takes 5–10 minutes. A good CLAUDE.md is the difference between an agent that
guesses at your conventions and one that follows them consistently.

---

### F2 — Delete a Trip

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

### F3 — Edit a Trip

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

### F4 — Per-Jurisdiction Miles

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

### Hour 8 Complete — End-State Check

```bash
pytest -v
```

Expected: all tests pass. Then verify in the browser:

- [ ] Delete button removes a trip from the list
- [ ] Edit form pre-fills the existing data and saves changes
- [ ] A trip can record miles for individual states, saved and shown again on edit

If any of these are missing, do not move to Hour 9.

---

## HOUR 9 — Frontend, Tests, and Deployment: F5 through F8

---

### F5 — IFTA Apportionment Summary Page

**Goal:** `GET /apportionment` shows a page summarising total miles per jurisdiction
across all trips, with each jurisdiction's percentage of total miles.

**What this teaches:** test-plan-first in practice. Hour 6 demonstrated the
front-half SDLC methodology (vague ask → sharpened requirements → test plan)
using the "flag suspicious trips" vague ask as the exercise vehicle; F5 is the
feature that methodology was building toward. The spec and test plan produced in
the Hour 6 instructor demo become the acceptance criteria you build against here.

**Direct Claude Code to:**
- Create `service.py` with a `get_apportionment_summary(conn)` function that
  queries the `trip_jurisdictions` table, groups by state, computes each
  jurisdiction's percentage of total miles (rounded to 2dp), and returns a list of
  summary objects plus a grand total
- Add `GET /apportionment` to `main.py`, calling `service.get_apportionment_summary`
- Add `templates/apportionment.html` showing the summary table
- Add tests in `tests/test_service.py` for the service function

**Files to read first in your prompt:** `db.py`, `main.py`, `tests/conftest.py`

**Verify:**
```bash
pytest -v
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/apportionment
```

Expected HTTP response: `200`. The page should show a table with state codes,
miles, and percentages. If no jurisdiction data has been entered, the page should
show a helpful message rather than a crash.

> **If percentages don't sum to 100%:** the last row should receive the remainder
> (`100 - sum_of_other_rows`) to avoid floating-point drift. Ask Claude Code to
> implement this "give the last row the remainder" pattern.

**Checkpoint H9-1:** `pytest -v` passes; `/apportionment` shows a summary table.

---

### F6 — Sortable Dashboard

**Goal:** `GET /dashboard` shows a per-vehicle summary table (trip count, total
miles, distinct jurisdictions visited) that can be sorted by any column via query
parameters.

**Direct Claude Code to:**
- Add `get_dashboard_rows(conn, sort_by, order)` to `service.py`. Safe-list allowed
  sort column names — do not interpolate user input directly into SQL.
- Add `GET /dashboard` to `main.py` accepting `?sort=` and `?order=asc/desc`
  query parameters
- Add `templates/dashboard.html` with column header links that toggle sort order

**Security note to include in your prompt:** "The `sort_by` parameter must be
validated against a fixed allowlist — never interpolate it directly into the SQL
string. If an unrecognised sort key is provided, default to `total_miles`."

**Verify:**
```bash
pytest -v
# In browser: try ?sort=vehicle&order=asc, then ?sort=total_miles&order=desc
```

> **If the sort toggle links are all the same URL:** the template needs to build a
> URL that flips the current `order` value. Ask Claude Code to show you how it
> generates those links.

**Checkpoint H9-2:** `pytest -v` passes; dashboard sorts by each column.

---

### F7 — Add a Jurisdiction Rate

**Goal:** `GET /jurisdictions` lists the rate table; `POST /jurisdictions` adds or
updates a rate. The table is used by F5 to show tax rates alongside miles.

This feature also includes a SKILL.md — you will write a skill that wraps the
add-jurisdiction task so Claude Code can execute it reliably in future sessions.

**Direct Claude Code to:**
- Add a `jurisdictions` table to `db.init_db()`:
  `(state_code TEXT PRIMARY KEY, state_name TEXT, tax_rate REAL)`
- Add `get_all_jurisdictions`, `get_jurisdiction`, `upsert_jurisdiction` to `db.py`
- Add `GET /jurisdictions` and `POST /jurisdictions` routes to `main.py`
- Add `templates/jurisdictions.html` with a list table and an add-rate form

**Then separately:** ask Claude Code to write a `SKILL.md` in
`.claude/skills/add-jurisdiction/SKILL.md` that documents how to add or update a
jurisdiction rate. The skill should describe: inputs (state code, name, rate),
validation rules, how to invoke the POST route or a helper script, and how to
verify the change was saved.

**Verify:**
```bash
pytest -v
# In browser: add a state (e.g. TX, Texas, 0.2000), confirm it appears in the table
# Then visit /apportionment — TX should now show a tax rate in its row
```

**Checkpoint H9-3:** `pytest -v` passes; rates can be added and updated; the skill
file exists at `.claude/skills/add-jurisdiction/SKILL.md`.

---

### Test Suite Expansion

With the feature pages built, and before you containerise the app, spend 10 minutes
expanding the test suite to cover any behaviour that is not yet tested. Use
`tests/test_service.py` for service layer tests and `tests/test_routes.py` for
HTTP-level tests.

Things that are commonly undertested at this point:

- Apportionment percentages with zero total miles (should return empty, not divide
  by zero)
- Dashboard with no trips (should return 200 with an empty table, not 500)
- Jurisdiction upsert: posting the same state code twice should update the rate, not
  create a duplicate

Ask Claude Code to identify any gaps in the current test coverage by reading the
test files alongside the service functions, then fill them.

```bash
pytest -v
```

**Checkpoint H9-4:** all new tests pass alongside the existing ones.

---

### Visual and Navigational Polish

This is not a UI course, but the app should be navigable. Ask Claude Code to:

- Add nav links in `templates/base.html` to Trips, Dashboard, Apportionment,
  and Jurisdictions
- Ensure each feature page has a clear heading and that tables are readable

Keep this short — 5–10 minutes. The goal is "usable," not "beautiful."

> **If the nav links break the existing tests:** the test client checks response
> content, not visual structure. Nav changes usually don't break tests unless a
> page title or heading text that a test asserts on changes.

---

### F8 — Containerise + Runbook

**Goal:** A `Dockerfile` that builds and runs the app; a `RUNBOOK.md` that Claude
Code can execute to build, run, smoke-test, and roll back.

**What this teaches:** runbooks as executable workflows. After you write the
runbook, you will ask Claude Code to execute it — demonstrating that a
well-structured runbook is a form of "Make Correctness Easy."

**Part A — Dockerfile.** Direct Claude Code to write a `Dockerfile`:
- Base image: `python:3.12-slim`
- Install dependencies from `requirements.txt`
- Copy application source
- Run as a non-root user
- Expose port 8000
- `CMD`: `uvicorn main:app --host 0.0.0.0 --port 8000`

**Verify the build:**
```bash
docker build -t mileage-logbook .
docker run -d --name logbook -p 8000:8000 mileage-logbook
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/
docker stop logbook && docker rm logbook
```

Expected HTTP code: `200`.

> **If `docker build` fails with a pip error:** the error is usually a missing
> package in `requirements.txt`. Check that `httpx` is listed (required by
> pytest's TestClient but often omitted from requirements).

> **Windows note:** Docker Desktop must be running before any `docker` command.
> If you see `error during connect`, open Docker Desktop and wait for it to report
> "Engine running."

**Part B — RUNBOOK.md.** Direct Claude Code to write a `RUNBOOK.md` with these
numbered sections, each with copy-paste commands and expected output:

1. Build the image
2. Seed the database (optional)
3. Run the application
4. Smoke test (HTTP health check + create a trip via curl + pytest inside the container)
5. Stop the container
6. Rollback procedure (tag the known-good image, stop and revert)
7. Cleanup

**Part C — Execute the runbook.** With the runbook written, open a new Claude Code
session and say:

> "Execute RUNBOOK.md step by step. Stop and tell me if any step fails before
> continuing."

Watch Claude Code work through the runbook. Note whether it follows the steps
literally or improvises. Any improvisation is a signal that the runbook needs
clarification.

> **If smoke test step 4d (pytest inside container) fails:** the most common cause
> is `httpx` not being in `requirements.txt`. The TestClient requires it. Add it,
> rebuild, and re-run.

**Checkpoint H9-5:** `docker build` succeeds; HTTP health check returns 200;
Claude Code executes the runbook without needing to deviate from its steps.

---

### Hour 9 Complete — Final End-State Verification

```bash
# All tests pass locally
pytest -v

# Container build and smoke test
docker build -t mileage-logbook . && \
docker run -d --name logbook -p 8000:8000 mileage-logbook && \
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8000/ && \
docker stop logbook && docker rm logbook
```

Expected: all tests pass; HTTP response is `200`.

Final browser check (with `uvicorn main:app --reload` running locally):

- [ ] All 5 nav links work
- [ ] Trips list shows Delete and Edit buttons
- [ ] Edit form pre-fills correctly
- [ ] `/apportionment` shows per-state totals
- [ ] `/dashboard` sorts by column header clicks
- [ ] `/jurisdictions` accepts new rates
- [ ] Adding a jurisdiction rate then visiting `/apportionment` shows that rate

---

## Reflection — The Full Build

Before leaving:

1. Look at `db.py` now versus what it was when you started. The starter had 3
   helpers; you now have many more. Would you structure it differently if starting
   fresh today?
2. Which Claude Code task produced the most unexpected output, and how did you
   redirect it?
3. The `service.py` layer was introduced at F5 because route handlers were getting
   complex. What was the trigger? What would you have done without a service layer?

---

## Appendix — Quick Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `uvicorn: command not found` | venv not activated | `source venv/Scripts/activate` (Windows) or `source venv/bin/activate` (macOS/Linux) |
| `pytest` fails with import error | Package not in venv | `pip install -r requirements.txt` with venv active |
| Delete button has no effect | Form method is GET, not POST | Check `<form method="post">` in template |
| Edit form shows blank fields | Route not passing `trip` object to template | Check context dict in the GET route |
| `/apportionment` returns 500 | No `service.py` yet, or import error | Check that `import service` is in `main.py` |
| Percentages don't sum to 100 | Floating-point drift without remainder logic | Apply "last row gets the remainder" pattern |
| `docker build` fails at pip | Missing package in requirements.txt | Add `httpx` and any other missing packages |
| Docker container starts then exits | Startup error — check logs | `docker logs logbook` to read the error |
| Claude Code adds SQLAlchemy | Training data bias toward ORMs | Anti-goal: "Do not add SQLAlchemy — use the existing `sqlite3` helpers in db.py" |
