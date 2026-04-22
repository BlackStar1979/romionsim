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


def _has_duplicate_creation_path(rows: List[Dict[str, Any]]) -> bool:
    for row in rows:
        notes = row.get("notes")
        if isinstance(notes, dict) and notes.get("duplicate_creation_path") is True:
            return True
    return False


def _summary_signature(fracture: Dict[str, Any]) -> Tuple[int, int, int, float]:
    return (
        int(fracture.get("loop_count", 0)),
        int(fracture.get("min_loop_length", 0)),
        int(fracture.get("max_loop_length", 0)),
        float(fracture.get("mean_loop_length", 0.0)),
    )


def audit_exclusion_readiness(rows: List[Dict[str, Any]]) -> Tuple[bool, str, Dict[str, Any]]:
    ticks = [row for row in rows if row.get("type") == "TICK"]
    if not ticks:
        return False, "no TICK events found", {}

    saw_non_legacy = False
    saw_operational_identity = False
    saw_summary_structural_non_equivalence = False
    missing_orientation = True
    missing_charge = True
    missing_excitation_index = True
    missing_niche_anchor = True

    previous_by_summary: Dict[Tuple[int, int, int, float], Set[str]] = {}

    for tick_event in ticks:
        fracture = tick_event.get("fracture")
        if not isinstance(fracture, dict):
            return False, "TICK fracture payload missing", {}

        projection_regime = fracture.get("projection_regime")
        if projection_regime is None:
            continue

        saw_non_legacy = True
        if projection_regime == "diagnostic_contaminated":
            return True, "not_ready_contaminated", {
                "missing_orientation": True,
                "missing_charge": True,
                "missing_excitation_index": True,
                "missing_niche_anchor": True,
                "has_duplicate_creation_path": False,
                "saw_operational_identity": False,
                "saw_summary_structural_non_equivalence": False,
            }

        if projection_regime != "canonical_separated":
            return False, f"unsupported projection_regime: {projection_regime}", {}

        if fracture.get("loop_identity_regime") == "canonical_exact_signature":
            saw_operational_identity = True

        if "loop_orientation" in fracture:
            missing_orientation = False
        if "loop_charge" in fracture:
            missing_charge = False
        if "loop_excitation_index" in fracture:
            missing_excitation_index = False
        if "loop_niche_anchor" in fracture:
            missing_niche_anchor = False

        loop_signatures = fracture.get("loop_signatures")
        if not isinstance(loop_signatures, list):
            continue
        signature_set = {str(item) for item in loop_signatures}
        summary = _summary_signature(fracture)
        prior = previous_by_summary.get(summary)
        if prior is not None and prior != signature_set:
            saw_summary_structural_non_equivalence = True
        previous_by_summary[summary] = signature_set

    if not saw_non_legacy:
        return True, "not_ready_legacy_only", {
            "missing_orientation": True,
            "missing_charge": True,
            "missing_excitation_index": True,
            "missing_niche_anchor": True,
            "has_duplicate_creation_path": False,
            "saw_operational_identity": False,
            "saw_summary_structural_non_equivalence": False,
        }

    has_duplicate_creation_path = _has_duplicate_creation_path(rows)

    result = {
        "missing_orientation": missing_orientation,
        "missing_charge": missing_charge,
        "missing_excitation_index": missing_excitation_index,
        "missing_niche_anchor": missing_niche_anchor,
        "has_duplicate_creation_path": has_duplicate_creation_path,
        "saw_operational_identity": saw_operational_identity,
        "saw_summary_structural_non_equivalence": saw_summary_structural_non_equivalence,
    }

    if not saw_operational_identity:
        return True, "not_ready_missing_operational_identity", result

    if not has_duplicate_creation_path:
        if saw_summary_structural_non_equivalence:
            return True, "partially_ready_operational_identity_only", result
        return True, "not_ready_missing_duplicate_creation_path", result

    if missing_orientation:
        return True, "not_ready_missing_orientation", result
    if missing_charge:
        return True, "not_ready_missing_charge", result
    if missing_excitation_index:
        return True, "not_ready_missing_excitation_index", result
    if missing_niche_anchor:
        return True, "not_ready_missing_niche_anchor", result
    return True, "candidate_ready_for_exclusion_test", result


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit ROMION exclusion readiness")
    ap.add_argument("--log", required=True, help="Path to simulation_*.jsonl")
    ap.add_argument(
        "--expected-class",
        default=None,
        choices=[
            "not_ready_legacy_only",
            "not_ready_contaminated",
            "not_ready_missing_operational_identity",
            "not_ready_missing_duplicate_creation_path",
            "not_ready_missing_orientation",
            "not_ready_missing_charge",
            "not_ready_missing_excitation_index",
            "not_ready_missing_niche_anchor",
            "partially_ready_operational_identity_only",
            "candidate_ready_for_exclusion_test",
        ],
    )
    ap.add_argument("--expect-non-equivalence", choices=["true", "false"], default=None)
    args = ap.parse_args()

    path = Path(args.log)
    if not path.exists():
        print("FAIL: log file not found")
        print(str(path))
        return 2

    try:
        rows = read_jsonl(path)
        valid, classification, result = audit_exclusion_readiness(rows)
    except Exception as e:
        print("FAIL: exception while auditing exclusion readiness")
        print(str(e))
        return 3

    if not valid:
        print("FAIL:", classification)
        return 1

    if args.expected_class is not None and classification != args.expected_class:
        print(f"FAIL: expected class {args.expected_class}, got {classification}")
        return 1

    if args.expect_non_equivalence is not None:
        expected = args.expect_non_equivalence == "true"
        if bool(result.get("saw_summary_structural_non_equivalence")) is not expected:
            print(
                "FAIL: expected saw_summary_structural_non_equivalence="
                f"{expected}, got {result.get('saw_summary_structural_non_equivalence')}"
            )
            return 1

    print("OK:", classification)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
