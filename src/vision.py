"""Optional YOLO vehicle detection integration."""

VEHICLE_CLASSES = {"car", "truck", "bus", "motorcycle", "bicycle"}


def detect_vehicles(image, model_name="yolo11n.pt"):
    """Detect vehicles with Ultralytics when installed and weights are available."""
    from ultralytics import YOLO

    model = YOLO(model_name)
    result = model(image, verbose=False)[0]
    detections = []
    for box in result.boxes:
        class_name = result.names[int(box.cls[0])]
        if class_name in VEHICLE_CLASSES:
            detections.append({
                "class": class_name,
                "confidence": float(box.conf[0]),
                "box": [float(value) for value in box.xyxy[0]],
            })
    return detections
