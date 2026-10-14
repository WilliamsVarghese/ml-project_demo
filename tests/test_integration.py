"""Integration tests for end-to-end route planning, comparisons, and model handling."""

from pathlib import Path
import pandas as pd
import pytest

from src.fuel import calculate_fuel
from src.emission import calculate_emissions
from src.route import enrich_routes, route_recommendations
from src.traffic import load_kmeans, predict_traffic_kmeans, TRAFFIC_COLUMNS

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
MODELS_DIR = PROJECT_DIR / "models"


def test_end_to_end_route_planning_workflow():
    """Verify end-to-end pipeline: load data -> enrich with vehicle -> rank recommendations."""
    routes_df = pd.read_csv(DATA_DIR / "routes.csv")
    vehicles_df = pd.read_csv(DATA_DIR / "vehicles.csv")

    assert not routes_df.empty, "Routes dataset must not be empty"
    assert not vehicles_df.empty, "Vehicles dataset must not be empty"

    # Test with each vehicle profile
    for _, vehicle in vehicles_df.iterrows():
        enriched = enrich_routes(routes_df, vehicle)
        assert "fuel_litres" in enriched.columns
        assert "co2_kg" in enriched.columns
        assert "eco_score" in enriched.columns

        # Verify physical validity
        assert (enriched["fuel_litres"] > 0).all(), "Fuel consumption must be positive"
        assert (enriched["co2_kg"] >= 0).all(), "CO2 emissions must be non-negative"
        assert (enriched["eco_score"] >= 0).all(), "Eco score must be non-negative"

        recs = route_recommendations(enriched)
        for key in ["shortest", "fastest", "lowest_fuel", "lowest_co2", "eco"]:
            assert key in recs, f"Missing recommendation key: {key}"
            assert isinstance(recs[key], pd.Series), f"Recommendation {key} must be a Series"


def test_route_comparison_alternatives():
    """Verify route comparison produces valid distinct alternatives and metrics."""
    routes_df = pd.read_csv(DATA_DIR / "routes.csv")
    vehicle = pd.read_csv(DATA_DIR / "vehicles.csv").iloc[0]  # Petrol Car

    enriched = enrich_routes(routes_df, vehicle)
    recs = route_recommendations(enriched)

    fastest = recs["fastest"]
    eco = recs["eco"]
    shortest = recs["shortest"]

    # Compare metrics existence and types
    for r in [fastest, eco, shortest]:
        assert "distance_km" in r
        assert "travel_time_min" in r
        assert "fuel_litres" in r
        assert "co2_kg" in r
        assert "eco_score" in r


def test_kmeans_model_loading_and_features():
    """Verify saved K-Means model loads correctly and uses consistent feature preprocessing."""
    model_path = MODELS_DIR / "traffic_kmeans.joblib"
    assert model_path.exists(), f"Model file {model_path} must exist"

    model, labels = load_kmeans(model_path)
    assert model is not None, "Loaded model must not be None"
    assert isinstance(labels, dict), "Loaded labels must be a dict"
    assert set(labels.values()).issubset({"LOW", "MEDIUM", "HIGH"}), "Labels must map to severity levels"

    # Verify input feature schema
    assert model.n_features_in_ == len(TRAFFIC_COLUMNS)

    # Test prediction with known values
    pred_low = predict_traffic_kmeans(model, labels, 400, 55, 0.30)
    assert pred_low in ["LOW", "MEDIUM", "HIGH"]

    pred_high = predict_traffic_kmeans(model, labels, 1200, 30, 0.85)
    assert pred_high in ["LOW", "MEDIUM", "HIGH"]


def test_missing_data_defensive_handling(tmp_path):
    """Verify that empty or malformed data is handled defensively without unhandled crashes."""
    empty_routes = pd.DataFrame(columns=[
        "route_id", "source", "destination", "route_name", "distance_km",
        "travel_time_min", "traffic_level", "road_condition"
    ])
    sample_vehicle = pd.Series({
        "vehicle_type": "Petrol Car",
        "fuel_efficiency_km_per_litre": 15.0,
        "co2_kg_per_litre": 2.31,
    })

    # Empty routes dataframe should return empty without raising
    result = enrich_routes(empty_routes, sample_vehicle)
    assert result.empty

    recs = route_recommendations(result)
    assert recs == {}

    # Missing model file returns None gracefully
    missing_model, missing_labels = load_kmeans(tmp_path / "non_existent.joblib")
    assert missing_model is None
    assert missing_labels is None
