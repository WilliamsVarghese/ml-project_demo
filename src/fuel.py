"""Fuel consumption estimates for the EcoRoute demo."""

TRAFFIC_FACTORS = {"LOW": 1.00, "MEDIUM": 1.10, "HIGH": 1.25}
ROAD_FACTORS = {"GOOD": 1.00, "MEDIUM": 1.05, "POOR": 1.10}


def calculate_fuel(distance_km, efficiency_km_per_litre, traffic_level="LOW", road_condition="GOOD"):
    """Estimate litres (or energy units) used, including traffic and road adjustments."""
    if distance_km < 0:
        raise ValueError("Distance cannot be negative.")
    if efficiency_km_per_litre <= 0:
        raise ValueError("Fuel efficiency must be greater than zero.")

    base_fuel = distance_km / efficiency_km_per_litre
    traffic_factor = TRAFFIC_FACTORS.get(str(traffic_level).upper(), 1.0)
    road_factor = ROAD_FACTORS.get(str(road_condition).upper(), 1.0)
    return base_fuel * traffic_factor * road_factor

