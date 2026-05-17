> **[Needs Tech Review]** — verify with lead instructor before use.

# C2 — CLAUDE.md Template + Annotated Example

iGEN Developer AI Training · Session 3 (Hour 5) reference

A `CLAUDE.md` file lives at the root of a repo and is read automatically by Claude Code at the start of every session. It is the primary way you "accommodate the AI" — giving the agent the context it needs to operate without asking you every time.

---

## Blank Template

Copy this into a new repo and fill in each section. Delete sections that genuinely don't apply; a short accurate file beats a long one with placeholder content.

```markdown
# CLAUDE.md — <Project Name>

## Project Overview
<!-- One paragraph: what this repo does, who uses it, why it exists. -->

## Tech Stack
<!-- Language(s), framework(s), database(s), key libraries. -->
<!-- Include versions if they matter (e.g., "Python 3.12, FastAPI 0.111"). -->

## Repository Layout
<!-- Brief map of the top-level folders. -->
<!-- Example:
  src/        application source
  tests/      pytest test suite
  scripts/    one-off helpers and seed data
  docs/       design docs and ADRs
-->

## How to Run
<!-- Exact commands to stand up the dev environment on Windows (Git Bash) and macOS/Linux. -->
<!-- Include the venv activation step for Python projects. -->

## How to Test
<!-- Command to run the full test suite. Any flags or environment variables needed. -->

## Conventions
<!-- Naming, formatting, import order, commit-message style — whatever the team enforces. -->
<!-- Only include conventions the AI might get wrong without being told. -->

## Key Constraints / Anti-Goals
<!-- What the agent must NOT do. Examples: do not modify the migrations folder, do not change
     the public API signature, do not install new dependencies without asking. -->

## Secrets & Environment Variables
<!-- List expected .env variables (names only, no values). Tell the agent where to find them. -->
<!-- Example: AZURE_CLIENT_ID, DB_PATH — loaded from .env in repo root. -->

## Recurring Tasks (if any SKILL.md files exist)
<!-- List the SKILL.md files and one-sentence summaries. -->
<!-- Example: SKILL.md/deploy.md — build and push the Docker image to ACR. -->
```

---

## Annotated Example — Mileage Logbook (course app)

Below is a filled-in `CLAUDE.md` for the mileage-logbook web app used in Hours 6–9. Margin notes explain *why* each section is written the way it is.

---

```markdown
# CLAUDE.md — Mileage Logbook
```
> **Annotation — Title:** Name the project. Claude Code can work in multiple repos
> in a day; disambiguation prevents confusion when context refers to "this project."

---

```markdown
## Project Overview
A FastAPI + SQLite web app for recording commercial vehicle trips.
iGEN drivers log start/end locations and miles per trip; the app produces
per-jurisdiction totals for IFTA reporting. Attendee exercise project; not
deployed to production.
```
> **Annotation — Overview:** Two to three sentences is enough. Include *why* the
> app exists, not just what it does — the AI uses this to make judgment calls about
> what matters and what doesn't.

---

```markdown
## Tech Stack
- Python 3.12
- FastAPI 0.115 with Jinja2 3.1 templates (server-side rendered, no JS framework)
- SQLite via the standard `sqlite3` module (no ORM)
- pytest 8.3 for testing; httpx for the test client
```
> **Annotation — Tech Stack:** Exact versions prevent the agent from suggesting
> syntax or APIs that don't exist in the version you're actually running. "No ORM"
> is an anti-goal encoded here — it prevents the agent from reaching for SQLAlchemy
> on its own.

---

```markdown
## Repository Layout
  main.py         FastAPI app: all routes and startup lifespan
  db.py           SQLite connection helper and all query functions
  service.py      computed summaries (apportionment, dashboard)
  seed.py         inserts ~10 sample trips for dev/demo
  templates/      Jinja2 HTML templates (base.html + one per page)
  static/         CSS only (style.css)
  tests/          pytest suite (conftest.py, test_db.py, test_routes.py, test_service.py)
  .claude/
    skills/
      add-jurisdiction/  multi-file skill: SKILL.md + add_jurisdiction.py
  requirements.txt
  Dockerfile
```
> **Annotation — Layout:** The agent navigates the file tree but benefits from a
> human-written map. Call out any non-obvious folder purposes. This section also
> documents intent — for example, that all routes live in `main.py` (not in a
> routes sub-package) and that database logic belongs in `db.py`, not inlined
> in route handlers.

