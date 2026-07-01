"""YOLO detection service — wraps StickDetector."""

from pathlib import Path
from detector.detector import StickDetector


_detector: StickDetector | None = None


def _get_detector() -> StickDetector:
    global _detector
    if _detector is None:
        model_path = str(Path(__file__).resolve().parent.parent / "weights" / "model.pt")
        _detector = StickDetector(model_path)
    return _detector


def detect_sticks(image_path: str) -> list[dict]:
    return _get_detector().detect(image_path)


def draw_detection(image_path: str, circles: list[dict]) -> bytes:
    return _get_detector().draw_to_bytes(image_path, circles)
