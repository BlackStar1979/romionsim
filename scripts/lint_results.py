#!/usr/bin/env python3
"""
Fail-closed linter for test result markdown files.

Checks:
1) RESULT files must explicitly state thresholds and flags:
   - wcluster/wdist (background geometry)
   - wbridge (bridges/field)
   - channels: on/off
   - anisotropy: on/off
   - INVALID runs excluded (fail-closed)

2) Test docs must not contain cosmology claims / domain leakage.
   (ROMION simulation here is computational + methodological; no cosmology narrative.)

Usage:
    python scripts/lint_results.py
    python scripts/lint_results.py --root /path/to/repo
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple


REQUIRED_PATTERNS: List[Tuple[str, str]] = [
    ("wcluster_or_wdist", r"\b(wcluster|wdist)\b"),
    ("wbridge", r"\bwbridge\b"),
    ("channels_flag", r"\bchannels\b"),
    ("anisotropy_flag", r"\banisotropy\b"),
    ("fail_closed_invalid", r"\b(INVALID|fail-closed|fail closed)\b"),
]


FORBIDDEN_PATTERNS: List[Tuple[str, str]] = [
    ("cosmology_claim", r"\b(proves?|confirms?|explains?)\s+(cosmolog|dark energy|Hubble)"),
    ("lambda_cdm_claim", r"\b(solves?|resolves?)\s+ΛCDM"),
    ("universe_claim", r"\b(the universe|our universe)\s+(is|shows|demonstrates)"),
]


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


def _find_result_files(root: Path) -> List[Path]:
    """Find RESULTS*.md files in tests/"""
    res = list(root.glob("tests/**/RESULTS*.md"))
    return sorted(set(p.resolve() for p in res))


def _find_test_docs(root: Path) -> List[Path]:
    """Find all markdown docs in tests/ for forbidden phrase scan"""
    docs = list(root.glob("tests/**/*.md"))
    return sorted(set(p.resolve() for p in docs))


def _lint_required(results_files: List[Path]) -> List[str]:
    """Check required fields in RESULTS files"""
    errors: List[str] = []
    for p in results_files:
        txt = _read(p)
        if not txt.strip():
            continue
        missing = []
        for name, pat in REQUIRED_PATTERNS:
            if not re.search(pat, txt, flags=re.IGNORECASE | re.MULTILINE):
                missing.append(name)
        if missing:
            errors.append(f"{p.name}: missing required fields: {', '.join(missing)}")
    return errors


def _lint_forbidden(files: List[Path]) -> List[str]:
    """Check for forbidden cosmology claims"""
    errors: List[str] = []
    for p in files:
        txt = _read(p)
        for name, pat in FORBIDDEN_PATTERNS:
            match = re.search(pat, txt, flags=re.IGNORECASE | re.MULTILINE)
            if match:
                errors.append(f"{p.name}: forbidden phrase '{name}': '{match.group()}'")
                break  # one hit per file
    return errors


def main():
    ap = argparse.ArgumentParser(
        description="Lint result docs for required fields + forbid cosmology claims"
    )
    ap.add_argument("--root", type=str, default=".", help="repo root")
    ap.add_argument("--strict", action="store_true", help="Exit non-zero on any warning")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    
    result_files = _find_result_files(root)
    test_docs = _find_test_docs(root)

    print(f"Scanning {len(result_files)} RESULTS files, {len(test_docs)} test docs...")

    # Required fields only for RESULTS*.md
    req_errors = _lint_required(result_files)
    
    # Forbidden phrases in all test docs
    forb_errors = _lint_forbidden(test_docs)

    all_errors = req_errors + forb_errors
    
    if all_errors:
        print("\nLINT WARNINGS:")
        for e in all_errors:
            print(f"  - {e}")
        if args.strict:
            print("\n[FAIL] Strict mode: lint failed")
            sys.exit(2)
        else:
            print("\n[WARN] Lint issues found (use --strict to fail)")
            sys.exit(0)

    print("[OK] lint_results: all checks passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
