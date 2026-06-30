"""Command-line entry point for stick counting."""

import argparse
import sys

from .detector import StickDetector


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Count bamboo sticks in a top-down image",
    )
    parser.add_argument("image", help="Path to the input image")
    parser.add_argument("--model", type=str, default=None,
                        help="YOLO model path (auto-detected if omitted)")
    parser.add_argument("--conf", type=float, default=0.25,
                        help="Confidence threshold (default: 0.25)")
    parser.add_argument("--debug", action="store_true",
                        help="Save annotated debug image")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON with positions and scores")
    args = parser.parse_args(argv)

    detector = StickDetector(args.model)
    circles = detector.detect(args.image, conf=args.conf)
    count = len(circles)

    if args.debug:
        detector.draw(args.image, circles)

    if args.json:
        import json
        json.dump({"count": count, "circles": circles}, sys.stdout, indent=2)
    else:
        print(count)
