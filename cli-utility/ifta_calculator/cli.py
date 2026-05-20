"""CLI entry point for the IFTA fuel-tax calculator."""

from __future__ import annotations

import argparse
import sys

from ifta_calculator.calculator import calculate
from ifta_calculator.loader import load_trips


def _print_report(
    results: list[dict],
    fleet_mpg: float,
    trips: list[dict],
) -> None:
    periods = sorted({t["period"] for t in trips})
    period_str = ", ".join(periods) if periods else "—"
    vehicles = {t["vehicle_id"] for t in trips}

    print("IFTA Apportionment Report")
    print(
        f"Period: {period_str}  "
        f"Vehicles: {len(vehicles)}  "
        f"Fleet MPG: {fleet_mpg}"
    )
    print("=" * 62)

    col_widths = (12, 10, 14, 14)
    header = (
        f"{'Jurisdiction':<{col_widths[0]}}"
        f"{'Miles':>{col_widths[1]}}"
        f"{'Fuel (gal)':>{col_widths[2]}}"
        f"{'Tax Owed ($)':>{col_widths[3]}}"
    )
    separator = (
        f"{'-' * col_widths[0]}"
        f"  {'-' * col_widths[1]}"
        f"  {'-' * (col_widths[2] - 2)}"
        f"  {'-' * (col_widths[3] - 2)}"
    )
    print(header)
    print(separator)

    total_miles = 0.0
    total_fuel = 0.0
    total_tax = 0.0

    for row in results:
        miles = row["miles"]
        fuel = row["fuel_used"]
        tax = row["tax_owed"]
        total_miles += miles
        total_fuel += fuel
        total_tax += tax
        print(
            f"{row['jurisdiction']:<{col_widths[0]}}"
            f"{miles:>{col_widths[1]}.1f}"
            f"{fuel:>{col_widths[2]}.2f}"
            f"{tax:>{col_widths[3]}.2f}"
        )

    print(separator)
    print(
        f"{'TOTAL':<{col_widths[0]}}"
        f"{total_miles:>{col_widths[1]}.1f}"
        f"{total_fuel:>{col_widths[2]}.2f}"
        f"{round(total_tax, 2):>{col_widths[3]}.2f}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ifta-calc",
        description="Compute IFTA fuel-tax apportionment from trip mileage data.",
    )
    parser.add_argument("--csv", required=True, help="Path to the trips CSV file.")
    parser.add_argument(
        "--mpg",
        type=float,
        default=6.5,
        help="Fleet average miles per gallon (default: 6.5).",
    )
    args = parser.parse_args()

    if args.mpg <= 0:
        print(f"Error: --mpg must be positive, got {args.mpg}", file=sys.stderr)
        sys.exit(1)

    try:
        trips = load_trips(args.csv)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        print(f"Error reading CSV: {exc}", file=sys.stderr)
        sys.exit(1)

    if not trips:
        print("No trip records found in the CSV file.", file=sys.stderr)
        sys.exit(1)

    try:
        results = calculate(trips=trips, fleet_mpg=args.mpg)
    except ValueError as exc:
        print(f"Calculation error: {exc}", file=sys.stderr)
        sys.exit(1)

    _print_report(results, fleet_mpg=args.mpg, trips=trips)


if __name__ == "__main__":
    main()
