"""
CLI entry point — STUB for students to implement.

When complete, running:

    ifta-calc --csv trips.csv --mpg 6.5

should print a table like:

    Jurisdiction  Miles    Fuel Used (gal)  Tax Owed ($)
    ------------  -------  ---------------  ------------
    IA            90.0       13.85              4.50
    IL            1550.0    238.46            108.50
    ...
    TOTAL         3035.0    466.92            227.43

See SPEC.md for the full output format and edge-case requirements.
"""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ifta-calc",
        description="Compute IFTA fuel-tax apportionment from trip mileage data.",
    )
    parser.add_argument("--csv", required=True, help="Path to trips CSV file.")
    parser.add_argument(
        "--mpg",
        type=float,
        default=6.5,
        help="Fleet average miles per gallon (default: 6.5).",
    )
    args = parser.parse_args()

    # TODO: call load_trips(), then calculate(), then print the results table.
    raise NotImplementedError("TODO: implement main()")


if __name__ == "__main__":
    main()
