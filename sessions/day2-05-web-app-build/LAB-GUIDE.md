# Lab Guide: Web App Build — Segment 5

iGEN Developer AI Training · Day 2 · Segment 5 (120 min)

This is your reference for the segment. The instructor will walk the room
through each beat live; this guide is here so you can keep moving if you fall
behind, or pick up from any beat if you arrived late.

---

## What you're building

The **IFTA apportionment summary page** (F5): a page in the Mileage Logbook
that shows tax owed per jurisdiction for trips in your data, using the
authoritative calculation logic from the IFTA CLI.

You'll do it in three moves:

1. **Extract a calc-skill** from the IFTA CLI (~25 min) — produce a markdown
   document capturing how the math works.
2. **Plan in planning mode** (~20 min) — feed planning mode your sharpened F5
   spec (from segment 4) plus the calc-skill; iterate until the plan is good;
   approve.
3. **Build with parallel subagents** (~60 min) — split backend and frontend
   into two subagents working against the plan's API contract; integrate;
   test.

Final ~15 min is debrief and close.

---

## Environment

### From segment 4, you should already have:

- Your sharpened **F5 spec** somewhere you can paste it (in your notes, in a
  text file, anywhere).
- The student repo's `cli-utility/` installed and tests passing
  (`cd cli-utility && pytest -v` should show 12 passing).
- The web-app starter installed (this folder — `day2-05-web-app-build/`)
  and tests passing (`pytest -v` should show 4 passing).

### If you need to set up from scratch:

#### CLI:

```bash
cd cli-utility
python3 -m venv .venv
source .venv/bin/activate         # Windows Git Bash: source .venv/Scripts/activate
pip install -e ".[dev]"
pytest -v
```

#### Web app:

```bash
cd sessions/day2-05-web-app-build
python3 -m venv venv
source venv/bin/activate           # Windows Git Bash: source venv/Scripts/activate
pip install -r requirements.txt
python seed.py
pytest -v
uvicorn main:app --reload
# then open http://127.0.0.1:8000
```

---

## Beat 1 — Extract the calc-skill (25 min)

Open Claude Code in `cli-utility/`. Run this prompt:

```
Read the source code under ifta_calculator/ and the tests in tests/. Produce a
markdown document — a "calc skill" — that captures every authoritative rule,
definition, and edge case the CLI uses to compute IFTA fuel tax. Treat the code
and tests as the source of truth; ignore any prose documentation, including
the README, when extracting the rules.

Include at minimum:
- The apportionment formula (how miles, fuel, and tax relate)
- Rounding behaviour and where it applies
- Per-jurisdiction special handling (rates, surcharges)
- The full set of supported jurisdictions and what kind of codes they are
- Any implicit assumptions (e.g., fuel type, period handling)
- Behaviour on edge cases (empty input, unknown codes, invalid mpg)

Anyone reading this document should be able to re-implement the calculations
in a different codebase without seeing the original code.

Write the output to ifta-calc-skill.md in this folder.
```

Read what it produces. Rules that are easy to miss: **surcharges** on certain
states, **half-up rounding** at the cent, **silent multi-period aggregation**.
Push the agent to dig deeper if the doc is shallow.

> Quality check before you move on: would a Python developer who has never
> seen this CLI be able to write a correct re-implementation from your
> document alone? If not, send the agent back for another pass.

---

## Beat 2 — Planning mode (20 min)

Now switch to the web-app starter:

```bash
cd ../day2-05-web-app-build
```

Launch Claude Code in planning mode:

```bash
claude --permission-mode plan
```

(Or open normally and `Shift+Tab` into plan mode.)

Run this prompt, filling in the two artifacts:

```
I want to build a new feature in this web app: an IFTA apportionment summary
page. Below are TWO artifacts you must read carefully before planning anything.

ARTIFACT 1 — Feature spec (what to build):
<paste your sharpened F5 spec here>

ARTIFACT 2 — Calculation rules (how the math works):
<paste the contents of ifta-calc-skill.md here>

Plan the implementation. The plan must include:

1. Every file you will touch, and what specifically you will change in each.
2. An EXPLICIT API contract — the JSON request/response shape between the
   backend route and the frontend template, including field names and types.
   We will implement backend and frontend in parallel against this contract,
   so it must be unambiguous.
3. The order of work, and which pieces can be built in parallel.
4. Any place where the spec and the calc-skill might conflict, and your
   proposed resolution.

Do not write or modify any code yet. Wait for my approval before proceeding.
```

**Read the plan.** Push back. Iterate. Be especially picky about the API
contract — that's the boundary between your two subagents in the next beat.

Approve only when the plan is concrete enough that you'd trust the build.

---

## Beat 3 — Parallel subagent build (~60 min)

In the same Claude Code session (the plan is in context), run:

```
Use subagents to implement the plan in parallel:

- Subagent A: implement the backend per the plan — routes, database queries,
  any calc helpers — matching the API contract exactly.
- Subagent B: implement the frontend per the plan — template, any styling
  needed — consuming the API contract exactly.

Both subagents work against the API contract from the plan. When both are
done, integrate (wire the route to the template), run the test suite, and
report what passed and what didn't.
```

Approve actions as they come up. **`Ctrl+E` on anything you're not sure
about** — see the action before approving. (Segment 2 muscle.) Auto-accept
the obvious ones if you're in Auto-accept mode.

### Running the app

```bash
uvicorn main:app --reload
```

Then open the URL the agent built (likely something like
`http://127.0.0.1:8000/apportionment`). Hard-reload (`Ctrl+Shift+R`) if the
template change isn't showing.

### Running the tests

```bash
pytest -v
```

The existing 4 tests should still pass; new tests for F5 should be added.

### When tests fail

That's normal. Read the failure with Claude Code, ask it to identify the
disagreement (usually backend vs frontend on the API contract), fix, re-run.

### If you finish early

Pick one stretch goal:
- Sort the table by tax owed (descending)
- Add a quarter filter so you can switch between Q1 and Q2
- Make the surcharge jurisdictions visually distinct in the table

---

## Pacing (rough markers from the start of the segment)

| Elapsed | Where you should be |
|---:|---|
| 25 min | Calc-skill written; switching to web-app |
| 45 min | Plan approved |
| 65 min | Both subagents reporting done; integrating |
| 85 min | Page renders something; debugging integration |
| 105 min | Tests green or close; debrief starting |

If you're significantly behind, ask the instructor — there's an answer-key
fallback (`solutions/web-app/` in the internal repo) for asynchronous
completion.

---

## What you'll take from this

The loop you just ran is the real workflow:

1. **Extract** the implicit rules from the code that already owns them.
2. **Plan** with explicit artifacts — spec + extracted rules.
3. **Split** independent work into parallel subagents against a contract.
4. **Integrate, test, fix.**

Not all four steps every time, but the moves are the same. Use them on Monday.
