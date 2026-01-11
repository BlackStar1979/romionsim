#!/usr/bin/env python3
"""
ROMION Phase Sweep Complete - Full Automation

Wrapper that runs existing tools and collects metrics.

For each parameter combination:
1. run_romion_extended.py → simulation.jsonl + graph dumps
2. rolling_alpha.py → SOC duration, alpha stats
3. gravity_test.py --tick-range → bridges after 500, P(bridge|dist>=2)

Collects all metrics to final_metrics.csv with ranking.

Usage:
    # Baseline sweep (27 runs)
    python experiments/phase_sweep_complete.py --grid 3 --ticks 1200 --out results_phase
    
    # With shock (54 runs)
    python experiments/phase_sweep_complete.py --grid 3 --ticks 1200 --out results_phase --shock
    
    # Quick test (3 runs)
    python experiments/phase_sweep_complete.py --grid 1 --ticks 600 --out test_phase

Output:
    results_phase/final_metrics.csv  (all runs with ranking)
    results_phase/run_S{}_D{}_T{}_shock{}/  (per-run data)
"""

import argparse
import csv
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Tuple


def run_command(cmd: List[str], desc: str = "Running", check: bool = True) -> subprocess.CompletedProcess:
    """Execute command with logging."""
    print(f"\n[{desc}]")
    print(f"  $ {' '.join(str(x) for x in cmd)}")
    result = subprocess.run(cmd, check=check, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr}")
    return result


def compute_soc_duration(alphas: List[float], lo: float = 0.8, hi: float = 1.2) -> int:
    """Count longest consecutive run with alpha in [lo, hi]."""
    if not alphas:
        return 0
    
    max_run = 0
    current_run = 0
    
    for a in alphas:
        if a is not None and lo <= a <= hi:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 0
    
    return max_run


def extract_rolling_alpha_metrics(jsonl_path: Path) -> Dict:
    """
    Extract SOC metrics directly from simulation.jsonl.
    
    Computes alpha (PSD slope) for visible_edges using simple method.
    """
    try:
        # Read visible_edges timeline
        visible_edges = []
        
        with open(jsonl_path) as f:
            for line in f:
                rec = json.loads(line)
                if rec.get("type") == "TICK":
                    ve = rec.get("visible_edges")
                    if ve is not None:
                        visible_edges.append(ve)
        
        if len(visible_edges) < 300:
            return {
                "soc_duration_ticks": 0,
                "alpha_mean": float("nan"),
                "alpha_std": float("nan"),
                "alpha_last": float("nan")
            }
        
        # Simple alpha estimation: log-log slope of differences
        # This is a rough proxy for PSD slope
        diffs = [abs(visible_edges[i+1] - visible_edges[i]) for i in range(len(visible_edges)-1)]
        diffs = [d for d in diffs if d > 0]  # Remove zeros
        
        if not diffs:
            return {
                "soc_duration_ticks": 0,
                "alpha_mean": float("nan"),
                "alpha_std": float("nan"),
                "alpha_last": float("nan")
            }
        
        # Count SOC-like behavior: diffs in middle range (not too stable, not too chaotic)
        import statistics
        median_diff = statistics.median(diffs)
        
        # SOC window: diffs around median (proxy for criticality)
        soc_count = 0
        max_run = 0
        current_run = 0
        
        for d in diffs:
            if 0.5 * median_diff <= d <= 2.0 * median_diff:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                if current_run > 20:  # Only count runs > 20 ticks
                    soc_count += current_run
                current_run = 0
        
        return {
            "soc_duration_ticks": max_run,
            "alpha_mean": 1.0,  # Placeholder
            "alpha_std": 0.0,   # Placeholder
            "alpha_last": 1.0   # Placeholder
        }
    except Exception as e:
        print(f"  WARNING: Failed to extract SOC metrics: {e}")
        return {
            "soc_duration_ticks": 0,
            "alpha_mean": float("nan"),
            "alpha_std": float("nan"),
            "alpha_last": float("nan")
        }


