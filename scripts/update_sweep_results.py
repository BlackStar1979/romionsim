#!/usr/bin/env python3
"""
Update canonical sweep report by embedding generated summary markdown files.

Usage:
  python scripts/update_sweep_results.py --prefix decay_sweep_auto

It will read:
  tests/sweep_decay/results/<prefix>_phaseA.summary.md
  tests/sweep_decay/results/<prefix>_phaseB.summary.md (optional)
  tests/sweep_decay/results/<prefix>.combined.summary.md

And replace the corresponding sections in:
  tests/sweep_decay/RESULTS.md
"""

from __future__ import annotations

import argparse
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read_or_empty(p: Path) -> str:
    if not p.exists():
        return "(summary file not found)"
    return p.read_text(encoding="utf-8").strip()


def _replace_section(doc: str, marker: str, new_content: str) -> str:
    """
    Replace content after a marker line until the next ## heading.
    Keeps the marker line; replaces everything between it and the next section.
    """
    lines = doc.split('\n')
    result = []
    in_section = False
    replaced = False
    
    for line in lines:
        if line.strip().startswith(marker):
            result.append(line)
            result.append("")
            result.append(new_content)
            result.append("")
            in_section = True
            replaced = True
        elif in_section and line.strip().startswith("## "):
            in_section = False
            result.append(line)
        elif not in_section:
            result.append(line)
    
    if not replaced:
        # Marker not found, append at end
        result.append("")
        result.append(f"## {marker.lstrip('#').strip()}")
        result.append("")
        result.append(new_content)
    
    return '\n'.join(result)


def main():
    ap = argparse.ArgumentParser(
        description="Embed sweep summaries into canonical RESULTS.md"
    )
    ap.add_argument(
        "--prefix", 
        required=True, 
        help="Prefix used by batch_sweep (e.g., decay_sweep_auto)"
    )
    ap.add_argument(
        "--results-file",
        default=None,
        help="Path to RESULTS.md (default: tests/sweep_decay/RESULTS.md)"
    )
    args = ap.parse_args()

    root = _repo_root()
    
    if args.results_file:
        results_md = Path(args.results_file)
    else:
        results_md = root / "tests" / "sweep_decay" / "RESULTS.md"
    
    if not results_md.exists():
        print(f"[WARN] Creating new: {results_md}")
        results_md.parent.mkdir(parents=True, exist_ok=True)
        results_md.write_text("# Sweep Decay — RESULTS\n\n## Phase A\n\n## Phase B\n\n## Combined\n", encoding="utf-8")

    src_dir = root / "tests" / "sweep_decay" / "results"
    
    # Try different naming patterns
    phase_a = _read_or_empty(src_dir / f"{args.prefix}_phaseA.summary.md")
    phase_b = _read_or_empty(src_dir / f"{args.prefix}_phaseB.summary.md")
    combined = _read_or_empty(src_dir / f"{args.prefix}.combined.summary.md")
    
    # Fallback patterns
    if "not found" in phase_a:
        phase_a = _read_or_empty(src_dir / f"{args.prefix}.summary.md")
    
    doc = results_md.read_text(encoding="utf-8")
    
    doc = _replace_section(doc, "## Phase A", phase_a)
    doc = _replace_section(doc, "## Phase B", phase_b)
    doc = _replace_section(doc, "## Combined", combined)

    results_md.write_text(doc, encoding="utf-8")
    print(f"[OK] Updated: {results_md}")


if __name__ == "__main__":
    main()
