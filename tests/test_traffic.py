"""Unit tests for traffic classification and unsupervised K-Means clustering."""

import pandas as pd
import pytest
from src.traffic import (
    classify_demo_traffic,
    load_kmeans,
    predict_traffic_kmeans,
    train_kmeans,
)


def test_classify_demo_traffic():
    assert classify_demo_traffic(1000, 35, 0.75) == "HIGH"
    assert classify_demo_traffic(600, 45, 0.50) == "MEDIUM"
    assert classify_demo_traffic(400, 60, 0.25) == "LOW"


def test_train_and_predict_kmeans(tmp_path):
    data = pd.DataFrame([
        {"vehicle_count": 400, "average_speed_kmh": 60, "traffic_density": 0.25},
        {"vehicle_count": 700, "average_speed_kmh": 45, "traffic_density": 0.50},
        {"vehicle_count": 1100, "average_speed_kmh": 30, "traffic_density": 0.80},
    ])

    model_file = tmp_path / "traffic_model.joblib"
    model, labels = train_kmeans(data, model_path=model_file)

    assert model is not None
    assert len(labels) == 3
    assert model_file.exists()

    # Test loading from disk
    loaded_model, loaded_labels = load_kmeans(model_file)
    assert loaded_model is not None
    assert loaded_labels == labels

    # Prediction
    pred = predict_traffic_kmeans(loaded_model, loaded_labels, 420, 58, 0.28)
    assert pred in ["LOW", "MEDIUM", "HIGH"]
