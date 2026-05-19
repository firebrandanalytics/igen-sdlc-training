> **Self-study take-home reference.** This CLI exercise is a worked greenfield
> full-SDLC example — requirements through packaging — for you to explore at your
> own pace. It is not part of the in-class session. Work through as much or as
> little as is useful to you.

# IFTA Fuel-Tax Calculator — Self-Study Reference

Build a command-line tool that computes IFTA fuel-tax apportionment from a CSV of
trip mileage records. Full requirements are in [SPEC.md](SPEC.md).

---

## Quick start

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

`cli.py` is a stub — it raises `NotImplementedError` until you implement it. Once
you have built the calculator, verify it with:

```bash
ifta-calc --csv sample_data/trips.csv --mpg 6.5
```

---

## Running tests

```bash
pytest
```

The provided test in `tests/test_calculator.py` **fails** until you implement
`calculate()`. That is intentional — it encodes the first acceptance criterion.

---

## Project layout

```
ifta_calculator/
    __init__.py
    jurisdictions.py   # rate table (provided)
    loader.py          # TODO: implement load_trips()
    calculator.py      # TODO: implement calculate()
    cli.py             # TODO: implement main()
tests/
    test_calculator.py # one failing test — make it pass
sample_data/
    trips.csv          # sample input
SPEC.md                # full requirements & acceptance criteria
```

---

## Key rules

- Standard library only — no third-party packages.
- Round `tax_owed` to 2 decimal places (cents).
- Fleet MPG applies uniformly across all jurisdictions.
- See SPEC.md for the complete list of acceptance criteria.
