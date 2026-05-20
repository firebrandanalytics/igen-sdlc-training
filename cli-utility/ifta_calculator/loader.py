"""CSV loader for IFTA trip records."""

from __future__ import annotations

import csv
from pathlib import Path

REQUIRED_COLUMNS = {"trip_id", "vehicle_id", "period", "jurisdiction", "miles"}


def load_trips(csv_path: str | Path) -> list[dict]:
    """Load trip records from a CSV file.

    Coerces 'miles' to float; uppercases the jurisdiction code. Raises
    FileNotFoundError if the file is missing, ValueError if any required column
    is absent or if a 'miles' value cannot be parsed as float.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)

        if reader.fieldnames is None:
            raise ValueError(f"CSV file is empty or has no header: {path}")
        reader.fieldnames = [col.strip() for col in reader.fieldnames]

        actual = set(reader.fieldnames)
        missing = REQUIRED_COLUMNS - actual
        if missing:
            raise ValueError(
                f"CSV is missing required columns: {sorted(missing)}. "
                f"Found: {sorted(actual)}"
            )

        trips: list[dict] = []
        for i, row in enumerate(reader, start=2):
            raw_miles = row["miles"].strip()
            try:
                miles = float(raw_miles)
            except ValueError:
                raise ValueError(
                    f"Row {i}: cannot convert miles={raw_miles!r} to float."
                )
            trips.append(
                {
                    "trip_id": row["trip_id"].strip(),
                    "vehicle_id": row["vehicle_id"].strip(),
                    "period": row["period"].strip(),
                    "jurisdiction": row["jurisdiction"].strip().upper(),
                    "miles": miles,
                }
            )

    return trips
