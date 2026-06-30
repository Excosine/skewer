"""Stick detection via YOLO."""

import cv2
import numpy as np
from pathlib import Path


class StickDetector:
    """Detect bamboo sticks in a top-down image using YOLO.

    Usage
    -----
        detector = StickDetector("weights/model.pt")
        count = detector.count("sample.png")
        circles = detector.detect("sample.png")
        detector.draw("sample.png", circles, "output.png")
    """

    def __init__(self, model_path: str | None = None):
        if model_path is None:
            model_path = _default_model()
        if model_path is None or not Path(model_path).exists():
            raise FileNotFoundError(
                f"Model not found. Place model.pt in models/ or pass model_path."
            )
        self._model_path = model_path

    def count(self, image_path: str, conf: float = 0.25) -> int:
        """Return the number of sticks in the image."""
        return len(self.detect(image_path, conf=conf))

    def detect(self, image_path: str, conf: float = 0.25) -> list[dict]:
        """Return a list of detected sticks.

        Each stick is a dict with keys: cx, cy, r, score.
        """
        from ultralytics import YOLO

        model = YOLO(self._model_path)
        results = model(image_path, conf=conf, device=1, verbose=False)
        boxes = results[0].boxes
        if boxes is None:
            return []

        xywh = boxes.xywh.cpu().numpy()
        confs = boxes.conf.cpu().numpy()

        circles = []
        for (x, y, w, h), c in zip(xywh, confs):
            r = int(max(w, h) / 2)
            circles.append({"cx": int(x), "cy": int(y), "r": r, "score": float(c)})
        return circles

    def draw(
        self,
        image_path: str,
        circles: list[dict] | None = None,
        output_path: str | None = None,
        conf: float = 0.25,
    ) -> None:
        """Draw detected circles on the image and save."""
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Cannot read image: {image_path}")

        if circles is None:
            circles = self.detect(image_path, conf=conf)

        max_score = max(c["score"] for c in circles) if circles else 1
        for c in circles:
            ratio = max(0.4, min(1.0, c["score"] / max_score))
            cv2.circle(
                img, (c["cx"], c["cy"]), c["r"],
                (0, int(255 * ratio), 0), 2,
            )
            cv2.circle(img, (c["cx"], c["cy"]), 2, (0, 0, 255), 3)

        out = output_path or str(Path(image_path).parent / "debug_output.png")
        cv2.imwrite(out, img)


def count_sticks(image_path: str, model_path: str | None = None) -> int:
    """Convenience function: count sticks in an image."""
    return StickDetector(model_path).count(image_path)


def _default_model() -> str | None:
    candidates = [
        str(Path(__file__).resolve().parent.parent / "models" / "model.pt"),
    ]
    for p in candidates:
        if Path(p).exists():
            return p
    return None
