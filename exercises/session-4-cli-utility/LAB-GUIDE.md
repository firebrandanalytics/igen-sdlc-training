# Lab Guide: Build the IFTA CLI Utility

iGEN Developer AI Training · Self-Study Take-Home Reference

> **Self-study take-home reference.** This guide walks through a complete greenfield
> SDLC pass — requirements, tests, implementation, packaging — using the IFTA
> calculator as the worked example. It is designed for self-paced exploration after
> the course, not for use during Session 4. Work through it at whatever depth is
> useful to you.

> **[Needs Tech Review]** — IFTA domain rules, tax rates, and the expected output
> values in this guide depend on placeholder rates in `jurisdictions.py`. Augustus
> will verify the rates and the corresponding expected output before distribution.
> Claude Code version references should be confirmed against the locked demo environment.

---

## Before You Start

**What you are building:** A command-line tool called `ifta-calc` that reads a CSV
of trip records and prints an IFTA fuel-tax apportionment table. The full
specification is in `SPEC.md` — read it before touching any code.

**What you are practising:** Directing Claude Code through a structured build rather
than writing code yourself. The agent does the typing; you do the directing and
reviewing.

**Time:** 50–60 minutes.

**What you have already:**

| File | Status |
|------|--------|
| `SPEC.md` | Complete spec — the *what* |
| `ifta_calculator/jurisdictions.py` | Provided, do not modify |
| `ifta_calculator/loader.py` | Stub only — `NotImplementedError` |
| `ifta_calculator/calculator.py` | Stub only — `NotImplementedError` |
| `ifta_calculator/cli.py` | Stub only — `NotImplementedError` |
| `tests/test_calculator.py` | One failing test (AC-1) |
| `sample_data/trips.csv` | 12-row sample — ready to use |
| `pyproject.toml` | Configured — `pip install -e ".[dev]"` already set up |

---

## Environment Setup

Do this once, before any Claude Code sessions.

### Windows (Git Bash)

```bash
cd exercises/session-4-cli-utility
python -m venv .venv
source .venv/Scripts/activate
pip install -e ".[dev]"
```

### macOS / Linux

```bash
cd exercises/session-4-cli-utility
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

After `pip install -e ".[dev]"`, the `ifta-calc` command is available inside the virtual
environment. You don't need to reinstall it as you edit the source — that's what
`-e` (editable mode) does.

**Verify the install:**

```bash
ifta-calc --help
```

Expected: the argument parser help block. If you get `command not found`, the venv
is not activated — activate it and try again.

---

## How to Work Through This Lab

Open a Claude Code session **in the `session-4-cli-utility/` directory**. Keep
`SPEC.md` open in a separate window for reference.

The steps below tell you what to direct Claude Code to do at each stage. They do
not tell you the exact prompts — constructing the prompt is part of the exercise.
Use the C7 AI-ready spec template if you want a structured prompt; or give a
direct, scoped instruction if the step is clear enough.

One rule: **review before you move on.** After Claude Code writes or changes a
file, read what it produced. If something looks wrong, say so before running tests.

---

## Step 1 — Implement `load_trips()`

**Goal:** Make `loader.py` read the CSV and return a list of dicts with `miles`
coerced to float. It should raise `ValueError` for a missing required column and
`FileNotFoundError` for a missing file.

**Direct Claude Code to:** implement `load_trips()` in `ifta_calculator/loader.py`.
Point it to `SPEC.md` for the input format and to the docstring already in the stub.

**Verify manually before continuing:**

```python
# From a Python REPL (with venv active)
from ifta_calculator.loader import load_trips
trips = load_trips("sample_data/trips.csv")
print(len(trips), trips[0])
```

Expected: 12 rows; first row looks like:
`{'trip_id': 'T001', 'vehicle_id': 'TRUCK-01', 'period': '2024-Q1', 'jurisdiction': 'IL', 'miles': 450.0}`

> **If you get stuck here:** Ask Claude Code to show you what `csv.DictReader`
> returns for the first row of the file — see if the column names match what
> `SPEC.md` specifies. Column whitespace can cause mismatches.

---

## Step 2 — Implement `calculate()` and pass the AC-1 test

**Goal:** Make the provided failing test pass. The test checks a single 100-mile
trip in Illinois at 6.5 MPG.

**Direct Claude Code to:** implement `calculate()` in `ifta_calculator/calculator.py`.
The formula is in `SPEC.md`. Tell it: do not round intermediate values; round only
`tax_owed` to 2 decimal places.

**Run the test:**

```bash
pytest tests/test_calculator.py -v
```

Expected: `1 passed`.

> **If the test fails with a NotImplementedError:** the function still returns the
> stub. Ask Claude Code to check that the stub was actually replaced.

> **If the math is wrong:** paste the test failure output to Claude Code and ask it
> to walk through the formula step by step. The formula is:
> `fuel_used = miles / fleet_mpg`, `tax_owed = round(fuel_used * rate, 2)`.

**Checkpoint 1 passed** when `pytest tests/test_calculator.py -v` shows `1 passed`.

---

## Step 3 — Add tests for AC-2 through AC-7

**Goal:** Write tests covering the remaining acceptance criteria before implementing
`cli.py`. This is the test-plan-first discipline from Hour 6.

Open `SPEC.md` and read the acceptance criteria table. Direct Claude Code to add
tests for AC-2 through AC-7 in `tests/test_calculator.py`.

Each criterion should have at least one test. Some have multiple (AC-5 should test
both that the error is raised and that the message is clear).

**Run the full test file:**

```bash
pytest tests/test_calculator.py -v
```

At this point, all new tests should also pass — `calculate()` should already handle
these cases if it was implemented correctly. If any fail, fix `calculator.py` first
before adding more tests.

> **If Claude Code adds tests that don't actually test the criterion:** read the
> test carefully. A common mistake is testing that no error is raised when the
> criterion says an error *should* be raised. Point out the mismatch.

> **For AC-6 (missing CSV column raises ValueError):** the test needs to create a
> CSV with a missing column. You can do this in the test with `tmp_path` and
> `pathlib.Path`. Ask Claude Code to use pytest's `tmp_path` fixture.

**Checkpoint 2 passed** when all tests in `test_calculator.py` pass.

---

## Step 4 — Implement `main()` in `cli.py`

**Goal:** Wire together `load_trips()` + `calculate()` + a formatted table printed
to stdout. Handle errors gracefully (file not found, bad CSV, unknown jurisdiction)
by printing to stderr and exiting with code 1.

**Direct Claude Code to:** implement `main()` in `ifta_calculator/cli.py`. Give it:
- The CLI interface from `SPEC.md` (`--csv` and `--mpg` flags)
- The example output format from `SPEC.md`
- The error-handling requirements (AC-5, AC-6 — clear messages, not tracebacks)

**Verify the CLI:**

```bash
ifta-calc --csv sample_data/trips.csv
```

Compare your output to the example in `SPEC.md`. Columns, alignment, and the TOTAL
row should all be present.

> **If `ifta-calc` is still running the old (unimplemented) version:** the editable
> install picks up changes automatically, but Python's import cache can sometimes
> lag. Try:
> ```bash
> pip install -e ".[dev]" --force-reinstall
> ```

> **If the table alignment is off:** ask Claude Code to use f-string format
> specifiers to fix column widths. Point it to the example output in `SPEC.md` for
> the expected column widths.

**Test error handling manually:**

```bash
# File not found
ifta-calc --csv nonexistent.csv
echo "Exit code: $?"

