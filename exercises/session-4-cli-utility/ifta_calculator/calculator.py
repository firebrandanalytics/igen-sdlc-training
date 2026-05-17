"""
IFTA apportionment calculator — STUB for students to implement.

The calculate() function must:
  1. Accept a list of trip records (dicts with keys: trip_id, vehicle_id,
     period, jurisdiction, miles).
  2. Compute total fleet miles across all jurisdictions.
  3. For each jurisdiction, compute:
       - jurisdiction_miles  : sum of miles driven in that jurisdiction
       - fuel_used           : jurisdiction_miles / fleet_mpg
       - tax_owed            : fuel_used * tax_rate_per_gallon
     Round tax_owed to 2 decimal places (cents).
  4. Return a list of JurisdictionResult dicts (see type below).

You may add helper functions and modules as you see fit.
Do NOT modify the function signature.
"""

from __future__ import annotations
from typing import TypedDict


class JurisdictionResult(TypedDict):
    jurisdiction: str        # two-letter code, e.g. "IL"
    name: str                # human-readable name, e.g. "Illinois"
    miles: float             # miles driven in this jurisdiction
    fuel_used: float         # gallons consumed (miles / fleet_mpg)
    tax_owed: float          # USD, rounded to cents


def calculate(
    trips: list[dict],
    fleet_mpg: float,
) -> list[JurisdictionResult]:
    """
    Compute IFTA tax owed per jurisdiction.

    Parameters
    ----------
    trips : list[dict]
        Rows loaded from the trips CSV. Each dict has at minimum:
            jurisdiction (str), miles (float or int).
    fleet_mpg : float
        Fleet average miles per gallon. Used to compute fuel consumed
        in each jurisdiction.

    Returns
    -------
    list[JurisdictionResult]
        One entry per jurisdiction, sorted by jurisdiction code.
    """
    raise NotImplementedError("TODO: implement calculate()")
