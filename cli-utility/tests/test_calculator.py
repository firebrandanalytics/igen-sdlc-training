"""Behavioural tests for the IFTA apportionment calculator.

Each test documents one rule the calculator enforces. Reading the asserts
should tell you what the calculator does, not just that it works.
"""

import pytest
from ifta_calculator.calculator import calculate


def _trip(jurisdiction, miles, period="2024-Q1", vehicle="TRUCK-01", tid="T001"):
    return {
        "trip_id": tid,
        "vehicle_id": vehicle,
        "period": period,
        "jurisdiction": jurisdiction,
        "miles": miles,
    }


def test_single_trip_single_jurisdiction():
    """Plain case: one trip, one non-surcharge jurisdiction."""
    results = calculate([_trip("IL", 100.0)], fleet_mpg=6.5)
    assert len(results) == 1
    row = results[0]
    assert row["jurisdiction"] == "IL"
    assert row["name"] == "Illinois"
    assert row["miles"] == pytest.approx(100.0)
    # 100 / 6.5 = 15.3846... gal; 15.3846 * 0.455 = 6.9999... -> $7.00
    assert row["fuel_used"] == pytest.approx(15.3846, abs=1e-4)
    assert row["tax_owed"] == pytest.approx(7.00)


def test_surcharge_added_on_top_of_base_rate():
    """Surcharge jurisdictions (IN, KY, VA) charge base + surcharge per gallon.

    Indiana: base 0.530 + surcharge 0.110 = effective 0.640 $/gal.
    100 mi / 6.5 mpg = 15.3846 gal; 15.3846 * 0.640 = 9.846... -> $9.85.
    """
    results = calculate([_trip("IN", 100.0)], fleet_mpg=6.5)
    assert results[0]["tax_owed"] == pytest.approx(9.85)


def test_kentucky_surcharge():
    """Kentucky has a surcharge: base 0.246 + 0.044 = 0.290 effective."""
    # 100 / 6.5 * 0.290 = 4.4615... -> $4.46
    results = calculate([_trip("KY", 100.0)], fleet_mpg=6.5)
    assert results[0]["tax_owed"] == pytest.approx(4.46)


def test_non_surcharge_jurisdiction_charges_base_rate_only():
    # 100 / 6.5 * 0.470 = 7.2307... -> $7.23
    results = calculate([_trip("OH", 100.0)], fleet_mpg=6.5)
    assert results[0]["tax_owed"] == pytest.approx(7.23)


def test_apportionment_is_fleet_wide_not_per_vehicle():
    """Multiple vehicles' miles in the same jurisdiction are pooled before computing."""
    trips = [
        _trip("IL", 50.0, vehicle="TRUCK-01", tid="T001"),
        _trip("IL", 50.0, vehicle="TRUCK-02", tid="T002"),
    ]
    results = calculate(trips, fleet_mpg=6.5)
    assert len(results) == 1
    assert results[0]["miles"] == pytest.approx(100.0)


def test_trips_are_aggregated_across_periods_silently():
    """The calculator does not filter by period. Trips from multiple reporting
    quarters in the same input contribute to a single combined report.
    """
    trips = [
        _trip("IL", 50.0, period="2024-Q1"),
        _trip("IL", 50.0, period="2024-Q2"),
    ]
    results = calculate(trips, fleet_mpg=6.5)
    assert len(results) == 1
    assert results[0]["miles"] == pytest.approx(100.0)


def test_canadian_provinces_supported():
    """Two-letter codes include Canadian provinces (ON, QC) alongside US states."""
    results = calculate([_trip("ON", 100.0)], fleet_mpg=6.5)
    assert results[0]["jurisdiction"] == "ON"
    assert results[0]["name"] == "Ontario"


def test_results_sorted_by_jurisdiction_code():
    trips = [_trip("WI", 50.0), _trip("IL", 50.0), _trip("IN", 50.0)]
    results = calculate(trips, fleet_mpg=6.5)
    assert [r["jurisdiction"] for r in results] == ["IL", "IN", "WI"]


def test_empty_trips_returns_empty_result():
    assert calculate([], fleet_mpg=6.5) == []


def test_jurisdiction_code_is_case_insensitive():
    results = calculate([_trip("il", 100.0)], fleet_mpg=6.5)
    assert results[0]["jurisdiction"] == "IL"


def test_unknown_jurisdiction_raises_clear_error():
    with pytest.raises(ValueError, match="ZZ"):
        calculate([_trip("ZZ", 100.0)], fleet_mpg=6.5)


def test_zero_or_negative_mpg_rejected():
    with pytest.raises(ValueError, match="fleet_mpg"):
        calculate([_trip("IL", 100.0)], fleet_mpg=0)
    with pytest.raises(ValueError, match="fleet_mpg"):
        calculate([_trip("IL", 100.0)], fleet_mpg=-1)
