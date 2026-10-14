"""Unit tests for route enrichment and multi-criteria recommendations."""

import pandas as pd
import pytest
from src.route import enrich_routes, route_recommendations


@pytest.fixture
def sample_routes():
    return pd.DataFrame([
        {
            "route_id": "R1",
            "source": "Kochi",
            "destination": "Thrissur",
            "route_name": "Highway Corridor",
            "distance_km": 78.0,
            "travel_time_min": 95.0,
            "traffic_level": "LOW",
            "road_condition": "GOOD",
        },
        {
            "route_id": "R2",
            "source": "Kochi",
            "destination": "Thrissur",
            "route_name": "Scenic Detour",
            "distance_km": 82.0,
            "travel_time_min": 115.0,
            "traffic_level": "MEDIUM",
            "road_condition": "GOOD",
        },
        {
            "route_id": "R3",
            "source": "Kochi",
            "destination": "Thrissur",
            "route_name": "Coastal Alternative",
            "distance_km": 86.0,
            "travel_time_min": 125.0,
            "traffic_level": "HIGH",
            "road_condition": "POOR",
        },
    ])


@pytest.fixture
def sample_vehicle():
    return pd.Series({
        "vehicle_type": "Petrol Car",
        "fuel_efficiency_km_per_litre": 15.0,
        "co2_kg_per_litre": 2.31,
    })


def test_enrich_routes(sample_routes, sample_vehicle):
    enriched = enrich_routes(sample_routes, sample_vehicle)
    assert "fuel_litres" in enriched.columns
    assert "co2_kg" in enriched.columns
    assert "eco_score" in enriched.columns
    assert len(enriched) == 3

    # R1 should have lower fuel consumption than R2 and R3
    assert enriched.loc[enriched["route_id"] == "R1", "fuel_litres"].iloc[0] < \
           enriched.loc[enriched["route_id"] == "R2", "fuel_litres"].iloc[0]


def test_route_recommendations(sample_routes, sample_vehicle):
    enriched = enrich_routes(sample_routes, sample_vehicle)
    recs = route_recommendations(enriched)

    # All required recommendation categories must be present
    assert "shortest" in recs
    assert "fastest" in recs
    assert "lowest_fuel" in recs
    assert "lowest_co2" in recs
    assert "eco" in recs

    # R1 is shortest (78 km) and fastest (95 min)
    assert recs["shortest"]["route_id"] == "R1"
    assert recs["fastest"]["route_id"] == "R1"
    assert recs["eco"]["route_id"] == "R1"


def test_enrich_routes_empty(sample_vehicle):
    empty_df = pd.DataFrame()
    enriched = enrich_routes(empty_df, sample_vehicle)
    assert enriched.empty
    assert route_recommendations(enriched) == {}
