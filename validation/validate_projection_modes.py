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


def validate_projection_mode(
    rows: List[Dict[str, Any]],
    expected_regime: str,
    expected_contaminated: bool | None,
) -> Tuple[bool, str]:
    if len(rows) < 3:
        return fail("log too short")

    params_event = rows[1]
    if params_event.get("type") != "PARAMS":
        return fail("second event must be PARAMS")

    ticks = [row for row in rows if row.get("type") == "TICK"]
    if not ticks:
        return fail("no TICK events found")

    for tick_event in ticks:
        fracture = tick_event.get("fracture")
        if not isinstance(fracture, dict):
            return fail("TICK fracture payload missing")

        regime = fracture.get("projection_regime")
        contaminated = fracture.get("projection_contaminated")

        if expected_regime == "legacy_visible_only":
            if regime is not None:
                return fail("legacy run should not emit projection_regime")
            if contaminated is not None:
                return fail("legacy run should not emit projection_contaminated")
            continue

        if regime != expected_regime:
            return fail(f"expected regime {expected_regime}, got {regime}")
        if expected_contaminated is not None and contaminated is not expected_contaminated:
            return fail(
                f"expected projection_contaminated={expected_contaminated}, got {contaminated}"
            )

        for key in [
            "cluster_edges",
            "cluster_ratio",
            "background_edges",
            "background_ratio",
            "bridge_edges",
            "bridge_weight",
            "bridge_ratio",
        ]:
            if key not in fracture:
                return fail(f"missing projection field {key}")

    return ok("projection regime validated")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate ROMION projection regime in a log")
    ap.add_argument("--log", required=True, help="Path to simulation_*.jsonl")
    ap.add_argument(
        "--expected-regime",
        required=True,
        choices=["legacy_visible_only", "canonical_separated", "diagnostic_contaminated"],
    )
    ap.add_argument(
        "--expected-contaminated",
        default=None,
        choices=["true", "false"],
        help="Optional expected projection_contaminated flag",
    )
    args = ap.parse_args()

    path = Path(args.log)
    if not path.exists():
        print("FAIL: log file not found")
        print(str(path))
        return 2

    expected_contaminated = None
    if args.expected_contaminated is not None:
        expected_contaminated = args.expected_contaminated == "true"

    try:
        rows = read_jsonl(path)
        valid, msg = validate_projection_mode(
            rows,
            expected_regime=args.expected_regime,
            expected_contaminated=expected_contaminated,
        )
    except Exception as e:
        print("FAIL: exception while validating projection mode")
        print(str(e))
        return 3

    if valid:
        print("OK:", msg)
        return 0

    print("FAIL:", msg)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
