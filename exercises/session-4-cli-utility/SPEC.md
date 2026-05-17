> **[Needs Tech Review]** — IFTA domain rules (tax rates, apportionment formula,
> rounding) are illustrative placeholders. Augustus will verify before the live session.

# IFTA Fuel-Tax Calculator — Exercise Specification (Hour 7)

## Background

The **International Fuel Tax Agreement (IFTA)** simplifies fuel-tax reporting for
carriers that operate across multiple US states and Canadian provinces. Instead of
filing with every jurisdiction separately, a carrier files a single quarterly report
with its home ("base") jurisdiction.

The core calculation is **apportionment by miles driven**:

1. For each jurisdiction, divide the miles driven there by the fleet's average fuel
   economy (miles per gallon) to get the gallons consumed in that jurisdiction.
2. Multiply gallons consumed by that jurisdiction's tax rate (USD per gallon).
3. That product is the tax owed to that jurisdiction for the period.

The carrier may have already pre-paid tax at the pump. IFTA reconciles any
difference. **For this exercise we compute gross tax owed only — no prepaid
credit.**

---

## What you must build

A command-line tool called `ifta-calc` that:

1. **Reads** a CSV file of trip records (see format below).
2. **Aggregates** total miles per jurisdiction across all trips and vehicles.
3. **Computes** fuel used and tax owed per jurisdiction using a hard-coded
   jurisdiction rate table (`jurisdictions.py` — already provided).
4. **Prints** a formatted summary table to stdout.
5. **Exits** with code 0 on success, non-zero on error.

---

## Input CSV format

| Column | Type | Description |
|---|---|---|
| `trip_id` | string | Unique trip identifier |
| `vehicle_id` | string | Vehicle identifier |
| `period` | string | Reporting period, e.g. `2024-Q1` |
| `jurisdiction` | string | Two-letter jurisdiction code, e.g. `IL` |
| `miles` | float | Miles driven in this jurisdiction on this trip |

A single trip may appear on multiple rows (one per jurisdiction driven through).
A vehicle may have many trips in the same period.

See `sample_data/trips.csv` for an example.

---

## Formulas

```
fuel_used (gal)  = jurisdiction_miles / fleet_mpg
tax_owed ($)     = fuel_used * jurisdiction_tax_rate_per_gallon
```

Round `tax_owed` to **2 decimal places** (cents). Do not round intermediate values.

---

## CLI interface

```
ifta-calc --csv <path> [--mpg <float>]
```

| Argument | Required | Default | Description |
|---|---|---|---|
| `--csv` | Yes | — | Path to the trips CSV file |
| `--mpg` | No | `6.5` | Fleet average miles per gallon |

### Example output

```
IFTA Apportionment Report
Period: mixed  Vehicles: 3  Fleet MPG: 6.5
============================================================
Jurisdiction  Miles     Fuel (gal)    Tax Owed ($)
------------  --------  ------------  ------------
IA            90.0        13.85           4.50
IL          1550.0       238.46         108.50
IN           430.0        66.15          35.06
MN           120.0        18.46           5.26
MO           175.0        26.92           5.25
OH           330.0        50.77          23.86
WI           340.0        52.31          17.21
------------  --------  ------------  ------------
TOTAL        3035.0       466.92         199.64
```

*(Exact totals depend on the tax rates in `jurisdictions.py`. The values above
are illustrative.)*

---

## Acceptance criteria

| ID | Criterion |
|---|---|
| AC-1 | Single trip, single jurisdiction: fuel and tax match the formula to 2 decimal places. |
| AC-2 | Multiple trips in the same jurisdiction are correctly summed before computing tax. |
| AC-3 | Multiple vehicles' miles are pooled (apportionment is fleet-wide, not per-vehicle). |
| AC-4 | Jurisdictions not present in any trip row are omitted from output. |
| AC-5 | A jurisdiction code not in the rate table raises a clear error (not a crash). |
| AC-6 | Missing required CSV column raises a clear `ValueError`. |
| AC-7 | `--mpg` flag changes computed fuel and tax proportionally. |

---

## Module layout (skeleton provided)

```
ifta_calculator/
    __init__.py          # (empty)
    jurisdictions.py     # rate table — PROVIDED, do not change rates
    loader.py            # STUB: implement load_trips()
    calculator.py        # STUB: implement calculate()
    cli.py               # STUB: implement main()
tests/
    test_calculator.py   # AC-1 failing test — make it pass, then add the rest
sample_data/
    trips.csv            # sample input
pyproject.toml           # already configured — pip install -e .
SPEC.md                  # this file
```

---

## Suggested build order

1. Implement `load_trips()` — make it read the CSV and convert `miles` to float.
2. Implement `calculate()` — make the provided AC-1 test pass.
3. Add tests for AC-2 through AC-7.
4. Implement `main()` in `cli.py` — wire loader + calculator + print table.
5. Install and test the CLI: `pip install -e .` then `ifta-calc --csv sample_data/trips.csv`.

---

## Notes

- Use only the **standard library** (`csv`, `argparse`, `pathlib`, etc.). No third-party
  packages are needed.
- The `jurisdictions.py` module is already provided. Do not modify the rates during
  this exercise — that is intentional; Augustus will verify them separately.
- All code must run on **Python 3.11+**.
