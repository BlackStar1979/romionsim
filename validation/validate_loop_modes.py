import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def fail(msg: str) -> Tuple[bool, str]:
    return False, msg


def ok(msg: str) -> Tuple[bool, str]:
    return True, msg


def validate_loop_mode(
    rows: List[Dict[str, Any]],
    expected_projection_regime: str,
    expected_loop_detection_regime: str | None,
    min_loop_count: int | None,
) -> Tuple[bool, str]:
    ticks = [row for row in rows if row.get("type") == "TICK"]
    if not ticks:
        return fail("no TICK events found")

    for tick_event in ticks:
        fracture = tick_event.get("fracture")
        if not isinstance(fracture, dict):
            return fail("TICK fracture payload missing")

        projection_regime = fracture.get("projection_regime")
        loop_detection_regime = fracture.get("loop_detection_regime")

        if expected_projection_regime == "legacy_visible_only":
            if projection_regime is not None:
                return fail("legacy run should not emit projection_regime")
            if loop_detection_regime is not None:
                return fail("legacy run should not emit loop_detection_regime")
            for key in [
                "loop_count",
                "max_loop_length",
                "min_loop_length",
                "mean_loop_length",
                "loop_edge_coverage_ratio",
            ]:
                if key in fracture:
                    return fail(f"legacy run should not emit {key}")
            continue

        if projection_regime != expected_projection_regime:
            return fail(
                f"expected projection_regime={expected_projection_regime}, got {projection_regime}"
            )
        if expected_loop_detection_regime is not None and loop_detection_regime != expected_loop_detection_regime:
            return fail(
                "expected loop_detection_regime="
                f"{expected_loop_detection_regime}, got {loop_detection_regime}"
            )

        if loop_detection_regime == "canonical_cluster_graph":
            for key in [
                "loop_count",
                "max_loop_length",
                "min_loop_length",
                "mean_loop_length",
                "loop_edge_coverage_ratio",
            ]:
                if key not in fracture:
                    return fail(f"missing canonical loop field {key}")

            loop_count = int(fracture["loop_count"])
            max_loop_length = int(fracture["max_loop_length"])
            min_loop_length = int(fracture["min_loop_length"])
            mean_loop_length = float(fracture["mean_loop_length"])
            coverage = float(fracture["loop_edge_coverage_ratio"])

            if loop_count < 0:
                return fail("loop_count must be >= 0")
            if coverage < 0.0 or coverage > 1.0:
                return fail("loop_edge_coverage_ratio must be in [0, 1]")
            if loop_count == 0:
                if max_loop_length != 0 or min_loop_length != 0 or mean_loop_length != 0.0:
                    return fail("acyclic canonical run must keep zero-valued loop length metrics")
            else:
                if min_loop_length < 3:
                    return fail("canonical loops must have min_loop_length >= 3")
                if max_loop_length < min_loop_length:
                    return fail("max_loop_length must be >= min_loop_length")
                if mean_loop_length < float(min_loop_length) or mean_loop_length > float(max_loop_length):
                    return fail("mean_loop_length must lie between min and max_loop_length")
            if min_loop_count is not None and loop_count < min_loop_count:
                return fail(f"expected loop_count >= {min_loop_count}, got {loop_count}")
        elif loop_detection_regime == "not_applicable_contaminated":
            for key in [
                "loop_count",
                "max_loop_length",
                "min_loop_length",
                "mean_loop_length",
                "loop_edge_coverage_ratio",
            ]:
                if key in fracture:
                    return fail(f"contaminated non-applicable run should not emit {key}")
        else:
            return fail("unexpected or missing loop_detection_regime")

    return ok("loop mode validated")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate ROMION loop summary mode in a log")
    ap.add_argument("--log", required=True, help="Path to simulation_*.jsonl")
    ap.add_argument(
        "--expected-projection-regime",
        required=True,
        choices=["legacy_visible_only", "canonical_separated", "diagnostic_contaminated"],
    )
    ap.add_argument(
        "--expected-loop-detection-regime",
        default=None,
        choices=["canonical_cluster_graph", "not_applicable_contaminated"],
        help="Optional expected loop detection regime",
    )
    ap.add_argument(
        "--min-loop-count",
        type=int,
        default=None,
        help="Optional minimum loop_count for canonical runs",
    )
    args = ap.parse_args()

    path = Path(args.log)
    if not path.exists():
        print("FAIL: log file not found")
        print(str(path))
        return 2

    try:
        rows = read_jsonl(path)
        valid, msg = validate_loop_mode(
            rows,
            expected_projection_regime=args.expected_projection_regime,
            expected_loop_detection_regime=args.expected_loop_detection_regime,
            min_loop_count=args.min_loop_count,
        )
    except Exception as e:
        print("FAIL: exception while validating loop mode")
        print(str(e))
        return 3

    if valid:
        print("OK:", msg)
        return 0

    print("FAIL:", msg)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