---

```markdown
## How to Run

**Windows (Git Bash):**
```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
App runs at http://localhost:8000.
Optional: seed sample data with `python seed.py`.
```
> **Annotation — How to Run:** Include both Windows and macOS/Linux paths —
> attendees are on Windows Git Bash; the agent may run on either. Providing the
> exact command string means the agent never has to guess the activation path.
> Note: the app module is `main:app`, not `app.main:app` — there is no `app/`
> sub-package; `main.py` lives at the project root.

---

```markdown
## How to Test
```bash
pytest tests/ -v
```
All tests must pass before committing. Use `pytest tests/ -k <name>` to run one test.
```
> **Annotation — How to Test:** "All tests must pass before committing" is an
> instruction to the agent, not just documentation. This lets you skip explicitly
> saying it in every prompt.

---

```markdown
## Conventions
- PEP 8; no external formatter enforced, but keep lines under 100 chars.
- All route handlers live in `main.py` — do not create a routes sub-package.
- SQL query functions go in `db.py`; multi-step computed summaries go in
  `service.py`; route handlers stay thin (call db/service, return response).
- Commit messages: imperative mood, ≤ 72 chars, e.g. `Add delete-trip endpoint`.
```
> **Annotation — Conventions:** Only list conventions the agent would violate if
> not told. "Route handlers in main.py only" prevents the agent from creating an
> `app/routes/` sub-package — a natural reflex it has for growing FastAPI apps.
> "SQL in db.py" prevents query logic from drifting into route handlers.

---

```markdown
## Key Constraints / Anti-Goals
- DO NOT add a JavaScript framework. Jinja2 server-side rendering only.
- DO NOT introduce an ORM. Use raw SQL via `db.py`.
- DO NOT create a routes sub-package (`app/routes/`). All routes live in `main.py`.
- DO NOT change the SQLite schema (tables: trips, trip_jurisdictions, jurisdictions)
  without asking — schema changes ripple through db.py, service.py, templates,
  and tests.
- DO NOT add new pip dependencies without asking first.
```
> **Annotation — Anti-Goals:** This is the highest-value section in a CLAUDE.md.
> Without it, the agent optimises toward what looks "good" by training data
> standards, which may mean adding SQLAlchemy, switching to htmx, or splitting
> routes into a sub-package. Be specific and use DO NOT.

---

```markdown
## Secrets & Environment Variables
- `DB_PATH` — path to the SQLite database file.
  Default: `logbook.db` in the project root (see `db.py`).
  Override: `DB_PATH=/tmp/test.db uvicorn main:app --reload`

No `.env` file is required for local dev; the default is safe for
development. Set `DB_PATH` as a shell variable or Docker env var in
production / CI.
```
> **Annotation — Secrets:** List variable names so the agent knows they exist and
> where to find them. Note that this project does NOT use python-dotenv — `DB_PATH`
> is read directly via `os.environ.get("DB_PATH", "logbook.db")` in `db.py`.
> Saying "load with python-dotenv" would be wrong and would cause the agent to
> install an unnecessary dependency.

---

```markdown
## Recurring Tasks
- `.claude/skills/add-jurisdiction/` — add or update a US state and its IFTA
  tax rate in the `jurisdictions` table. Includes a helper script
  (`add_jurisdiction.py`) that validates inputs and writes to the database.
  Run: `/add-jurisdiction TX Texas 0.200`
```
> **Annotation — Recurring Tasks:** A one-line index pointing to skill files.
> The agent can read those files on demand; you don't need to duplicate their
> content here. Use the real folder path (`.claude/skills/<name>/`) so the
> agent knows where to look without a directory scan.

---

> **Footnote — AGENTS.md:** Some cross-tool environments use `AGENTS.md` as the
> portable equivalent of `CLAUDE.md`. This course teaches `CLAUDE.md` exclusively;
> the format and intent are identical.

<!-- VERIFY: confirm that CLAUDE.md is the canonical filename read automatically by the current Claude Code version — no additional flag required -->
<!-- VERIFY: confirm that Jinja2 and server-side rendering is the intended approach for the course mileage-logbook app (no htmx / HTMX additions planned) -->