# Invalid MPG
ifta-calc --csv sample_data/trips.csv --mpg -1
echo "Exit code: $?"
```

Both should print a clear error message to stderr (not a Python traceback) and exit
with code 1.

**Checkpoint 3 passed** when the CLI runs without error, the output table matches
the `SPEC.md` example structure, and error cases exit cleanly.

---

## Step 5 — Run the full test suite

```bash
pytest -v
```

All tests should pass. If any fail, read the failure message and direct Claude Code
to fix the specific issue.

> **If tests pass in isolation but fail together:** check whether the test file
> imports are correct. The package must be installed (`pip install -e ".[dev]"`) for
> `from ifta_calculator.calculator import calculate` to work.

**Checkpoint 4 passed** when `pytest -v` reports no failures.

---

## End-State Verification

Run this sequence. Every step must succeed before you are done.

```bash
# 1. All tests pass
pytest -v

# 2. CLI produces output for the sample data
ifta-calc --csv sample_data/trips.csv

# 3. Custom MPG works
ifta-calc --csv sample_data/trips.csv --mpg 7.5

# 4. Error exits cleanly (non-zero code)
ifta-calc --csv missing.csv; echo "Exit: $?"
```

The output from step 2 should show:
- A header block (Period, Vehicles, Fleet MPG)
- One row per jurisdiction (IA, IL, IN, MN, MO, OH, WI for the sample data)
- A TOTAL row
- No Python traceback anywhere

---

## Reflection — What Just Happened

Before moving to Hour 8, take two minutes to note:

1. Which step required the most back-and-forth with Claude Code, and why?
2. At what point did you catch something in Claude Code's output before running the
   tests — and how?
3. The `jurisdictions.py` module was handed to you with placeholder tax rates. How
   would you verify those rates in a real project? (You don't need to do it now —
   just think about it.)

---

## Appendix — Quick Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `ifta-calc: command not found` | venv not activated | `source .venv/Scripts/activate` (Windows) or `source .venv/bin/activate` (macOS/Linux) |
| `ModuleNotFoundError: ifta_calculator` | Not installed in editable mode | `pip install -e ".[dev]"` |
| `pytest` not found | venv not activated, or pytest not installed | Activate venv; run `pip install -e ".[dev]"` |
| AC-1 tax_owed wrong | Rounding applied to intermediate value | Tax formula: `round(fuel_used * rate, 2)` — do not round `fuel_used` first |
| Unknown jurisdiction error | A jurisdiction code in the CSV is not in `jurisdictions.py` | Check `sample_data/trips.csv` — all codes must be in the rate table |
| Output columns misaligned | f-string width not set | Point Claude Code to the example output in `SPEC.md` |
