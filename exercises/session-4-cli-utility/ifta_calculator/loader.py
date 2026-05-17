"""
CSV loader — STUB for students to implement.

load_trips() must:
  - Accept a file path (str or Path).
  - Read the CSV using the standard-library csv module.
  - Return a list of dicts; the 'miles' field must be converted to float.
  - Raise ValueError if a required column is missing.

Required columns: trip_id, vehicle_id, period, jurisdiction, miles
"""

from __future__ import annotations
from pathlib import Path


def load_trips(csv_path: str | Path) -> list[dict]:
    """
    Load trip records from a CSV file.

    Parameters
    ----------
    csv_path : str or Path
        Path to the CSV file.

    Returns
    -------
    list[dict]
        One dict per row. 'miles' is coerced to float.

    Raises
    ------
    FileNotFoundError
        If csv_path does not exist.
    ValueError
        If a required column is absent.
    """
    raise NotImplementedError("TODO: implement load_trips()")
