"""YOLO detection service — wraps StickDetector (lazy import)."""

from pathlib import Path

_detector = None


def _get_detector():
    global _detector
    if _detector is None:
        from detector.detector import StickDetector
        model_path = str(Path(__file__).resolve().parent.parent / "weights" / "model.pt")
        _detector = StickDetector(model_path)
    return _detector


def detect_sticks(image_path: str) -> list[dict]:
    return _get_detector().detect(image_path)
