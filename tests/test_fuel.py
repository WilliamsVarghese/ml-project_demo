"""Unit tests for fuel consumption estimation."""

import pytest
from src.fuel import calculate_fuel


def test_calculate_fuel_standard():
    # 75 km, 15 km/L, LOW traffic, GOOD road -> 75 / 15 = 5.0 L
    fuel = calculate_fuel(75.0, 15.0, traffic_level="LOW", road_condition="GOOD")
    assert pytest.approx(fuel, rel=1e-3) == 5.0


def test_calculate_fuel_with_traffic():
    # 75 km, 15 km/L, HIGH traffic (1.25x) -> 5.0 * 1.25 = 6.25 L
    fuel = calculate_fuel(75.0, 15.0, traffic_level="HIGH", road_condition="GOOD")
    assert pytest.approx(fuel, rel=1e-3) == 6.25


def test_calculate_fuel_with_road():
    # 75 km, 15 km/L, POOR road (1.10x) -> 5.0 * 1.10 = 5.50 L
    fuel = calculate_fuel(75.0, 15.0, traffic_level="LOW", road_condition="POOR")
    assert pytest.approx(fuel, rel=1e-3) == 5.50


def test_calculate_fuel_zero_efficiency():
    with pytest.raises(ValueError, match="greater than zero"):
        calculate_fuel(100.0, 0.0)


def test_calculate_fuel_negative_efficiency():
    with pytest.raises(ValueError, match="greater than zero"):
        calculate_fuel(100.0, -10.0)


def test_calculate_fuel_negative_distance():
    with pytest.raises(ValueError, match="Distance cannot be negative"):
        calculate_fuel(-50.0, 15.0)
