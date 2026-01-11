#!/usr/bin/env python3
"""
Batch runner for gravity_test.py across all Test C runs.
Generates CSV with corrected metrics.

ROMION O'LOGIC: Uses three semantic thresholds:
- wcluster: objects/matter (clusters)
- wdist: background geometry (distances)  
- wbridge: field/interactions (bridges)
"""

import subprocess
import csv
import re
from pathlib import Path

# Test C runs (updated paths)
RUNS = [
    ("R0", "tests/test_c/results/R0_base", "Baseline"),
    ("R1", "tests/test_c/results/R1_spawnUp", "spawn×1.2"),
    ("R2", "tests/test_c/results/R2_decayDown", "decay×0.7"),
    ("R3", "tests/test_c/results/R3_tensionUp", "tension×1.2"),
    ("R4", "tests/test_c/results/R4_combo", "Combo"),
    ("R5", "tests/test_c/results/R5_shock", "Shock"),
]

TICK = 400

# === THREE SEMANTIC THRESHOLDS (ROMION O'LOGIC) ===
# wcluster: defines OBJECTS (stable local structures)
# wdist:    defines GEOMETRY (background metric)
# wbridge:  defines FIELD (sparse selective channels)
ANALYSIS_PARAMS = {
    "wcluster": 0.02,   # Objects threshold
    "wdist": 0.01,      # Background geometry threshold
    "wbridge": 0.0,     # Field threshold (0.0 = debug mode)
}

BASE_CMD = [
    "python", "analysis/gravity_test.py",
    "--tick", str(TICK),
    "--wcluster", str(ANALYSIS_PARAMS["wcluster"]),
    "--wdist", str(ANALYSIS_PARAMS["wdist"]),
    "--wbridge", str(ANALYSIS_PARAMS["wbridge"]),
    "--cluster-mode", "threshold",
    "--min-cluster-size", "2",
    "--disconnected-policy", "maxdist",
]

def parse_output(text: str) -> dict:
    """Extract key metrics from gravity_test output (new format)."""
    result = {
        "clusters_active": 0,
        "clusters_total": 0,
        "singletons": 0,
        "unassigned_nodes": 0,
        "skipped_edges": 0,
        "pairs_with_bridge": 0,
        "total_bridges": 0,
        "total_weight": 0.0,
        "hub_degree": 0,
        "hub_share": 0.0,
        "coverage": 0.0,
        "max_range": 0,
        "corr_w_d_spearman": 0.0,
        "corr_n_d_spearman": 0.0,
    }
    
    # New format parsing
    
    # Clusters: 451
    m = re.search(r"Clusters:\s+(\d+)", text)
    if m:
        result["clusters_total"] = int(m.group(1))
    
    # Active clusters (with bridges): 301
    m = re.search(r"Active clusters \(with bridges\):\s+(\d+)", text)
    if m:
        result["clusters_active"] = int(m.group(1))
    
    # Singletons: 256 (56.8%)
    m = re.search(r"Singletons:\s+(\d+)", text)
    if m:
        result["singletons"] = int(m.group(1))
    
    # Unassigned nodes: X
    m = re.search(r"Unassigned nodes:\s+(\d+)", text)
    if m:
        result["unassigned_nodes"] = int(m.group(1))
    
    # Skipped edges: X
    m = re.search(r"Skipped edges.*:\s+(\d+)", text)
    if m:
        result["skipped_edges"] = int(m.group(1))
    
    # Pairs with bridges: 1079
    m = re.search(r"Pairs with bridges:\s+(\d+)", text)
    if m:
        result["pairs_with_bridge"] = int(m.group(1))
    
    # Total bridges: 1389
    m = re.search(r"Total bridges:\s+(\d+)", text)
    if m:
        result["total_bridges"] = int(m.group(1))
    
    # Total weight: 14.659
    m = re.search(r"Total weight:\s+([\d.]+)", text)
    if m:
        result["total_weight"] = float(m.group(1))
    
    # Hub degree: 57
    m = re.search(r"Hub degree:\s+(\d+)", text)
    if m:
        result["hub_degree"] = int(m.group(1))
    
    # Hub share: 2.6%
    m = re.search(r"Hub share:\s+([\d.]+)%", text)
    if m:
        result["hub_share"] = float(m.group(1))
    
    # Coverage: 66.7%
    m = re.search(r"Coverage:\s+([\d.]+)%", text)
    if m:
        result["coverage"] = float(m.group(1))
    
    # Max distance with bridges: 8
    m = re.search(r"Max distance with bridges:\s+(\d+)", text)
    if m:
        result["max_range"] = int(m.group(1))
    
    # w~d Spearman: -0.769
    m = re.search(r"w~d Spearman:\s+([-+]?[\d.]+)", text)
    if m:
        result["corr_w_d_spearman"] = float(m.group(1))
    
    # n~d Spearman: -0.328
    m = re.search(r"n~d Spearman:\s+([-+]?[\d.]+)", text)
    if m:
        result["corr_n_d_spearman"] = float(m.group(1))
    
    return result

