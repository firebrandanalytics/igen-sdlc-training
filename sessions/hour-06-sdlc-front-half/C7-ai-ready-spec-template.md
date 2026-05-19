# C7 — "AI-Ready Spec" Prompt Template

iGEN Developer AI Training · Used in Hours 2, 6, and 7

Copy this template. Fill in every section before handing the task to Claude Code. Delete sections that genuinely don't apply, but be honest about whether they apply — most of them do.

---

## Why This Template Exists

Vague prompts produce confident but wrong output. The agent doesn't have your intuition, your knowledge of the codebase, or your understanding of the business context. This template makes that implicit knowledge explicit — turning a vague ask into a structured spec the agent can execute reliably.

"I want a script that pulls last quarter's fuel tax filings and flags anomalies" is a starting point. The template below turns it into an instruction set.

---

## The Template

```
## Task
<!-- One to three sentences. What do you want done? Be concrete.
     "Add a delete endpoint for trips" beats "improve the trips feature." -->

## Context
<!-- What does the agent need to know about the codebase, team conventions,
     or business domain that it can't read from the source files?
     Examples: "We don't use SQLAlchemy," "This script runs in a CI pipeline,"
     "The IFTA jurisdiction table is in db/jurisdictions.csv." -->

## Constraints
<!-- What must be true about the solution?
     Technical: must use Python 3.12, must not add new dependencies, must run on Windows.
     Functional: must handle the case where the input CSV is empty gracefully.
     Style: must follow the existing route/service split in this codebase. -->

## Anti-Goals
<!-- What does the solution explicitly NOT need to do?
     Examples: "Don't build a UI — CLI output is enough."
     "Don't worry about pagination — max 50 rows in practice."
     "Don't modify the schema — new code only." -->

## Acceptance Criteria
<!-- Bullet list of verifiable pass/fail statements.
     Each criterion should be checkable without judgment calls:
     - Running `pytest tests/` passes with zero failures.
     - `DELETE /trips/{id}` returns 204 for a valid ID.
     - `DELETE /trips/9999` returns 404 when the trip doesn't exist.
     - No import of SQLAlchemy anywhere in the diff. -->

## Files to Read First
<!-- List the files the agent should read before writing any code.
     Saves time; prevents the agent from inventing a schema it could have read.
     Examples: app/routes/trips.py, app/services/trip_service.py, app/db.py -->

## Files to Modify (expected)
<!-- Best guess at what changes. The agent will deviate if needed, but this
     anchors scope and surfaces surprises.
     Examples: app/routes/trips.py (add DELETE handler), tests/test_trips.py (add test) -->

## Dos
<!-- Optional. Explicit "prefer X" instructions:
     - Prefer early returns over deeply nested if-blocks.
     - Prefer named constants over magic numbers.
     - Do follow the existing pattern in trips.py for error handling. -->

## Don'ts
<!-- Optional. Explicit prohibitions beyond constraints and anti-goals:
     - Don't add docstrings to private helper functions — not our convention.
     - Don't rename existing variables — it breaks other agents' context. -->

## Glossary (for this task)
<!-- Terms that mean something specific in this context that the agent might misread.
     Examples: "jurisdiction" = a US state or Canadian province in this codebase, not a generic concept.
     "trip" = a single vehicle-movement record in the logbook schema, not a round trip. -->

## Definition of Done
<!-- One clear statement: when is this task complete and ready for review?
     Example: "When all acceptance criteria pass, the code is committed on a feature branch,
     and I have reviewed the diff." -->
```

---

## Quick-Fill Tips

**Start with Acceptance Criteria.** If you can't write testable acceptance criteria, the task is still vague. Write those first, then fill in the rest — the other sections almost write themselves.

**Anti-Goals earn their keep.** The agent optimises for "good" as defined by training data. Without anti-goals, it will add pagination, add authentication, add logging — because that's what a production feature "should" have. Anti-goals redirect that energy.

**Context ≠ re-paste the schema.** Tell the agent *where* to find the schema, not what it contains. "Read `app/models.py` for the Trip dataclass" is better than pasting the whole dataclass into the prompt.

**Glossary is underused.** Domain terms — IFTA, apportionment, jurisdiction — mean specific things in iGEN's context that differ from general usage. A two-line glossary prevents a category of hallucination.

---

## Before-and-After Example

**Before (vague):**
> Add a way to flag suspicious trips.

**After (AI-ready):**
> **Task:** Add a `suspicious` boolean column to the `trips` table. A trip is suspicious if its miles exceed 800 or if `start_location` equals `end_location`. Flag it on creation; surface it in the trips list.
>
> **Context:** Trip data lives in the `trips` SQLite table (see `db.py`). The schema has `trip_date`, `start_location`, `end_location`, and `miles`. The app is server-rendered (Jinja2); there is no JSON API.
>
> **Constraints:** No new dependencies. Add the column via `ALTER TABLE` in `db.init_db()`; do not drop and recreate the table.
>
> **Anti-Goals:** Don't build a filter UI for hiding suspicious trips — that is out of scope for this version.
>
> **Acceptance Criteria:**
> - A trip with more than 800 miles is marked suspicious in the database.
> - A trip where `start_location == end_location` is marked suspicious.
> - A trip with 400 miles and distinct locations is not marked suspicious.
> - The trips list page shows a visual indicator (e.g. a flag) for suspicious trips.
> - `pytest tests/` passes.
>
> **Files to Read First:** `main.py`, `db.py`, `templates/trips_list.html`, `tests/conftest.py`
>
> **Definition of Done:** Acceptance criteria pass; change committed on a feature branch; I've reviewed the diff.
