"""Jurisdiction rate table.

PLACEHOLDER RATES AND SURCHARGES — illustrative values for training only.
Real IFTA rates and surcharges are set quarterly by each jurisdiction and
must be obtained from the official IFTA rate matrix for the relevant fuel type.
"""

JURISDICTIONS: dict[str, dict] = {
    "IA": {"name": "Iowa",       "rate_per_gallon": 0.325, "surcharge_per_gallon": 0.000},
    "IL": {"name": "Illinois",   "rate_per_gallon": 0.455, "surcharge_per_gallon": 0.000},
    "IN": {"name": "Indiana",    "rate_per_gallon": 0.530, "surcharge_per_gallon": 0.110},
    "KY": {"name": "Kentucky",   "rate_per_gallon": 0.246, "surcharge_per_gallon": 0.044},
    "MN": {"name": "Minnesota",  "rate_per_gallon": 0.285, "surcharge_per_gallon": 0.000},
    "MO": {"name": "Missouri",   "rate_per_gallon": 0.195, "surcharge_per_gallon": 0.000},
    "OH": {"name": "Ohio",       "rate_per_gallon": 0.470, "surcharge_per_gallon": 0.000},
    "VA": {"name": "Virginia",   "rate_per_gallon": 0.262, "surcharge_per_gallon": 0.035},
    "WI": {"name": "Wisconsin",  "rate_per_gallon": 0.329, "surcharge_per_gallon": 0.000},
    "ON": {"name": "Ontario",    "rate_per_gallon": 0.143, "surcharge_per_gallon": 0.000},
    "QC": {"name": "Quebec",     "rate_per_gallon": 0.202, "surcharge_per_gallon": 0.000},
}


def get_rate(code: str) -> float:
    return JURISDICTIONS[code.upper()]["rate_per_gallon"]


def get_surcharge(code: str) -> float:
    return JURISDICTIONS[code.upper()]["surcharge_per_gallon"]


def get_name(code: str) -> str:
    return JURISDICTIONS[code.upper()]["name"]
