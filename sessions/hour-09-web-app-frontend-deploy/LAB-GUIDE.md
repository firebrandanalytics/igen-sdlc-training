# Lab Guide: Mileage Logbook — Hour 9 (Frontend, Tests, Deployment)

iGEN Developer AI Training · Hour 9

---

## What You Are Building

Hour 9 finishes the Mileage Logbook. You continue the **same app you built in
Hour 8** — adding features F5–F8: an IFTA apportionment summary page, a sortable
dashboard, a jurisdiction rate table, and containerisation with a runbook.

**The app is in `../hour-08-web-app-backend/`.** You are not starting fresh — keep
working in that folder, with the code, database, and CLAUDE.md you produced in
Hour 8.

**Time:** approximately 50 minutes.

---

## Environment

You set this app up in Hour 8. Reactivate the virtual environment and confirm the
app still runs. Run from the repo root.

### Windows (Git Bash)

```bash
cd sessions/hour-08-web-app-backend
source venv/Scripts/activate
uvicorn main:app --reload
```

### macOS / Linux

```bash
cd sessions/hour-08-web-app-backend
source venv/bin/activate
uvicorn main:app --reload
```

Confirm [http://127.0.0.1:8000](http://127.0.0.1:8000) still shows the trips list
with the Delete and Edit features from Hour 8, then check the tests are green:

```bash
pytest -v
```

If you did not finish Hour 8 (F2–F4), do that first — F5 depends on the
`trip_jurisdictions` table added in F4.

---

## A Note on Approach

Each feature below is a vertical slice: route, data layer, template, tests. Direct
Claude Code to handle the whole slice at once. Before each `pytest` run, read the
diff — that review discipline is what the C10 rubric is for.

---

## F5 — IFTA Apportionment Summary Page

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

## F6 — Sortable Dashboard

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

## F7 — Add a Jurisdiction Rate

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

## Test Suite Expansion

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

## Visual and Navigational Polish

This is not a UI course, but the app should be navigable. Ask Claude Code to:

- Add nav links in `templates/base.html` to Trips, Dashboard, Apportionment,
  and Jurisdictions
- Ensure each feature page has a clear heading and that tables are readable

Keep this short — 5–10 minutes. The goal is "usable," not "beautiful."

> **If the nav links break the existing tests:** the test client checks response
> content, not visual structure. Nav changes usually don't break tests unless a
> page title or heading text that a test asserts on changes.

---

## F8 — Containerise + Runbook

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

## Hour 9 Complete — Final End-State Verification

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
| `/apportionment` returns 500 | No `service.py` yet, or import error | Check that `import service` is in `main.py` |
| Percentages don't sum to 100 | Floating-point drift without remainder logic | Apply "last row gets the remainder" pattern |
| `docker build` fails at pip | Missing package in requirements.txt | Add `httpx` and any other missing packages |
| Docker container starts then exits | Startup error — check logs | `docker logs logbook` to read the error |
| Claude Code adds SQLAlchemy | Training data bias toward ORMs | Anti-goal: "Do not add SQLAlchemy — use the existing `sqlite3` helpers in db.py" |
