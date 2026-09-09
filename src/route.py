"""Route enrichment and recommendation logic."""

import pandas as pd

from .emission import calculate_emissions
from .fuel import calculate_fuel

DEFAULT_WEIGHTS = {
    "fuel": 0.30,
    "co2": 0.30,
    "time": 0.20,
    "traffic": 0.10,
    "road": 0.10,
}

TRAFFIC_SCORES = {"LOW": 0.0, "MEDIUM": 0.5, "HIGH": 1.0}
ROAD_SCORES = {"GOOD": 0.0, "MEDIUM": 0.5, "POOR": 1.0}


def _normalise(values):
    minimum, maximum = values.min(), values.max()
    if maximum == minimum:
        return pd.Series(0.0, index=values.index)
    return (values - minimum) / (maximum - minimum)


def enrich_routes(routes, vehicle, weights=None):
    """Add fuel, emissions, and a transparent eco score to route rows."""
    weights = weights or DEFAULT_WEIGHTS
    result = routes.copy()
    result["fuel_litres"] = result.apply(
        lambda row: calculate_fuel(
            row["distance_km"],
            vehicle["fuel_efficiency_km_per_litre"],
            row["traffic_level"],
            row["road_condition"],
        ),
        axis=1,
    )
    result["co2_kg"] = result["fuel_litres"].apply(
        lambda fuel: calculate_emissions(fuel, vehicle["co2_kg_per_litre"])
    )
    result["eco_score"] = (
        weights["fuel"] * _normalise(result["fuel_litres"])
        + weights["co2"] * _normalise(result["co2_kg"])
        + weights["time"] * _normalise(result["travel_time_min"])
        + weights["traffic"] * result["traffic_level"].map(TRAFFIC_SCORES)
        + weights["road"] * result["road_condition"].map(ROAD_SCORES)
    )
    return result


def route_recommendations(routes):
    """Return the fastest, lowest-fuel, lowest-CO2, and eco-score routes."""
    return {
        "fastest": routes.loc[routes["travel_time_min"].idxmin()],
        "lowest_fuel": routes.loc[routes["fuel_litres"].idxmin()],
        "lowest_co2": routes.loc[routes["co2_kg"].idxmin()],
        "eco": routes.loc[routes["eco_score"].idxmin()],
    }
