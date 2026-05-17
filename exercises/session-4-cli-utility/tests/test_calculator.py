"""
Acceptance test for the IFTA calculator — first criterion.

This test MUST FAIL before students implement calculate().
It MUST PASS once calculate() is correctly implemented.

Criterion AC-1:
    Given a single trip of 100 miles in Illinois (IL) at 6.5 mpg,
    the calculator must return exactly one jurisdiction result for IL
    with:
        - miles == 100.0
        - fuel_used rounded to 2dp == 15.38   (100 / 6.5 = 15.384...)
        - tax_owed rounded to 2dp == 7.00      (15.384... * 0.455 = 6.999... -> $7.00)

Note: the expected tax_owed value above uses the PLACEHOLDER rate for IL
(0.455 $/gal). Augustus will verify this rate during tech review.
"""

import pytest
from ifta_calculator.calculator import calculate


SINGLE_IL_TRIP = [
    {
        "trip_id": "T001",
        "vehicle_id": "TRUCK-01",
        "period": "2024-Q1",
        "jurisdiction": "IL",
        "miles": 100.0,
    }
]


def test_ac1_single_jurisdiction_tax_owed():
    """AC-1: single trip, single jurisdiction, correct fuel and tax computation."""
    results = calculate(trips=SINGLE_IL_TRIP, fleet_mpg=6.5)

    assert len(results) == 1, "Expected exactly one jurisdiction result"

    row = results[0]
    assert row["jurisdiction"] == "IL"
    assert row["miles"] == pytest.approx(100.0)
    assert round(row["fuel_used"], 2) == pytest.approx(15.38)
    assert round(row["tax_owed"], 2) == pytest.approx(7.00)
