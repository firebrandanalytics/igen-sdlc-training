# IFTA Fuel-Tax Calculator

A small command-line tool that computes IFTA fuel-tax apportionment from a CSV
of trip mileage records. Reads trips, aggregates miles per jurisdiction,
computes fuel used and tax owed, and prints a summary table.

This is the calculator that the web-app build references for its tax-math.

---

## Setup

### Windows (Git Bash or PowerShell 7)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

---

## Run it

```bash
ifta-calc --csv sample_data/trips.csv --mpg 6.5
```

Output is a per-jurisdiction table with miles, fuel used, and tax owed,
followed by totals.

---

## Tests

```bash
pytest -v
```

---

## Layout

```
ifta_calculator/
    __init__.py
    jurisdictions.py   # rate + surcharge table
    loader.py          # CSV -> list[dict]
    calculator.py      # apportionment math
    cli.py             # argparse + report formatter
tests/
    test_calculator.py # behavioural tests, one rule per test
sample_data/
    trips.csv          # sample input (Q1 + Q2, US + Canada)
```
