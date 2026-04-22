import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


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


def collect_tick_observables(
    rows: List[Dict[str, Any]],
) -> Tuple[bool, str, Optional[List[Tuple[bool, int]]]]:
    ticks = [row for row in rows if row.get("type") == "TICK"]
    if not ticks:
        return fail("no TICK events found"), None

    saw_non_legacy = False
    observables: List[Tuple[bool, int]] = []

    for tick_event in ticks:
        fracture = tick_event.get("fracture")
        if not isinstance(fracture, dict):
            return fail("TICK fracture payload missing"), None

        regime = fracture.get("projection_regime")
        if regime is None:
            # Legacy logs should not be reinterpreted into persistence classes.
            continue

        saw_non_legacy = True

        freeze_state = fracture.get("freeze_state")
        visible_edges = fracture.get("visible_edges")

        if not isinstance(freeze_state, bool):
            return fail("freeze_state missing or not bool"), None
        if visible_edges is None:
            return fail("visible_edges missing"), None

        visible_edges_value = int(visible_edges)
        if visible_edges_value < 0:
            return fail("visible_edges must be >= 0"), None

        observables.append((freeze_state, visible_edges_value))

    if not saw_non_legacy:
        return ok("legacy_only"), None

    return ok("non_legacy"), observables


def classify_frozen_persistence(rows: List[Dict[str, Any]]) -> Tuple[bool, str]:
    result, observables = collect_tick_observables(rows)
    valid, status = result
    if not valid:
        return result
    if status == "legacy_only":
        return ok("legacy_only")
    assert observables is not None

    saw_frozen = False
    saw_frozen_with_structure = False
    for freeze_state, visible_edges_value in observables:
        if not freeze_state:
            continue
        saw_frozen = True
        if visible_edges_value > 0:
            saw_frozen_with_structure = True

    if saw_frozen_with_structure:
        return ok("supports_persistence")
    if saw_frozen:
        return ok("frozen_without_persistence_support")
    return ok("not_frozen")


def longest_frozen_persistence_interval(observables: List[Tuple[bool, int]]) -> int:
    longest = 0
    current = 0
    for freeze_state, visible_edges in observables:
        if freeze_state and visible_edges > 0:
            current += 1
            if current > longest:
                longest = current
        else:
            current = 0
    return longest


def classify_evolving_frozen_persistence(
    rows: List[Dict[str, Any]], l_persist: int
) -> Tuple[bool, str]:
    if l_persist <= 0:
        return fail("L_persist must be > 0")

    result, observables = collect_tick_observables(rows)
    valid, status = result
    if not valid:
        return result
    if status == "legacy_only":
        return ok("legacy_only")
    assert observables is not None

    saw_frozen = False
    saw_frozen_with_structure = False
    for freeze_state, visible_edges_value in observables:
        if not freeze_state:
            continue
        saw_frozen = True
        if visible_edges_value > 0:
            saw_frozen_with_structure = True

    if not saw_frozen:
        return ok("not_frozen")
    if not saw_frozen_with_structure:
        return ok("frozen_without_persistence_support")

    longest_interval = longest_frozen_persistence_interval(observables)
    if longest_interval >= l_persist:
        return ok("supports_evolving_persistence")
    return ok("frozen_but_not_persistent_enough")


def main() -> int:
    ap = argparse.ArgumentParser(description="Classify frozen persistence support in a log")
    ap.add_argument("--log", required=True, help="Path to simulation_*.jsonl")
    ap.add_argument(
        "--mode",
        default="snapshot",
        choices=["snapshot", "evolving"],
        help="Classification mode: legacy snapshot support or interval-based evolving support",
    )
    ap.add_argument(
        "--l-persist",
        type=int,
        default=20,
        help="Required contiguous persistence interval length for --mode evolving",
    )
    ap.add_argument(
        "--expected-class",
        default=None,
        choices=[
            "supports_persistence",
            "supports_evolving_persistence",
            "frozen_but_not_persistent_enough",
            "frozen_without_persistence_support",
            "not_frozen",
            "legacy_only",
        ],
        help="Optional expected persistence class",
    )
    args = ap.parse_args()

    path = Path(args.log)
    if not path.exists():
        print("FAIL: log file not found")
        print(str(path))
        return 2

    try:
        rows = read_jsonl(path)
        if args.mode == "snapshot":
            valid, classification = classify_frozen_persistence(rows)
        else:
            valid, classification = classify_evolving_frozen_persistence(rows, args.l_persist)
    except Exception as e:
        print("FAIL: exception while classifying frozen persistence")
        print(str(e))
        return 3

    if not valid:
        print("FAIL:", classification)
        return 1

    if args.expected_class is not None and classification != args.expected_class:
        print(f"FAIL: expected class {args.expected_class}, got {classification}")
        return 1

    print("OK:", classification)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
