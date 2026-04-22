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


def _has_duplicate_creation_path(rows: List[Dict[str, Any]]) -> bool:
    for row in rows:
        notes = row.get("notes")
        if isinstance(notes, dict) and notes.get("duplicate_creation_path") is True:
            return True
        meta = row.get("meta")
        if isinstance(meta, dict) and meta.get("duplicate_creation_path") is True:
            return True
    return False


def classify_exclusion_ingredients(rows: List[Dict[str, Any]]) -> Tuple[bool, str, Dict[str, Any]]:
    ticks = [row for row in rows if row.get("type") == "TICK"]
    if not ticks:
        return False, "no TICK events found", {}

    saw_non_legacy = False
    saw_canonical = False
    saw_richer_identity = False
    candidate_regimes = set()

    for tick_event in ticks:
        fracture = tick_event.get("fracture")
        if not isinstance(fracture, dict):
            return False, "TICK fracture payload missing", {}

        projection_regime = fracture.get("projection_regime")
        if projection_regime is None:
            continue

        saw_non_legacy = True
        exclusion_candidate_regime = fracture.get("exclusion_candidate_regime")

        if projection_regime == "diagnostic_contaminated":
            if exclusion_candidate_regime is not None and exclusion_candidate_regime != "not_applicable_contaminated":
                return False, "contaminated run must emit not_applicable_contaminated", {}
            return True, "not_applicable_contaminated", {
                "saw_richer_identity": False,
                "has_duplicate_creation_path": False,
            }

        if projection_regime != "canonical_separated":
            return False, f"unsupported projection_regime: {projection_regime}", {}

        saw_canonical = True
        if exclusion_candidate_regime is not None:
            if not isinstance(exclusion_candidate_regime, str):
                return False, "canonical exclusion_candidate_regime must be a string", {}
            candidate_regimes.add(exclusion_candidate_regime)

        loop_signatures = fracture.get("loop_signatures")
        if not isinstance(loop_signatures, list):
            return False, "canonical run requires loop_signatures list", {}

        richer = {
            "loop_orientation": fracture.get("loop_orientation"),
            "loop_charge": fracture.get("loop_charge"),
            "loop_excitation_index": fracture.get("loop_excitation_index"),
            "loop_niche_anchor": fracture.get("loop_niche_anchor"),
        }
        richer_present = any(value is not None for value in richer.values())
        if richer_present:
            saw_richer_identity = True
            expected_len = len(loop_signatures)
            for name, value in richer.items():
                if not isinstance(value, list):
                    return False, f"{name} must be a list in canonical richer identity runs", {}
                if len(value) != expected_len:
                    return False, f"{name} length must match loop_signatures", {}
            for value in richer["loop_orientation"]:
                if int(value) not in {-1, 1}:
                    return False, "loop_orientation values must be in {-1, +1}", {}
            for signature, orientation, charge in zip(
                loop_signatures,
                richer["loop_orientation"],
                richer["loop_charge"],
            ):
                loop_len = len(str(signature).split("-"))
                expected_charge = int(int(orientation) * (loop_len % 2))
                if int(charge) != expected_charge:
                    return False, "loop_charge must match orientation * (loop_length mod 2)", {}
            for value in richer["loop_excitation_index"]:
                if int(value) < 0:
                    return False, "loop_excitation_index values must be >= 0", {}
            for value in richer["loop_niche_anchor"]:
                if int(value) < 0:
                    return False, "loop_niche_anchor values must be >= 0", {}

    if not saw_non_legacy:
        return True, "legacy_only", {
            "saw_richer_identity": False,
            "has_duplicate_creation_path": False,
        }

    if not saw_canonical:
        return False, "no canonical ticks found", {}

    has_duplicate_creation_path = _has_duplicate_creation_path(rows)

    if not candidate_regimes:
        return True, "canonical_missing_instrumentation", {
            "saw_richer_identity": saw_richer_identity,
            "has_duplicate_creation_path": has_duplicate_creation_path,
        }

    if len(candidate_regimes) != 1:
        return False, "canonical run must use one exclusion_candidate_regime consistently", {}

    candidate_regime = next(iter(candidate_regimes))

    if not saw_richer_identity:
        return True, "canonical_missing_instrumentation", {
            "saw_richer_identity": False,
            "has_duplicate_creation_path": has_duplicate_creation_path,
        }

    if candidate_regime == "canonical_candidate_path":
        if not has_duplicate_creation_path:
            return False, "canonical_candidate_path requires explicit duplicate_creation_path marker", {}
        return True, "canonical_candidate_path", {
            "saw_richer_identity": True,
            "has_duplicate_creation_path": True,
        }

    if candidate_regime != "canonical_identity_only":
        return False, "unexpected canonical exclusion_candidate_regime", {}
    if has_duplicate_creation_path:
        return False, "canonical_identity_only must not carry duplicate_creation_path marker", {}
    return True, "canonical_identity_only", {
        "saw_richer_identity": True,
        "has_duplicate_creation_path": False,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate exclusion-ingredient instrumentation in a log")
    ap.add_argument("--log", required=True, help="Path to simulation_*.jsonl")
    ap.add_argument(
        "--expected-class",
        default=None,
        choices=[
            "legacy_only",
            "not_applicable_contaminated",
            "canonical_missing_instrumentation",
            "canonical_identity_only",
            "canonical_candidate_path",
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
        valid, classification, result = classify_exclusion_ingredients(rows)
    except Exception as e:
        print("FAIL: exception while validating exclusion ingredients")
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
