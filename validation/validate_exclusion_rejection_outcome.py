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


def _find_candidate_marker(rows: List[Dict[str, Any]]) -> Dict[str, Any] | None:
    for row in rows:
        notes = row.get("notes")
        if isinstance(notes, dict) and notes.get("duplicate_creation_path") is True:
            return notes
        meta = row.get("meta")
        if isinstance(meta, dict) and meta.get("duplicate_creation_path") is True:
            return meta
    return None


def _find_rejection_tick(rows: List[Dict[str, Any]]) -> Dict[str, Any] | None:
    for row in rows:
        notes = row.get("notes")
        if isinstance(notes, dict) and notes.get("exclusion_rejection") is True:
            return row
    return None


def classify_rejection_outcome(rows: List[Dict[str, Any]]) -> Tuple[bool, str, Dict[str, Any]]:
    saw_non_legacy = False
    saw_canonical = False

    for row in rows:
        if row.get("type") != "TICK":
            continue
        fracture = row.get("fracture")
        if not isinstance(fracture, dict):
            return False, "TICK fracture payload missing", {}
        regime = fracture.get("projection_regime")
        if regime is None:
            continue
        saw_non_legacy = True
        if regime == "diagnostic_contaminated":
            return True, "not_applicable_contaminated", {
                "duplicate_creation_path": False,
                "duplicate_candidate_identity_complete": False,
                "exclusion_rejection": False,
            }
        if regime == "canonical_separated":
            saw_canonical = True
            continue
        return False, f"unsupported projection_regime: {regime}", {}

    if not saw_non_legacy:
        return True, "legacy_only", {
            "duplicate_creation_path": False,
            "duplicate_candidate_identity_complete": False,
            "exclusion_rejection": False,
        }
    if not saw_canonical:
        return False, "no canonical ticks found", {}

    marker = _find_candidate_marker(rows)
    rejection_tick = _find_rejection_tick(rows)

    if marker is None:
        if rejection_tick is not None:
            return False, "rejection outcome requires duplicate_creation_path", {}
        return True, "rejection_outcome_not_applicable_absent", {
            "duplicate_creation_path": False,
            "duplicate_candidate_identity_complete": False,
            "exclusion_rejection": False,
        }

    complete = marker.get("duplicate_candidate_identity_complete")
    if not isinstance(complete, bool):
        return False, "duplicate_candidate_identity_complete must be a bool", {}

    result = {
        "duplicate_creation_path": True,
        "duplicate_candidate_identity_complete": complete,
        "exclusion_rejection": False,
    }

    if not complete:
        if rejection_tick is not None:
            return False, "partial candidate path must not emit exclusion rejection", {}
        return True, "rejection_outcome_not_applicable_partial", result

    if rejection_tick is None:
        return False, "complete candidate identity requires rejection signal", {}

    notes = rejection_tick.get("notes")
    fracture = rejection_tick.get("fracture")
    if not isinstance(notes, dict) or not isinstance(fracture, dict):
        return False, "rejection tick requires notes and fracture", {}
    if notes.get("rejection_stage") != "stabilization":
        return False, "rejection_stage must be stabilization", {}
    if notes.get("rejection_reason") != "duplicate_niche_identity":
        return False, "rejection_reason must be duplicate_niche_identity", {}
    if notes.get("rejection_identity_complete") is not True:
        return False, "rejection_identity_complete must be true", {}

    signatures = fracture.get("loop_signatures")
    loop_count = fracture.get("loop_count")
    if not isinstance(signatures, list):
        return False, "rejection outcome requires loop_signatures list", {}
    if loop_count is None:
        return False, "rejection outcome requires loop_count", {}
    loop_count = int(loop_count)
    unique_signatures = {str(item) for item in signatures}

    result.update(
        {
            "exclusion_rejection": True,
            "loop_count": loop_count,
            "loop_signatures": [str(item) for item in signatures],
            "unique_loop_signatures": len(unique_signatures),
        }
    )

    if loop_count != len(signatures):
        return False, "loop_count must match loop_signatures length on rejection tick", {}

    if len(unique_signatures) != len(signatures):
        return True, "rejection_with_duplicate_persistence_detected", result

    return True, "rejection_without_duplicate_persistence", result


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate Stage 5 exclusion rejection outcome semantics")
    ap.add_argument("--log", required=True, help="Path to simulation_*.jsonl")
    ap.add_argument(
        "--expected-class",
        default=None,
        choices=[
            "legacy_only",
            "not_applicable_contaminated",
            "rejection_outcome_not_applicable_absent",
            "rejection_outcome_not_applicable_partial",
            "rejection_without_duplicate_persistence",
            "rejection_with_duplicate_persistence_detected",
        ],
    )
    args = ap.parse_args()

    path = Path(args.log)
    if not path.exists():
        print("FAIL: log file not found")
        print(str(path))
        return 2

    try:
        rows = read_jsonl(path)
        valid, classification, result = classify_rejection_outcome(rows)
    except Exception as e:
        print("FAIL: exception while validating exclusion rejection outcome")
        print(str(e))
        return 3

    if not valid:
        print("FAIL:", classification)
        return 1

    if args.expected_class is not None and classification != args.expected_class:
        print(f"FAIL: expected class {args.expected_class}, got {classification}")
        return 1

    print("OK:", classification)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
