"""Unit tests for CO2 emissions estimation."""

import pytest
from src.emission import calculate_emissions


def test_calculate_emissions_petrol():
    # 10 Litres * 2.31 kg/L = 23.1 kg CO2
    co2 = calculate_emissions(10.0, 2.31)
    assert pytest.approx(co2, rel=1e-3) == 23.1


def test_calculate_emissions_zero_fuel():
    co2 = calculate_emissions(0.0, 2.31)
    assert co2 == 0.0


def test_calculate_emissions_electric():
    # EV tailpipe factor is 0.00
    co2 = calculate_emissions(15.0, 0.00)
    assert co2 == 0.0


def test_calculate_emissions_negative_inputs():
    with pytest.raises(ValueError, match="cannot be negative"):
        calculate_emissions(-5.0, 2.31)

    with pytest.raises(ValueError, match="cannot be negative"):
        calculate_emissions(10.0, -1.0)
