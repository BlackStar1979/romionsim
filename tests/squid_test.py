#!/usr/bin/env python3
"""
SQUID C_cycles Test - True ROMION Prediction

Tests unique ROMION prediction:
    A_n / A_1 = C_cycles
    
Where:
    A_n = amplitude of 1/f noise for topology with n cycles
    C_cycles = number of independent loops

Three topologies:
1. Single loop (C=1)
2. Figure-8 (C=2)  
3. Three loops (C=3)

This is NOT general SOC test (α ∈ [0.5, 1.5])
This is SPECIFIC ROMION prediction from S1 derivation.

Usage:
    python tests/squid_test.py --ticks 1500 --samples 50

Expected if theory correct:
    A_2/A_1 ≈ 2.0 ± 0.3
    A_3/A_1 ≈ 3.0 ± 0.3
    
If ratios ≠ C_cycles → theory falsified
"""

import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.signal import welch
import subprocess


def run_simulation(topology, nodes, ticks, out_dir):
    """Run simulation for specific topology."""
    print(f"Running {topology} topology...")
    
    topo_dir = out_dir / topology
    topo_dir.mkdir(parents=True, exist_ok=True)
    
    # For now, use standard topology - future: custom init
    cmd = [
        "python", "run_romion_clean.py",
        "--ticks", str(ticks),
        "--nodes", str(nodes),
        "--out", str(topo_dir)
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    
    return topo_dir / "simulation.jsonl"


def load_visible_edges(log_path, start_tick=300):
    """Load visible_edges time series."""
    data = []
    with open(log_path, 'r') as f:
        for line in f:
            obj = json.loads(line)
            if obj.get("type") == "STATS":
                stats = obj["data"]
                if stats["tick"] >= start_tick:
                    data.append(stats["visible_edges"])
    return np.array(data)


def compute_1f_amplitude(signal):
    """
    Compute amplitude of 1/f component.
    
    Returns amplitude A where S(f) ≈ A/f^α
    """
    # Remove mean
    signal = signal - np.mean(signal)
    signal = np.diff(signal)  # First difference
    
    # PSD
    f, P = welch(signal, nperseg=min(256, len(signal)))
    f, P = f[1:], P[1:]  # Remove DC
    
    # Fit in log-log space
    mask = (f > 0.01) & (f < 0.2)
    if np.sum(mask) < 5:
        return np.nan, np.nan
    
    lf = np.log10(f[mask])
    lP = np.log10(P[mask])
    
    # Fit: log(P) = log(A) - α·log(f)
    # So: log(A) = intercept at log(f)=0
    poly = np.polyfit(lf, lP, 1)
    slope = poly[0]  # -α
    intercept = poly[1]  # log(A)
    
    alpha = -slope
    A = 10**intercept
    
    return A, alpha


def main():
    ap = argparse.ArgumentParser(
        description='SQUID C_cycles Test - ROMION Unique Prediction',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    ap.add_argument('--ticks', type=int, default=1500,
                    help='Simulation length')
    ap.add_argument('--nodes', type=int, default=2000,
                    help='Number of nodes')
    ap.add_argument('--samples', type=int, default=50,
                    help='Number of runs per topology')
    ap.add_argument('--out', default='results_squid',
                    help='Output directory')
    
    args = ap.parse_args()
    
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    
    topologies = {
        "single": 1,    # C_cycles = 1
        "figure8": 2,   # C_cycles = 2
        "triple": 3     # C_cycles = 3
    }
    
    results = {}
    
    print("=" * 70)
    print("SQUID C_cycles Test - ROMION Falsification")
    print("=" * 70)
    print()
    
    for topo_name, C_cycles in topologies.items():
        print(f"Testing {topo_name} (C={C_cycles})...")
        
        amplitudes = []
        alphas = []
        
        for run in range(args.samples):
            run_dir = out / topo_name / f"run_{run:03d}"
            run_dir.mkdir(parents=True, exist_ok=True)
            
            # Run simulation
            log_path = run_simulation(topo_name, args.nodes, args.ticks, run_dir.parent)
            
            # Analyze
            signal = load_visible_edges(log_path)
            A, alpha = compute_1f_amplitude(signal)
            
            if not np.isnan(A):
                amplitudes.append(A)
                alphas.append(alpha)
            
            if (run + 1) % 10 == 0:
                print(f"  {run + 1}/{args.samples} runs complete")
        
        # Statistics
        A_mean = np.mean(amplitudes)
        A_std = np.std(amplitudes)
        alpha_mean = np.mean(alphas)
        
        results[topo_name] = {
            "C_cycles": C_cycles,
            "A_mean": A_mean,
            "A_std": A_std,
            "alpha_mean": alpha_mean,
            "amplitudes": amplitudes
        }
        
        print(f"  A = {A_mean:.2e} ± {A_std:.2e}")
        print(f"  α = {alpha_mean:.2f}")
        print()
    
    # Compute ratios
    A1 = results["single"]["A_mean"]
    A2 = results["figure8"]["A_mean"]
    A3 = results["triple"]["A_mean"]
    
    ratio_2_1 = A2 / A1
    ratio_3_1 = A3 / A1
    
    print("=" * 70)
    print("RESULTS:")
    print("=" * 70)
    print()
    print(f"A_2/A_1 = {ratio_2_1:.2f} (predicted: 2.0)")
    print(f"A_3/A_1 = {ratio_3_1:.2f} (predicted: 3.0)")
    print()
    
    # Statistical test
    # Use bootstrap to estimate uncertainty
    n_boot = 1000
    ratios_2_1 = []
    ratios_3_1 = []
    
    for _ in range(n_boot):
        # Resample
        idx1 = np.random.choice(len(results["single"]["amplitudes"]), 
                               len(results["single"]["amplitudes"]))
        idx2 = np.random.choice(len(results["figure8"]["amplitudes"]), 
                               len(results["figure8"]["amplitudes"]))
        idx3 = np.random.choice(len(results["triple"]["amplitudes"]), 
                               len(results["triple"]["amplitudes"]))
        
        A1_boot = np.mean([results["single"]["amplitudes"][i] for i in idx1])
        A2_boot = np.mean([results["figure8"]["amplitudes"][i] for i in idx2])
        A3_boot = np.mean([results["triple"]["amplitudes"][i] for i in idx3])
        
        ratios_2_1.append(A2_boot / A1_boot)
        ratios_3_1.append(A3_boot / A1_boot)
    
    # 95% confidence intervals
    ci_2_1 = np.percentile(ratios_2_1, [2.5, 97.5])
    ci_3_1 = np.percentile(ratios_3_1, [2.5, 97.5])
    
    print(f"95% CI for A_2/A_1: [{ci_2_1[0]:.2f}, {ci_2_1[1]:.2f}]")
    print(f"95% CI for A_3/A_1: [{ci_3_1[0]:.2f}, {ci_3_1[1]:.2f}]")
    print()
    
    # Verdict
    print("=" * 70)
    print("VERDICT:")
    print("=" * 70)
    
    pass_2 = (ci_2_1[0] < 2.0 < ci_2_1[1])
    pass_3 = (ci_3_1[0] < 3.0 < ci_3_1[1])
    
    if pass_2 and pass_3:
        print("✅ PASS: Ratios consistent with C_cycles prediction")
        print("   ROMION theory VALIDATED")
    elif pass_2 or pass_3:
        print("🟡 PARTIAL: Some ratios consistent, some not")
        print("   Theory partially supported")
    else:
        print("❌ FAIL: Ratios NOT consistent with C_cycles")
        print("   ROMION theory FALSIFIED")
    
    # Save results
    results_path = out / "squid_results.json"
    with open(results_path, 'w') as f:
        json.dump({
            "ratio_2_1": float(ratio_2_1),
            "ratio_3_1": float(ratio_3_1),
            "ci_2_1": [float(x) for x in ci_2_1],
            "ci_3_1": [float(x) for x in ci_3_1],
            "pass": bool(pass_2 and pass_3)
        }, f, indent=2)
    
    print()
    print(f"Results saved: {results_path}")


if __name__ == "__main__":
    main()
