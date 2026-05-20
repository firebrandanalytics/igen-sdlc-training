"""IFTA apportionment calculator."""

from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from typing import TypedDict

from ifta_calculator.jurisdictions import (
    JURISDICTIONS,
    get_name,
    get_rate,
    get_surcharge,
)

_CENT = Decimal("0.01")


class JurisdictionResult(TypedDict):
    jurisdiction: str
    name: str
    miles: float
    fuel_used: float
    tax_owed: float


def calculate(
    trips: list[dict],
    fleet_mpg: float,
) -> list[JurisdictionResult]:
    """Compute IFTA tax owed per jurisdiction from a list of trip records."""
    if fleet_mpg <= 0:
        raise ValueError(f"fleet_mpg must be positive, got {fleet_mpg}")

    miles_by_jurisdiction: dict[str, float] = defaultdict(float)
    for trip in trips:
        code = trip["jurisdiction"].upper()
        if code not in JURISDICTIONS:
            raise ValueError(
                f"Jurisdiction code {code!r} is not in the rate table. "
                f"Known codes: {sorted(JURISDICTIONS)}"
            )
        miles_by_jurisdiction[code] += float(trip["miles"])

    results: list[JurisdictionResult] = []
    for code in sorted(miles_by_jurisdiction):
        miles = miles_by_jurisdiction[code]
        fuel_used = miles / fleet_mpg
        effective_rate = get_rate(code) + get_surcharge(code)
        tax_decimal = Decimal(str(fuel_used)) * Decimal(str(effective_rate))
        tax_owed = float(tax_decimal.quantize(_CENT, rounding=ROUND_HALF_UP))
        results.append(
            JurisdictionResult(
                jurisdiction=code,
                name=get_name(code),
                miles=miles,
                fuel_used=fuel_used,
                tax_owed=tax_owed,
            )
        )

    return results
