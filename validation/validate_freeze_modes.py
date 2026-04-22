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


def validate_freeze_mode(
    rows: List[Dict[str, Any]],
    expected_regime: str,
    expected_freeze_state: bool | None,
    expected_freeze_reason: str | None,
) -> Tuple[bool, str]:
    if len(rows) < 3:
        return fail("log too short")

    ticks = [row for row in rows if row.get("type") == "TICK"]
    if not ticks:
        return fail("no TICK events found")

    for tick_event in ticks:
        fracture = tick_event.get("fracture")
        if not isinstance(fracture, dict):
            return fail("TICK fracture payload missing")

        regime = fracture.get("projection_regime")
        freeze_state = fracture.get("freeze_state")
        freeze_reason = fracture.get("freeze_reason")
        bridge_edges = fracture.get("bridge_edges")
        bridge_weight = fracture.get("bridge_weight")

        if expected_regime == "legacy_visible_only":
            if (
                freeze_state is not None
                or freeze_reason is not None
                or bridge_weight is not None
            ):
                return fail("legacy run should not emit freeze or bridge_weight fields")
            continue

        if regime != expected_regime:
            return fail(f"expected regime {expected_regime}, got {regime}")
        if bridge_edges is None:
            return fail("freeze validation requires bridge_edges")
        if bridge_weight is None:
            return fail("freeze validation requires bridge_weight")
        if not isinstance(freeze_state, bool):
            return fail("freeze_state missing or not bool")
        if not isinstance(freeze_reason, str):
            return fail("freeze_reason missing or not string")
        try:
            bridge_weight_value = float(bridge_weight)
        except Exception:
            return fail("bridge_weight missing or not numeric")
        if bridge_weight_value < 0.0:
            return fail("bridge_weight must be >= 0")

        if freeze_state and freeze_reason not in {"no_bridges", "zero_bridge_weight"}:
            return fail("frozen tick has invalid freeze_reason")
        if not freeze_state and freeze_reason not in {"active", "not_applicable"}:
            return fail("active tick has invalid freeze_reason")

        if freeze_reason == "no_bridges":
            if int(bridge_edges) != 0:
                return fail("freeze_reason=no_bridges requires bridge_edges == 0")
        elif freeze_reason == "zero_bridge_weight":
            if int(bridge_edges) <= 0:
                return fail("freeze_reason=zero_bridge_weight requires bridge_edges > 0")
            if bridge_weight_value != 0.0:
                return fail("freeze_reason=zero_bridge_weight requires bridge_weight == 0")
        elif freeze_reason == "active":
            if int(bridge_edges) <= 0:
                return fail("freeze_reason=active requires bridge_edges > 0")
            if bridge_weight_value <= 0.0:
                return fail("freeze_reason=active requires bridge_weight > 0")

        if expected_freeze_state is not None and freeze_state is not expected_freeze_state:
            return fail(
                f"expected freeze_state={expected_freeze_state}, got {freeze_state}"
            )
        if expected_freeze_reason is not None and freeze_reason != expected_freeze_reason:
            return fail(
                f"expected freeze_reason={expected_freeze_reason}, got {freeze_reason}"
            )

    return ok("freeze mode validated")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate ROMION freeze state in a log")
    ap.add_argument("--log", required=True, help="Path to simulation_*.jsonl")
    ap.add_argument(
        "--expected-regime",
        required=True,
        choices=["legacy_visible_only", "canonical_separated", "diagnostic_contaminated"],
    )
    ap.add_argument(
        "--expected-freeze-state",
        default=None,
        choices=["true", "false"],
        help="Optional expected freeze_state",
    )
    ap.add_argument(
        "--expected-freeze-reason",
        default=None,
        choices=["no_bridges", "zero_bridge_weight", "active", "not_applicable"],
        help="Optional expected freeze_reason",
    )
    args = ap.parse_args()

    path = Path(args.log)
    if not path.exists():
        print("FAIL: log file not found")
        print(str(path))
        return 2

    expected_freeze_state = None
    if args.expected_freeze_state is not None:
        expected_freeze_state = args.expected_freeze_state == "true"

    try:
        rows = read_jsonl(path)
        valid, msg = validate_freeze_mode(
            rows,
            expected_regime=args.expected_regime,
            expected_freeze_state=expected_freeze_state,
            expected_freeze_reason=args.expected_freeze_reason,
        )
    except Exception as e:
        print("FAIL: exception while validating freeze mode")
        print(str(e))
        return 3

    if valid:
        print("OK:", msg)
        return 0

    print("FAIL:", msg)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
