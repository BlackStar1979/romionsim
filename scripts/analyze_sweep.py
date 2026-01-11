#!/usr/bin/env python3
"""
Analyze decay sweep results with channels/anisotropy.
Runs gravity_test on all completed simulations.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import subprocess
import csv
import re
from typing import Dict, List

RESULTS_DIR = Path("tests/sweep_decay_inprocess/results")
ANALYSIS_PARAMS = {
    "wcluster": 0.02,
    "wdist": 0.005,
    "wbridge": 0.0,
    "wdist_mode": "threshold",
    "min_cluster_size": 2,
    "disconnected_policy": "maxdist",
}
MAIN_TICK = 400


def parse_gravity_output(text: str) -> Dict:
    """Extract metrics from gravity_test output."""
    result = {
        "clusters_total": 0,
        "clusters_active": 0,
        "singletons": 0,
        "total_bridge_count": 0,
        "total_bridge_weight": 0.0,
        "hub_share": 0.0,
        "coverage": 0.0,
        "range": 0,
        "channel_capacity": None,
        "anisotropy": None,
    }
    
    # Parse all metrics
    m = re.search(r"Clusters:\s+(\d+)", text)
    if m:
        result["clusters_total"] = int(m.group(1))
    
    m = re.search(r"Active clusters \(with bridges\):\s+(\d+)", text)
    if m:
        result["clusters_active"] = int(m.group(1))
    
    m = re.search(r"Singletons:\s+(\d+)", text)
    if m:
        result["singletons"] = int(m.group(1))
    
    m = re.search(r"Total bridges:\s+(\d+)", text)
    if m:
        result["total_bridge_count"] = int(m.group(1))
    
    m = re.search(r"Total weight:\s+([\d.]+)", text)
    if m:
        result["total_bridge_weight"] = float(m.group(1))
    
    m = re.search(r"Hub share:\s+([\d.]+)%", text)
    if m:
        result["hub_share"] = float(m.group(1))
    
    m = re.search(r"Coverage:\s+([\d.]+)%", text)
    if m:
        result["coverage"] = float(m.group(1))
    
    m = re.search(r"Max distance with bridges:\s+(\d+)", text)
    if m:
        result["range"] = int(m.group(1))
    
    m = re.search(r"channel_capacity:\s+([\d.]+)", text)
    if m:
        result["channel_capacity"] = float(m.group(1))
    
    m = re.search(r"anisotropy:\s+([\d.]+)", text)
    if m:
        result["anisotropy"] = float(m.group(1))
    
    return result


def analyze_run(log_path: Path, tick: int) -> Dict:
    """Run gravity_test with channels/anisotropy."""
    cmd = [
        "python", "analysis/gravity_test.py",
        "--log", str(log_path),
        "--tick", str(tick),
        "--wcluster", str(ANALYSIS_PARAMS["wcluster"]),
        "--wbridge", str(ANALYSIS_PARAMS["wbridge"]),
        "--wdist", str(ANALYSIS_PARAMS["wdist"]),
        "--min-cluster-size", str(ANALYSIS_PARAMS["min_cluster_size"]),
        "--disconnected-policy", ANALYSIS_PARAMS["disconnected_policy"],
        "--channels",
        "--channels-mode", "cut_weight",
        "--anisotropy",
        "--anisotropy-splits", "5",
    ]
    
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=90, check=False)
        if proc.returncode != 0:
            print(f"  [FAIL] {log_path.parent.name}")
            return {}
        return parse_gravity_output(proc.stdout)
    except Exception as e:
        print(f"  [ERROR] {log_path.parent.name}: {e}")
        return {}


def main():
    if not RESULTS_DIR.exists():
        print(f"Results directory not found: {RESULTS_DIR}")
        return
    
    results = []
    run_dirs = sorted(RESULTS_DIR.glob("d*_s*"))
    
    print("=" * 70)
    print(f"ANALYZING {len(run_dirs)} sweep results @ tick {MAIN_TICK}")
    print("=" * 70)
    
    for i, run_dir in enumerate(run_dirs, 1):
        log_path = run_dir / "simulation.jsonl"
        if not log_path.exists():
            print(f"[{i}/{len(run_dirs)}] SKIP {run_dir.name} - no log")
            continue
        
        # Parse decay and seed from directory name
        # Format: d1.0_s42
        name = run_dir.name
        parts = name.split("_")
        decay = float(parts[0][1:])  # "d1.0" -> 1.0
        seed = int(parts[1][1:])     # "s42" -> 42
        
        print(f"[{i}/{len(run_dirs)}] {name} ", end="")
        
        metrics = analyze_run(log_path, MAIN_TICK)
        if not metrics:
            continue
        
        result = {
            "decay": decay,
            "seed": seed,
            "tick": MAIN_TICK,
            **metrics
        }
        results.append(result)
        
        cap = metrics.get("channel_capacity")
        an = metrics.get("anisotropy")
        cap_s = f"{cap:.3f}" if cap else "-"
        an_s = f"{an:.3f}" if an else "-"
        
        print(f"bridges={metrics['total_bridge_count']} ({metrics['total_bridge_weight']:.2f}), "
              f"cap={cap_s}, aniso={an_s}")
    
    # Write CSV
    if results:
        csv_path = RESULTS_DIR / "analysis_results.csv"
        fieldnames = [
            "decay", "seed", "tick",
            "clusters_total", "clusters_active", "singletons",
            "total_bridge_count", "total_bridge_weight",
            "hub_share", "coverage", "range",
            "channel_capacity", "anisotropy",
        ]
        
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        print("\n" + "=" * 70)
        print(f"[OK] Results written to: {csv_path}")
        print(f"   {len(results)} runs analyzed")
        
        # Quick summary by decay
        print("\nSUMMARY BY DECAY:")
        by_decay = {}
        for r in results:
            by_decay.setdefault(r['decay'], []).append(r)
        
        for decay in sorted(by_decay.keys(), reverse=True):
            runs = by_decay[decay]
            avg_bridges = sum(r['total_bridge_count'] for r in runs) / len(runs)
            caps = [r['channel_capacity'] for r in runs if r['channel_capacity']]
            avg_cap = sum(caps) / len(caps) if caps else 0.0
            print(f"  decay={decay:.2f}: bridges={avg_bridges:.1f}, capacity={avg_cap:.3f} (n={len(runs)})")
    else:
        print("\n[FAIL] No results to write")


if __name__ == "__main__":
    main()
