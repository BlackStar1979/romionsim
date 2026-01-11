#!/usr/bin/env python3
"""
Simple decay sweep runner - minimal version for testing.
Based on batch_test_c.py pattern.
"""

import subprocess
import csv
import re
from pathlib import Path

# Sweep configuration  
DECAY_VALUES = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5]
SEEDS = [42, 123]
TICK = 400

# Analysis parameters
ANALYSIS_PARAMS = {
    "wcluster": 0.02,
    "wdist": 0.005,
    "wbridge": 0.0,
}


def parse_output(text: str) -> dict:
    """Extract metrics from gravity_test output."""
    result = {
        "total_bridge_count": 0,
        "total_bridge_weight": 0.0,
        "channel_capacity": 0.0,
        "anisotropy": 0.0,
        "clusters_total": 0,
        "hub_share": 0.0,
        "coverage": 0.0,
    }
    
    m = re.search(r"Total bridges:\s+(\d+)", text)
    if m:
        result["total_bridge_count"] = int(m.group(1))
    
    m = re.search(r"Total weight:\s+([\d.]+)", text)
    if m:
        result["total_bridge_weight"] = float(m.group(1))
    
    m = re.search(r"(?:Channel capacity|channel_capacity):\s+([\d.]+)", text)
    if m:
        result["channel_capacity"] = float(m.group(1))
    
    m = re.search(r"\banisotropy:\s+([\d.]+)", text)
    if m:
        result["anisotropy"] = float(m.group(1))
    
    m = re.search(r"Clusters:\s+(\d+)", text)
    if m:
        result["clusters_total"] = int(m.group(1))
    
    m = re.search(r"Hub share:\s+([\d.]+)%", text)
    if m:
        result["hub_share"] = float(m.group(1))
    
    m = re.search(r"Coverage:\s+([\d.]+)%", text)
    if m:
        result["coverage"] = float(m.group(1))
    
    return result


def analyze_run(log_path: str) -> dict:
    """Run gravity_test analysis."""
    cmd = [
        "python", "analysis/gravity_test.py",
        "--log", log_path,
        "--tick", str(TICK),
        "--wcluster", str(ANALYSIS_PARAMS["wcluster"]),
        "--wdist", str(ANALYSIS_PARAMS["wdist"]),
        "--wbridge", str(ANALYSIS_PARAMS["wbridge"]),
        "--min-cluster-size", "2",
        "--disconnected-policy", "maxdist",
        "--channels",
        "--channels-mode", "cut_weight",
        "--anisotropy",
        "--anisotropy-splits", "5",
    ]
    
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        if proc.returncode != 0:
            print(f"    [FAIL] Analysis error: {proc.returncode}")
            return {}
        return parse_output(proc.stdout)
    except Exception as e:
        print(f"    [FAIL] Exception: {e}")
        return {}


def main():
    """Analyze existing Test C results."""
    print("=" * 70)
    print("ANALYZING EXISTING TEST C RESULTS")
    print("=" * 70)
    
    results = []
    
    # Test C results
    runs = [
        ("R0", "tests/test_c/results/R0_base", 1.0, 42),
        ("R2", "tests/test_c/results/R2_decayDown", 0.7, 42),
    ]
    
    for run_id, result_dir, decay, seed in runs:
        log_path = Path(result_dir) / "simulation.jsonl"
        
        if not log_path.exists():
            print(f"\n[SKIP] {run_id}: Log not found")
            continue
        
        print(f"\n[{run_id}] decay={decay}, seed={seed}")
        print(f"  Analyzing {log_path}...")
        
        metrics = analyze_run(str(log_path))
        
        if not metrics:
            print(f"  [FAIL] No metrics")
            continue
        
        result = {
            "run_id": run_id,
            "decay_scale": decay,
            "seed": seed,
            **metrics
        }
        results.append(result)
        
        print(f"  [OK] bridges={metrics.get('total_bridge_count', 0)}, "
              f"w={metrics.get('total_bridge_weight', 0.0):.3f}, "
              f"cap={metrics.get('channel_capacity', 0.0):.3f}, "
              f"aniso={metrics.get('anisotropy', 0.0):.3f}")
    
    # Write results
    if results:
        out_file = "tests/sweep_decay/testc_reanalysis.csv"
        Path(out_file).parent.mkdir(parents=True, exist_ok=True)
        
        fieldnames = [
            "run_id", "decay_scale", "seed",
            "total_bridge_count", "total_bridge_weight",
            "channel_capacity", "anisotropy",
            "clusters_total", "hub_share", "coverage",
        ]
        
        with open(out_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        print("\n" + "=" * 70)
        print(f"[OK] Results written to: {out_file}")
        print(f"   {len(results)} runs analyzed")
    else:
        print("\n[FAIL] No results")


if __name__ == "__main__":
    main()
