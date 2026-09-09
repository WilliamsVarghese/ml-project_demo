"""Road damage extension point; no damage model is bundled with the demo."""


def summarize_damage(detections):
    """Summarize supplied detections without pretending a dataset exists."""
    counts = {}
    for detection in detections:
        label = detection.get("class", "unknown")
        counts[label] = counts.get(label, 0) + 1
    severity = min(sum(counts.values()) / 10, 1.0)
    return {"counts": counts, "severity": severity}