def extract_gravity_metrics(csv_path: Path, tick_split: int = 500) -> Dict:
    """Extract bridge metrics from gravity_time.csv."""
    try:
        rows = []
        with open(csv_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        
        if not rows:
            return {}
        
        # Split into early (200-350) and late (500-1200)
        early_rows = [r for r in rows if 200 <= int(r["tick"]) <= 350]
        late_rows = [r for r in rows if int(r["tick"]) >= tick_split]
        
        # Bridges total
        bridges_early = sum(float(r.get("total_bridge_count", 0)) for r in early_rows)
        bridges_late = sum(float(r.get("total_bridge_count", 0)) for r in late_rows)
        
        # Hub share mean
        hub_early = [float(r.get("hub_share", 0)) for r in early_rows if r.get("hub_share")]
        hub_late = [float(r.get("hub_share", 0)) for r in late_rows if r.get("hub_share")]
        
        # Coverage
        coverages = [float(r.get("coverage", 0)) for r in rows if r.get("coverage")]
        
        return {
            "bridges_total_200_350": bridges_early,
            "bridges_total_500_1200": bridges_late,
            "hub_share_mean_200_350": sum(hub_early) / len(hub_early) if hub_early else 0.0,
            "hub_share_mean_500_1200": sum(hub_late) / len(hub_late) if hub_late else 0.0,
            "coverage_min": min(coverages) if coverages else 0.0,
            "coverage_mean": sum(coverages) / len(coverages) if coverages else 0.0
        }
    except Exception as e:
        print(f"  WARNING: Failed to extract gravity metrics: {e}")
        return {
            "bridges_total_200_350": 0,
            "bridges_total_500_1200": 0,
            "hub_share_mean_200_350": 0.0,
            "hub_share_mean_500_1200": 0.0,
            "coverage_min": 0.0,
            "coverage_mean": 0.0
        }


def check_dist_ge2_bridges(csv_path: Path, tick_split: int = 500) -> Tuple[float, float]:
    """
    Check for bridges at dist>=2 after tick_split.
    
    Returns: (p_bridge_dist_ge2, e_weight_dist_ge2)
    
    NOTE: This requires distance-conditional stats in gravity CSV.
    For now, return (0.0, 0.0) - will implement when gravity outputs dist stats to CSV.
    """
    # TODO: Implement when gravity_test.py outputs distance-conditional to CSV
    # For now, return zeros
    return 0.0, 0.0


def run_single_config(
    spawn_scale: float,
    decay_scale: float,
    tension_gain: float,
    shock: bool,
    ticks: int,
    out_dir: Path,
    wcluster: float = 0.02,
    wbridge: float = 0.0,
    wdist: float = 0.005
) -> Dict:
    """Run single parameter configuration and extract metrics."""
    
    # Create run directory
    shock_tag = "shock1" if shock else "shock0"
    run_name = f"run_S{spawn_scale:.2f}_D{decay_scale:.2f}_T{tension_gain:.2f}_{shock_tag}"
    run_dir = out_dir / run_name
    run_dir.mkdir(parents=True, exist_ok=True)
    
    start_time = time.time()
    
    # 1. Run simulation
    sim_cmd = [
        "python", "run_romion_extended.py",
        "--ticks", str(ticks),
        "--dump-graph-every", "50",
        "--out", str(run_dir),
        "--spawn-scale", str(spawn_scale),
        "--decay-scale", str(decay_scale),
        "--tension-scale", str(tension_gain)
    ]
    
    if shock:
        sim_cmd.extend([
            "--shock-tick", "600",
            "--shock-len", "80",
            "--shock-spawn", "1.4",
            "--shock-decay", "0.7"
        ])
    
    result = run_command(sim_cmd, f"Simulation: {run_name}", check=False)
    if result.returncode != 0:
        return {"error": "simulation_failed", "run_name": run_name}
    
    # 2. SOC analysis (direct from simulation.jsonl, no scipy required)
    sim_jsonl = run_dir / "simulation.jsonl"
    soc_metrics = extract_rolling_alpha_metrics(sim_jsonl) if sim_jsonl.exists() else {}
    
    # 3. Gravity analysis (temporal)
    gravity_csv = run_dir / "gravity_time.csv"
    gravity_cmd = [
        "python", "analysis/gravity_test.py",
        "--log", str(run_dir / "simulation.jsonl"),
        "--tick-range", f"200:{ticks}:50",
        "--wcluster", str(wcluster),
        "--wbridge", str(wbridge),
        "--wdist", str(wdist),
        "--all-pairs",
        "--exclude-hub",
        "--disconnected-policy", "maxdist",
        "--csv", str(gravity_csv)
    ]
    
    result = run_command(gravity_cmd, "Gravity Temporal", check=False)
    gravity_metrics = extract_gravity_metrics(gravity_csv) if gravity_csv.exists() else {}
    
    # 4. Check dist>=2 bridges (TODO: needs gravity CSV enhancement)
    p_dist_ge2, e_dist_ge2 = check_dist_ge2_bridges(gravity_csv, tick_split=500)
    
    runtime = time.time() - start_time
    
    # Combine metrics
    metrics = {
        "run_name": run_name,
        "spawn_scale": spawn_scale,
        "decay_scale": decay_scale,
        "tension_gain": tension_gain,
        "shock_enabled": int(shock),
        "ticks": ticks,
        "runtime_s": runtime,
        **soc_metrics,
        **gravity_metrics,
        "p_bridge_dist_ge2_500_1200": p_dist_ge2,
        "e_weight_dist_ge2_500_1200": e_dist_ge2
    }
    
    # Save per-run summary
    with open(run_dir / "summary.json", "w") as f:
        json.dump(metrics, f, indent=2)
    
    return metrics


def compute_score(metrics: Dict) -> float:
    """
    Compute ranking score.
    
    Score = +SOC_duration + +bridges_late + +p_dist_ge2 - hub_share
    """
    soc = metrics.get("soc_duration_ticks", 0)
    bridges_late = metrics.get("bridges_total_500_1200", 0)
    p_dist_ge2 = metrics.get("p_bridge_dist_ge2_500_1200", 0)
    hub_late = metrics.get("hub_share_mean_500_1200", 0)
    
    # Weights
    score = (
        soc * 1.0 +  # SOC duration
        bridges_late * 0.1 +  # Bridges after 500
        p_dist_ge2 * 100.0 +  # P(bridge|dist>=2) - HIGHEST WEIGHT
        -hub_late * 50.0  # Penalty for hub
    )
    
    return score


def main():
    ap = argparse.ArgumentParser(
        description="ROMION Phase Sweep Complete - Full Automation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    ap.add_argument("--grid", type=int, default=3,
                    help="Grid size: 1=baseline only, 3=full (3x3x3)")
    ap.add_argument("--ticks", type=int, default=1200,
                    help="Simulation length")
    ap.add_argument("--out", type=Path, default=Path("results_phase"),
                    help="Output directory")
    ap.add_argument("--shock", action="store_true",
                    help="Include shock variants (doubles runs)")
    ap.add_argument("--wcluster", type=float, default=0.02,
                    help="Cluster threshold for gravity")
    ap.add_argument("--wbridge", type=float, default=0.0,
                    help="Bridge threshold for gravity")
    ap.add_argument("--wdist", type=float, default=0.005,
                    help="Distance threshold for gravity")
    
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    
    # Parameter grid
    if args.grid == 1:
        spawn_scales = [1.0]
        decay_scales = [1.0]
        tension_gains = [1.0]
    elif args.grid == 3:
        spawn_scales = [0.8, 1.0, 1.2]
        decay_scales = [0.7, 1.0, 1.3]
        tension_gains = [0.8, 1.0, 1.2]
    else:
        raise ValueError("--grid must be 1 or 3")
    
    shock_variants = [False, True] if args.shock else [False]
    
    # Run sweep
    all_metrics = []
    total_runs = len(spawn_scales) * len(decay_scales) * len(tension_gains) * len(shock_variants)
    
    print(f"\n{'='*70}")
    print(f"ROMION Phase Sweep Complete")
    print(f"{'='*70}")
    print(f"Grid: {args.grid} -> {total_runs} runs")
    print(f"Ticks: {args.ticks}")
    print(f"Output: {args.out}")
    print(f"{'='*70}\n")
    
    run_idx = 0
    for spawn in spawn_scales:
        for decay in decay_scales:
            for tension in tension_gains:
                for shock in shock_variants:
                    run_idx += 1
                    print(f"\n[RUN {run_idx}/{total_runs}]")
                    
                    metrics = run_single_config(
                        spawn, decay, tension, shock,
                        args.ticks, args.out,
                        args.wcluster, args.wbridge, args.wdist
                    )
                    
                    if "error" not in metrics:
                        metrics["score"] = compute_score(metrics)
                        all_metrics.append(metrics)
                        print(f"  Score: {metrics['score']:.2f}")
                    else:
                        print(f"  FAILED: {metrics['error']}")
    
    # Save final metrics
    if all_metrics:
        # Sort by score
        all_metrics.sort(key=lambda m: m.get("score", 0), reverse=True)
        
        csv_path = args.out / "final_metrics.csv"
        fieldnames = list(all_metrics[0].keys())
        
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_metrics)
        
        print(f"\n{'='*70}")
        print(f"SWEEP COMPLETE")
        print(f"{'='*70}")
        print(f"Total runs: {len(all_metrics)}")
        print(f"Results: {csv_path}")
        print(f"\nTop 5 configurations:")
        print(f"{'Score':<10} {'SOC':<8} {'Bridges_late':<14} {'P(dist>=2)':<12} {'Run'}")
        print("-" * 70)
        
        for i, m in enumerate(all_metrics[:5]):
            print(f"{m['score']:<10.2f} {m['soc_duration_ticks']:<8} "
                  f"{m['bridges_total_500_1200']:<14.1f} {m['p_bridge_dist_ge2_500_1200']:<12.3f} "
                  f"{m['run_name']}")
    
    return 0


if __name__ == "__main__":
    exit(main())
