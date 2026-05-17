"""
Jurisdiction tax-rate table.

PLACEHOLDER RATES — these are illustrative values used for training only.
Real IFTA rates change quarterly and vary by fuel type.
Augustus: please verify / replace before any live use.

Each entry:
    key   : two-letter jurisdiction code (IFTA standard)
    name  : human-readable name
    rate  : tax rate in USD per gallon (placeholder)
"""

# [Needs Tech Review] — rates are illustrative placeholders only.
JURISDICTIONS: dict[str, dict] = {
    "IL": {"name": "Illinois",   "rate_per_gallon": 0.455},
    "IN": {"name": "Indiana",    "rate_per_gallon": 0.530},
    "OH": {"name": "Ohio",       "rate_per_gallon": 0.470},
    "WI": {"name": "Wisconsin",  "rate_per_gallon": 0.329},
    "MN": {"name": "Minnesota",  "rate_per_gallon": 0.285},
    "MO": {"name": "Missouri",   "rate_per_gallon": 0.195},
    "IA": {"name": "Iowa",       "rate_per_gallon": 0.325},
}


def get_rate(jurisdiction_code: str) -> float:
    """Return the tax rate (USD/gallon) for the given jurisdiction code.

    Raises KeyError if the code is not in the table.
    """
    return JURISDICTIONS[jurisdiction_code.upper()]["rate_per_gallon"]
