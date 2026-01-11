#!/usr/bin/env python3
"""
Auto-analyze when sweep completes.
Runs full analysis pipeline and generates all reports.
"""

import subprocess
import sys
import time
from pathlib import Path

RESULTS_DIR = Path("tests/sweep_decay_inprocess/results")
EXPECTED_RUNS = 18

def check_completion():
    """Check if all 18 runs are complete."""
    run_dirs = list(RESULTS_DIR.glob("d*_s*"))
    
    if len(run_dirs) < EXPECTED_RUNS:
        return False, len(run_dirs)
    
    # Check each has simulation.jsonl
    complete = 0
    for run_dir in run_dirs:
        log = run_dir / "simulation.jsonl"
        if log.exists() and log.stat().st_size > 1000:  # At least 1KB
            complete += 1
    
    return complete == EXPECTED_RUNS, complete

def run_analysis():
    """Run complete analysis pipeline."""
    print("=" * 70)
    print("RUNNING COMPLETE ANALYSIS PIPELINE")
    print("=" * 70)
    print()
    
    scripts = [
        ("analyze_sweep.py", "Gravity analysis with channels/anisotropy"),
        ("quick_viz.py", "Quick visualization"),
        ("final_report.py", "Comprehensive report generation"),
    ]
    
    for script, desc in scripts:
        print(f"\n[STEP] {desc}")
        print(f"Running: python scripts/{script}")
        print("-" * 70)
        
        result = subprocess.run(
            [sys.executable, f"scripts/{script}"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"[OK] {script} completed successfully")
        else:
            print(f"[ERROR] {script} failed:")
            print(result.stderr)
            return False
    
    return True

def main():
    print("Checking sweep completion...")
    
    complete, count = check_completion()
    
    if not complete:
        print(f"Sweep not complete yet: {count}/{EXPECTED_RUNS} runs found")
        print("Run this script again when sweep finishes.")
        return
    
    print(f"[OK] All {EXPECTED_RUNS} runs complete!")
    print()
    
    if run_analysis():
        print()
        print("=" * 70)
        print("ANALYSIS COMPLETE!")
        print("=" * 70)
        print()
        print("Generated files:")
        print("  - tests/sweep_decay_inprocess/results/analysis_results.csv")
        print("  - tests/sweep_decay_inprocess/FINAL_RESULTS.md")
        print()
        print("Next steps:")
        print("  1. Review FINAL_RESULTS.md")
        print("  2. Create canonical RESULTS.md")
        print("  3. Update ROADMAP.md")
        print("  4. Plan next experiments")
        print()
        print("See NEXT_SESSION_TODO.md for detailed checklist")
    else:
        print()
        print("[ERROR] Analysis pipeline failed")
        print("Check error messages above and fix issues")

if __name__ == "__main__":
    main()
