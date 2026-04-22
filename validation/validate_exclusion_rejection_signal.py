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


def _find_rejection_signal(rows: List[Dict[str, Any]]) -> Dict[str, Any] | None:
    for row in rows:
        notes = row.get("notes")
        if isinstance(notes, dict) and notes.get("exclusion_rejection") is True:
            return notes
    return None


def classify_rejection_signal(rows: List[Dict[str, Any]]) -> Tuple[bool, str, Dict[str, Any]]:
    saw_non_legacy = False
    saw_canonical = False

    for row in rows:
        if row.get("type") != "TICK":
            continue
        fracture = row.get("fracture")
        if not isinstance(fracture, dict):
            return False, "TICK fracture payload missing", {}
        projection_regime = fracture.get("projection_regime")
        if projection_regime is None:
            continue
        saw_non_legacy = True
        if projection_regime == "diagnostic_contaminated":
            return True, "not_applicable_contaminated", {
                "duplicate_creation_path": False,
                "duplicate_candidate_identity_complete": False,
                "exclusion_rejection": False,
            }
        if projection_regime == "canonical_separated":
            saw_canonical = True
            continue
        return False, f"unsupported projection_regime: {projection_regime}", {}

    if not saw_non_legacy:
        return True, "legacy_only", {
            "duplicate_creation_path": False,
            "duplicate_candidate_identity_complete": False,
            "exclusion_rejection": False,
        }
    if not saw_canonical:
        return False, "no canonical ticks found", {}

    marker = _find_candidate_marker(rows)
    signal = _find_rejection_signal(rows)

    if marker is None:
        if signal is not None:
            return False, "rejection signal requires duplicate_creation_path", {}
        return True, "rejection_signal_absent", {
            "duplicate_creation_path": False,
            "duplicate_candidate_identity_complete": False,
            "exclusion_rejection": False,
        }

    if "duplicate_candidate_identity_complete" not in marker:
        return False, "candidate path marker requires duplicate_candidate_identity_complete", {}
    complete = marker.get("duplicate_candidate_identity_complete")
    if not isinstance(complete, bool):
        return False, "duplicate_candidate_identity_complete must be a bool", {}
    source = marker.get("duplicate_candidate_source")
    if source is None or not isinstance(source, str) or not source.strip():
        return False, "duplicate_candidate_source must be a non-empty string", {}

    result = {
        "duplicate_creation_path": True,
        "duplicate_candidate_identity_complete": complete,
        "duplicate_candidate_source": source,
        "exclusion_rejection": False,
    }

    if not complete:
        if signal is not None:
            return False, "partial candidate path must not emit exclusion rejection", {}
        return True, "rejection_signal_partial_nonrejected", result

    if signal is None:
        return False, "complete candidate identity requires explicit rejection signal", {}
    if signal.get("rejection_stage") != "stabilization":
        return False, "rejection_stage must be stabilization", {}
    if signal.get("rejection_reason") != "duplicate_niche_identity":
        return False, "rejection_reason must be duplicate_niche_identity", {}
    if signal.get("rejection_identity_complete") is not True:
        return False, "rejection_identity_complete must be true", {}

    result.update(
        {
            "exclusion_rejection": True,
            "rejection_stage": "stabilization",
            "rejection_reason": "duplicate_niche_identity",
            "rejection_identity_complete": True,
        }
    )
    return True, "rejection_signal_emitted", result


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate Stage 5 exclusion rejection signaling")
    ap.add_argument("--log", required=True, help="Path to simulation_*.jsonl")
    ap.add_argument(
        "--expected-class",
        default=None,
        choices=[
            "legacy_only",
            "not_applicable_contaminated",
            "rejection_signal_absent",
            "rejection_signal_partial_nonrejected",
            "rejection_signal_emitted",
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
        valid, classification, result = classify_rejection_signal(rows)
    except Exception as e:
        print("FAIL: exception while validating exclusion rejection signal")
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
