"""Estimated CO2 calculations for the EcoRoute demo."""


def calculate_emissions(fuel_litres, co2_kg_per_litre):
    """Return estimated kilograms of CO2 from fuel consumed."""
    if fuel_litres < 0 or co2_kg_per_litre < 0:
        raise ValueError("Fuel and emission factors cannot be negative.")
    return fuel_litres * co2_kg_per_litre