def main():
    results = []
    
    print("Running gravity_test.py for all Test C runs...")
    print(f"Thresholds: wcluster={ANALYSIS_PARAMS['wcluster']}, "
          f"wdist={ANALYSIS_PARAMS['wdist']}, wbridge={ANALYSIS_PARAMS['wbridge']}")
    print("=" * 70)
    
    # Warn if wbridge=0.0 (debug mode)
    if ANALYSIS_PARAMS["wbridge"] == 0.0:
        print("NOTE: wbridge=0.0 => bridges include all positive edges (debug mode)")
        print()
    
    for run_id, run_dir, param in RUNS:
        log_path = Path(run_dir) / "simulation.jsonl"
        if not log_path.exists():
            print(f"[WARN] {run_id}: {log_path} not found, skipping")
            continue
        
        cmd = BASE_CMD + ["--log", str(log_path)]
        print(f"\n{run_id} ({param}): Running...")
        
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            
            if proc.returncode != 0:
                print(f"  [FAIL] Failed: {proc.stderr[:200]}")
                continue
            
            metrics = parse_output(proc.stdout)
            metrics["run_id"] = run_id
            metrics["parameter"] = param
            # Add thresholds to each row
            metrics["wcluster"] = ANALYSIS_PARAMS["wcluster"]
            metrics["wdist"] = ANALYSIS_PARAMS["wdist"]
            metrics["wbridge"] = ANALYSIS_PARAMS["wbridge"]
            results.append(metrics)
            
            print(f"  [OK] Bridges: {metrics['total_bridges']}, "
                  f"Pairs: {metrics['pairs_with_bridge']}, "
                  f"Hub: {metrics['hub_share']:.1f}%, "
                  f"Range: {metrics['max_range']}")
            
        except subprocess.TimeoutExpired:
            print(f"  [FAIL] Timeout")
        except Exception as e:
            print(f"  [FAIL] Error: {e}")
    
    # Write CSV
    if results:
        csv_path = "tests/test_c/results/test_c_corrected_results.csv"
        fieldnames = [
            "run_id", "parameter",
            "wcluster", "wdist", "wbridge",  # Thresholds first
            "clusters_total", "clusters_active", "singletons",
            "unassigned_nodes", "skipped_edges",
            "pairs_with_bridge", "total_bridges", "total_weight",
            "hub_degree", "hub_share", "coverage",
            "max_range", "corr_w_d_spearman", "corr_n_d_spearman"
        ]
        
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        print("\n" + "=" * 70)
        print(f"[OK] Results written to: {csv_path}")
        print(f"   {len(results)}/{len(RUNS)} runs completed")
        print(f"   Thresholds: wcluster={ANALYSIS_PARAMS['wcluster']}, "
              f"wdist={ANALYSIS_PARAMS['wdist']}, wbridge={ANALYSIS_PARAMS['wbridge']}")
    else:
        print("\n[FAIL] No results collected")

if __name__ == "__main__":
    main()
