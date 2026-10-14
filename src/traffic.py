"""Traffic classification helpers. K-Means is optional for the demo."""

TRAFFIC_COLUMNS = ["vehicle_count", "average_speed_kmh", "traffic_density"]


def classify_demo_traffic(vehicle_count, average_speed_kmh, traffic_density):
    """Use transparent thresholds when no trained K-Means model is available."""
    if traffic_density >= 0.65 or average_speed_kmh < 40:
        return "HIGH"
    if traffic_density >= 0.45 or average_speed_kmh < 48:
        return "MEDIUM"
    return "LOW"


def train_kmeans(data, model_path=None):
    """Train K-Means and map clusters by congestion severity, not cluster id."""
    from sklearn.cluster import KMeans
    import joblib
    from pathlib import Path

    n_samples = len(data)
    if n_samples == 0:
        raise ValueError("Data cannot be empty for K-Means training.")

    n_clusters = min(3, n_samples)
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    model.fit(data[TRAFFIC_COLUMNS])
    centers = model.cluster_centers_

    max_c0 = centers[:, 0].max() if centers[:, 0].max() > 0 else 1.0
    max_c1 = centers[:, 1].max() if centers[:, 1].max() > 0 else 1.0
    severity = centers[:, 0] / max_c0 + (1 - centers[:, 1] / max_c1)
    order = severity.argsort()

    severity_names = ["LOW", "MEDIUM", "HIGH"]
    labels = {int(order[i]): severity_names[min(i, len(severity_names) - 1)] for i in range(len(order))}

    if model_path:
        path = Path(model_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({"model": model, "labels": labels}, path)
    return model, labels


def load_kmeans(model_path):
    """Load a trained K-Means model and severity label mapping from disk."""
    import joblib
    from pathlib import Path

    path = Path(model_path)
    if not path.exists():
        return None, None
    saved = joblib.load(path)
    return saved.get("model"), saved.get("labels")


def predict_traffic_kmeans(model, labels, vehicle_count, average_speed_kmh, traffic_density):
    """Predict traffic congestion level using trained K-Means, falling back to heuristics."""
    if model is None or labels is None:
        return classify_demo_traffic(vehicle_count, average_speed_kmh, traffic_density)
    
    import pandas as pd
    features = pd.DataFrame([[vehicle_count, average_speed_kmh, traffic_density]], columns=TRAFFIC_COLUMNS)
    cluster = int(model.predict(features)[0])
    return labels.get(cluster, "MEDIUM")

