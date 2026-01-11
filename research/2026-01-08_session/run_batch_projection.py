#!/usr/bin/env python3
"""
Batch runner for projection ratio tests across all simulations.
Generates comprehensive data for validation.
"""

import subprocess
import json
from pathlib import Path

RESULTS_DIR = Path("C:/Work/romionsim/tests/test_c/results")
OUTPUT_DIR = Path("C:/Work/romionsim/research/2026-01-08_session/batch_results")

SIMULATIONS = ["R0_base", "R1_spawnUp", "R2_decayDown", "R3_tensionUp", "R4_combo", "R5_shock"]
TICKS = [100, 200, 300, 400, 500]

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    all_results = []
    
    for sim in SIMULATIONS:
        log_path = RESULTS_DIR / sim / "simulation.jsonl"
        if not log_path.exists():
            print(f"SKIP: {sim} - no simulation.jsonl")
            continue
            
        for tick in TICKS:
            print(f"Testing {sim} tick {tick}...")
            
            try:
                result = subprocess.run(
                    ["python", "analysis/projection_ratio_test.py",
                     "--log", str(log_path),
                     "--tick", str(tick),
                     "--json"],
                    capture_output=True,
                    text=True,
                    cwd="C:/Work/romionsim",
                    timeout=60
                )
                
                if result.returncode == 0 and result.stdout.strip():
                    data = json.loads(result.stdout)
                    data["simulation"] = sim
                    all_results.append(data)
                    
                    # Extract key metric for summary
                    if "projections" in data:
                        for proj in data["projections"]:
                            if abs(proj["theta"] - 0.5) < 0.01:
                                print(f"  theta=0.5: edge={proj['edge_ratio_percent']:.1f}%, node={proj['node_ratio_percent']:.1f}%")
                else:
                    print(f"  ERROR: {result.stderr[:100] if result.stderr else 'no output'}")
                    
            except Exception as e:
                print(f"  EXCEPTION: {e}")
    
    # Save all results
    output_file = OUTPUT_DIR / "all_projection_ratios.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\nSaved {len(all_results)} results to {output_file}")
    
    # Generate summary table
    print("\n" + "="*80)
    print("SUMMARY: Projection ratio at theta=0.5")
    print("="*80)
    print(f"{'Simulation':<15} {'Tick':<6} {'Edge%':<8} {'Node%':<8} {'Clusters':<10}")
    print("-"*80)
    
    for r in all_results:
        if "projections" in r:
            for proj in r["projections"]:
                if abs(proj["theta"] - 0.5) < 0.01:
                    print(f"{r['simulation']:<15} {r['tick']:<6} {proj['edge_ratio_percent']:<8.2f} {proj['node_ratio_percent']:<8.2f} {proj['n_clusters']:<10}")

if __name__ == "__main__":
    main()
