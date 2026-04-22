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


def collect_loop_tick_observables(
    rows: List[Dict[str, Any]],
) -> Tuple[bool, str, Optional[List[Tuple[int, int, int]]]]:
    ticks = [row for row in rows if row.get("type") == "TICK"]
    if not ticks:
        return fail("no TICK events found"), None

    saw_non_legacy = False
    observables: List[Tuple[int, int, int]] = []

    for tick_event in ticks:
        fracture = tick_event.get("fracture")
        if not isinstance(fracture, dict):
            return fail("TICK fracture payload missing"), None

        projection_regime = fracture.get("projection_regime")
        if projection_regime is None:
            continue

        saw_non_legacy = True
        loop_detection_regime = fracture.get("loop_detection_regime")

        if projection_regime == "diagnostic_contaminated":
            if loop_detection_regime != "not_applicable_contaminated":
                return fail("contaminated run must emit not_applicable_contaminated"), None
            return ok("not_applicable_contaminated"), None

        if projection_regime != "canonical_separated":
            return fail(f"unsupported projection_regime: {projection_regime}"), None

        if loop_detection_regime != "canonical_cluster_graph":
            return fail("canonical run must emit canonical_cluster_graph"), None

        loop_count = fracture.get("loop_count")
        min_loop_length = fracture.get("min_loop_length")
        max_loop_length = fracture.get("max_loop_length")
        if loop_count is None or min_loop_length is None or max_loop_length is None:
            return fail("canonical run missing loop persistence fields"), None

        loop_count_value = int(loop_count)
        min_loop_length_value = int(min_loop_length)
        max_loop_length_value = int(max_loop_length)
        if loop_count_value < 0:
            return fail("loop_count must be >= 0"), None
        observables.append(
            (loop_count_value, min_loop_length_value, max_loop_length_value)
        )

    if not saw_non_legacy:
        return ok("legacy_only"), None

    return ok("canonical"), observables


def longest_loop_interval(observables: List[Tuple[int, int, int]]) -> int:
    longest = 0
    current = 0
    for loop_count, _, _ in observables:
        if loop_count >= 1:
            current += 1
            if current > longest:
                longest = current
        else:
            current = 0
    return longest


def longest_stable_summary_interval(observables: List[Tuple[int, int, int]]) -> int:
    longest = 0
    current = 0
    current_signature: Optional[Tuple[int, int, int]] = None

    for item in observables:
        loop_count, min_len, max_len = item
        if loop_count < 1:
            current = 0
            current_signature = None
            continue

        signature = (loop_count, min_len, max_len)
        if current_signature == signature:
            current += 1
        else:
            current_signature = signature
            current = 1
        if current > longest:
            longest = current

    return longest


def classify_loop_persistence(
    rows: List[Dict[str, Any]], l_loop: int
) -> Tuple[bool, str]:
    if l_loop <= 0:
        return fail("L_loop must be > 0")

    result, observables = collect_loop_tick_observables(rows)
    valid, status = result
    if not valid:
        return result
    if status in {"legacy_only", "not_applicable_contaminated"}:
        return ok(status)

    assert observables is not None
    saw_loops = any(loop_count >= 1 for loop_count, _, _ in observables)
    if not saw_loops:
        return ok("no_loops_detected")

    longest_interval = longest_loop_interval(observables)
    if longest_interval < l_loop:
        return ok("loop_present_but_not_persistent_enough")

    stable_interval = longest_stable_summary_interval(observables)
    if stable_interval >= l_loop:
        return ok("supports_stable_loop_summary")
    return ok("supports_loop_persistence")


def main() -> int:
    ap = argparse.ArgumentParser(description="Classify loop persistence support in a log")
    ap.add_argument("--log", required=True, help="Path to simulation_*.jsonl")
    ap.add_argument(
        "--l-loop",
        type=int,
        default=3,
        help="Required contiguous loop-bearing interval length",
    )
    ap.add_argument(
        "--expected-class",
        default=None,
        choices=[
            "supports_loop_persistence",
            "supports_stable_loop_summary",
            "loop_present_but_not_persistent_enough",
            "no_loops_detected",
            "legacy_only",
            "not_applicable_contaminated",
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
        valid, classification = classify_loop_persistence(rows, args.l_loop)
    except Exception as e:
        print("FAIL: exception while classifying loop persistence")
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
