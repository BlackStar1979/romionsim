#!/usr/bin/env python3
"""
ROMION Phase Sweep (Test C)

Sweeps spawn/decay parameters and evaluates SOC duration.

For each parameter combination:
- Runs simulation with run_romion_extended.py
- Analyzes with rolling_alpha.py
- Counts consecutive ticks in SOC window (α ∈ [0.7, 1.3])

Optional shock: Second wave of criticality via --shock

Usage:
  python experiments/phase_sweep.py --grid 5 --ticks 1200 --out results_phase
  
With shock:
  python experiments/phase_sweep.py --grid 5 --ticks 1200 --out results_phase --shock

Output:
  results_phase/phase_sweep.csv
"""

import argparse
import csv
import json
import statistics
import subprocess
from pathlib import Path


def run_command(cmd, desc="Running"):
    """Execute command with logging."""
    print(f"{desc}: {' '.join(str(x) for x in cmd)}")
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result


def read_alphas_json(path):
    """Read alphas from JSON output of rolling_alpha.py."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("alphas", [])


def soc_run_length(alphas, lo=0.7, hi=1.3):
    """
    Count longest consecutive run in SOC window.
    
    Returns maximum number of consecutive windows with α ∈ [lo, hi].
    """
    best = 0
    current = 0
    
    for a in alphas:
        # Handle None or invalid values
        if a is None or not isinstance(a, (int, float)):
            current = 0
            continue
        
        if lo <= a <= hi:
            current += 1
            best = max(best, current)
        else:
            current = 0
    
    return best


def main():
    ap = argparse.ArgumentParser(
        description='ROMION Phase Sweep - SOC Duration vs Parameters',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    ap.add_argument('--grid', type=int, default=5,
                    help='Grid resolution for parameter sweep')
    ap.add_argument('--ticks', type=int, default=1000,
                    help='Simulation length')
    ap.add_argument('--out', default='results_phase',
                    help='Output directory')
    ap.add_argument('--nodes', type=int, default=2000,
                    help='Number of nodes')
    ap.add_argument('--init-edges', type=int, default=6000,
                    help='Initial edges')
    ap.add_argument('--log-interval', type=int, default=50,
                    help='Log stats every N ticks')
    ap.add_argument('--dump-graph-every', type=int, default=200,
                    help='Dump graph every N ticks')
    ap.add_argument('--shock', action='store_true',
                    help='Enable second wave of criticality')
    
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # Generate parameter grid
    # Range: 0.8 to 1.6 (factor of 2 span)
    scales = [0.8 + i * (0.8 / (args.grid - 1)) for i in range(args.grid)]
    decays = [0.8 + i * (0.8 / (args.grid - 1)) for i in range(args.grid)]

    rows = []
    total_runs = len(scales) * len(decays)
    run_num = 0

    print(f"Phase sweep: {args.grid}x{args.grid} = {total_runs} runs")
    print(f"Parameter range: spawn [{scales[0]:.2f}, {scales[-1]:.2f}], decay [{decays[0]:.2f}, {decays[-1]:.2f}]")
    if args.shock:
        print("Shock enabled: second wave of criticality")
    print()

    for spawn_scale in scales:
        for decay_scale in decays:
            run_num += 1
            print(f"[{run_num}/{total_runs}] spawn={spawn_scale:.2f}, decay={decay_scale:.2f}")
            
            # Run directory
            run_dir = out / f"s{spawn_scale:.2f}_d{decay_scale:.2f}"
            run_dir.mkdir(parents=True, exist_ok=True)

            # 1. Run simulation
            cmd = [
                "python", "run_romion_extended.py",
                "--ticks", str(args.ticks),
                "--nodes", str(args.nodes),
                "--init-edges", str(args.init_edges),
                "--spawn-scale", f"{spawn_scale:.3f}",
                "--decay-scale", f"{decay_scale:.3f}",
                "--out", str(run_dir),
                "--log-interval", str(args.log_interval),
                "--dump-graph-every", str(args.dump_graph_every)
            ]
            
            # ✅ FIXED: Add shock parameters properly
            if args.shock:
                shock_tick = int(args.ticks * 0.55)  # Start at 55% through
                cmd += [
                    "--shock-tick", str(shock_tick),
                    "--shock-len", "120",
                    "--shock-spawn", "1.6",
                    "--shock-decay", "0.7"
                ]
            
            try:
                run_command(cmd, f"Simulation {run_num}")
            except subprocess.CalledProcessError as e:
                print(f"ERROR: Simulation failed: {e}")
                continue

            # 2. Run rolling alpha analysis
            alpha_json = run_dir / "rolling_alpha.json"
            
            # ✅ FIXED: Proper path to rolling_alpha.py
            # ChatGPT error: split "analysis" and "rolling_alpha.py" into separate args
            cmd2 = [
                "python", "analysis/rolling_alpha.py",
                "--log", str(run_dir / "simulation.jsonl"),
                "--signal", "visible_edges",
                "--diff",
                "--window", "200",
                "--step", "25",
                "--out-json", str(alpha_json)
            ]
            
            try:
                run_command(cmd2, "Rolling alpha")
            except subprocess.CalledProcessError as e:
                print(f"ERROR: Analysis failed: {e}")
                continue

            # 3. Analyze results
            try:
                alphas = read_alphas_json(alpha_json)
            except Exception as e:
                print(f"ERROR: Failed to read alphas: {e}")
                continue
            
            # Compute metrics
            best_soc = soc_run_length(alphas)
            
            # Median alpha (only numeric values)
            numeric_alphas = [a for a in alphas if isinstance(a, (int, float))]
            if numeric_alphas:
                median_alpha = statistics.median(numeric_alphas)
            else:
                median_alpha = float("nan")
            
            # Store results
            rows.append({
                "spawn_scale": spawn_scale,
                "decay_scale": decay_scale,
                "best_soc_run": best_soc,
                "median_alpha": median_alpha,
                "dir": run_dir.name
            })
            
            print(f"  → SOC run: {best_soc}, median α: {median_alpha:.3f}")
            print()

    # Save results
    csv_path = out / "phase_sweep.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        if rows:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    print(f"Results saved: {csv_path}")
    print(f"Total successful runs: {len(rows)}/{total_runs}")


if __name__ == "__main__":
    main()
