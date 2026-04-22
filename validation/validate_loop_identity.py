import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


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


def collect_identity_tick_signatures(
    rows: List[Dict[str, Any]],
) -> Tuple[bool, str, Optional[List[Set[str]]]]:
    ticks = [row for row in rows if row.get("type") == "TICK"]
    if not ticks:
        return fail("no TICK events found"), None

    saw_non_legacy = False
    signatures_per_tick: List[Set[str]] = []

    for tick_event in ticks:
        fracture = tick_event.get("fracture")
        if not isinstance(fracture, dict):
            return fail("TICK fracture payload missing"), None

        projection_regime = fracture.get("projection_regime")
        if projection_regime is None:
            continue

        saw_non_legacy = True
        loop_identity_regime = fracture.get("loop_identity_regime")

        if projection_regime == "diagnostic_contaminated":
            if loop_identity_regime != "not_applicable_contaminated":
                return fail("contaminated run must emit not_applicable_contaminated"), None
            return ok("not_applicable_contaminated"), None

        if projection_regime != "canonical_separated":
            return fail(f"unsupported projection_regime: {projection_regime}"), None

        if loop_identity_regime != "canonical_exact_signature":
            return fail("canonical run must emit canonical_exact_signature"), None

        loop_signatures = fracture.get("loop_signatures")
        if not isinstance(loop_signatures, list):
            return fail("canonical identity run requires loop_signatures list"), None
        signature_set: Set[str] = set()
        for item in loop_signatures:
            if not isinstance(item, str):
                return fail("loop_signatures must contain strings only"), None
            signature_set.add(item)
        if len(signature_set) != len(loop_signatures):
            return fail("loop_signatures must be unique"), None
        signatures_per_tick.append(signature_set)

    if not saw_non_legacy:
        return ok("legacy_only"), None

    return ok("canonical"), signatures_per_tick


def summarize_identity_transitions(signatures_per_tick: List[Set[str]]) -> Dict[str, int]:
    total_persisting = 0
    total_new = 0
    total_dissolved = 0
    max_persisting = 0

    for prev, curr in zip(signatures_per_tick, signatures_per_tick[1:]):
        persisting = len(prev & curr)
        new = len(curr - prev)
        dissolved = len(prev - curr)
        total_persisting += persisting
        total_new += new
        total_dissolved += dissolved
        if persisting > max_persisting:
            max_persisting = persisting

    return {
        "total_persisting": total_persisting,
        "total_new": total_new,
        "total_dissolved": total_dissolved,
        "max_persisting": max_persisting,
    }


def classify_loop_identity(rows: List[Dict[str, Any]]) -> Tuple[bool, str, Dict[str, int]]:
    result, signatures_per_tick = collect_identity_tick_signatures(rows)
    valid, status = result
    if not valid:
        return False, status, {}
    if status in {"legacy_only", "not_applicable_contaminated"}:
        return True, status, {
            "total_persisting": 0,
            "total_new": 0,
            "total_dissolved": 0,
            "max_persisting": 0,
        }

    assert signatures_per_tick is not None
    if not any(signatures_per_tick):
        return True, "no_loops_detected", {
            "total_persisting": 0,
            "total_new": 0,
            "total_dissolved": 0,
            "max_persisting": 0,
        }

    stats = summarize_identity_transitions(signatures_per_tick)
    if stats["max_persisting"] > 0:
        return True, "supports_strict_loop_identity_continuity", stats
    return True, "loop_identity_break_detected", stats


def main() -> int:
    ap = argparse.ArgumentParser(description="Classify strict loop identity continuity in a log")
    ap.add_argument("--log", required=True, help="Path to simulation_*.jsonl")
    ap.add_argument(
        "--expected-class",
        default=None,
        choices=[
            "supports_strict_loop_identity_continuity",
            "loop_identity_break_detected",
            "no_loops_detected",
            "legacy_only",
            "not_applicable_contaminated",
        ],
        help="Optional expected identity class",
    )
    ap.add_argument("--expect-persisting-at-least", type=int, default=None)
    ap.add_argument("--expect-new-at-least", type=int, default=None)
    ap.add_argument("--expect-dissolved-at-least", type=int, default=None)
    args = ap.parse_args()

    path = Path(args.log)
    if not path.exists():
        print("FAIL: log file not found")
        print(str(path))
        return 2

    try:
        rows = read_jsonl(path)
        valid, classification, stats = classify_loop_identity(rows)
    except Exception as e:
        print("FAIL: exception while classifying loop identity")
        print(str(e))
        return 3

    if not valid:
        print("FAIL:", classification)
        return 1

    if args.expected_class is not None and classification != args.expected_class:
        print(f"FAIL: expected class {args.expected_class}, got {classification}")
        return 1
    if args.expect_persisting_at_least is not None and stats["total_persisting"] < args.expect_persisting_at_least:
        print(f"FAIL: expected total_persisting >= {args.expect_persisting_at_least}, got {stats['total_persisting']}")
        return 1
    if args.expect_new_at_least is not None and stats["total_new"] < args.expect_new_at_least:
        print(f"FAIL: expected total_new >= {args.expect_new_at_least}, got {stats['total_new']}")
        return 1
    if args.expect_dissolved_at_least is not None and stats["total_dissolved"] < args.expect_dissolved_at_least:
        print(f"FAIL: expected total_dissolved >= {args.expect_dissolved_at_least}, got {stats['total_dissolved']}")
        return 1

    print("OK:", classification)
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
