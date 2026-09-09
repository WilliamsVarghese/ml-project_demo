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

    model = KMeans(n_clusters=3, random_state=42, n_init=10)
    model.fit(data[TRAFFIC_COLUMNS])
    centers = model.cluster_centers_
    severity = centers[:, 0] / centers[:, 0].max() + (1 - centers[:, 1] / centers[:, 1].max())
    order = severity.argsort()
    labels = {int(order[0]): "LOW", int(order[1]): "MEDIUM", int(order[2]): "HIGH"}
    if model_path:
        joblib.dump({"model": model, "labels": labels}, model_path)
    return model, labels
