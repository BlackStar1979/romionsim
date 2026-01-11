#!/usr/bin/env python3
"""
Frustration Logger and S2 Tail Analyzer

This tool:
1. Logs Frust(e) during simulation
2. Analyzes tail distribution: P(antipair spawns | high Frust)
3. Verifies if epsilon_spark can be derived from S2

Theory:
    S2 (Antipair): w'(e†) = α₂ · w(e) · exp(-μ · Frust(e))
    
    Hypothesis: epsilon_spark = P(w'(e†) > w_min | Frust >> 1)
                              ≈ ∫[Frust_high] exp(-μ·Frust) dFrust

Usage:
    1. Enable frustration logging in simulation
    2. Run analysis on log file
    3. Compare estimated ε with epsilon_spark = 0.002
"""

import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pathlib import Path


def read_jsonl(path):
    """Read JSONL file."""
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def load_frustration_data(log_path):
    """
    Load frustration data from simulation log.
    
    Expected format:
        {"type":"FRUST","tick":t,"frust":[[u,v,frust_val], ...]}
    """
    all_frust = []
    
    for rec in read_jsonl(log_path):
        if rec.get("type") == "FRUST":
            frust_data = rec.get("frust", [])
            all_frust.extend([f[2] for f in frust_data])  # Extract frust values
    
    if not all_frust:
        raise ValueError("No FRUST data found in log. Enable frustration logging.")
    
    return np.array(all_frust)


def estimate_s2_tail(frust_values, w_min=0.005, alpha2=1.0):
    """
    Estimate probability of spontaneous antipair from S2 tail.
    
    P(w'(e†) > w_min | Frust) = P(α₂·w(e)·exp(-μ·Frust) > w_min)
    
    We estimate μ from distribution fit, then compute tail probability.
    """
    # Fit exponential: P(F) ∝ exp(-μ·F)
    hist, bins = np.histogram(frust_values, bins=50, density=True)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    
    # Fit exp(-μ·x) to histogram
    def exp_model(x, mu, A):
        return A * np.exp(-mu * x)
    
    try:
        # Only fit where we have data
        mask = hist > 0
        popt, _ = curve_fit(exp_model, bin_centers[mask], hist[mask], p0=[1.0, 1.0])
        mu_est, A_est = popt
    except:
        print("Warning: Could not fit exponential, using mu=1.0")
        mu_est = 1.0
        A_est = 1.0
    
    print(f"Estimated μ = {mu_est:.3f}")
    
    # High frustration threshold (top 20%)
    frust_threshold = np.percentile(frust_values, 80)
    
    # For high Frust, compute P(antipair forms)
    # Assuming typical w(e) ~ 0.3, α₂ ~ 1.0
    # w'(e†) = α₂ · w(e) · exp(-μ·Frust) > w_min
    # exp(-μ·Frust) > w_min / (α₂ · w(e))
    # -μ·Frust > log(w_min / (α₂ · w(e)))
    # Frust < -log(w_min / (α₂ · w(e))) / μ
    
    typical_w = 0.3
    threshold_frust = -np.log(w_min / (alpha2 * typical_w)) / mu_est
    
    # Probability that Frust < threshold (allows antipair)
    epsilon_est = np.mean(frust_values < threshold_frust)
    
    return epsilon_est, mu_est, frust_threshold


def plot_frustration_analysis(frust_values, epsilon_est, mu_est, output_path):
    """Plot frustration distribution and S2 tail analysis."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # 1. Histogram
    ax1.hist(frust_values, bins=50, density=True, alpha=0.7, label='Data')
    
    # Fitted exponential
    x = np.linspace(frust_values.min(), frust_values.max(), 100)
    hist, bins = np.histogram(frust_values, bins=50, density=True)
    A_est = hist[0] if len(hist) > 0 else 1.0
    y_fit = A_est * np.exp(-mu_est * x)
    ax1.plot(x, y_fit, 'r--', label=f'exp(-{mu_est:.2f}·F)')
    
    ax1.set_xlabel('Frustration')
    ax1.set_ylabel('Probability Density')
    ax1.set_title('Frustration Distribution')
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    # 2. Cumulative (tail)
    sorted_frust = np.sort(frust_values)
    ccdf = 1.0 - np.arange(len(sorted_frust)) / len(sorted_frust)
    
    ax2.semilogy(sorted_frust, ccdf, label='Empirical CCDF')
    ax2.axhline(epsilon_est, color='r', linestyle='--', 
                label=f'Estimated ε = {epsilon_est:.4f}')
    ax2.set_xlabel('Frustration')
    ax2.set_ylabel('P(F > x)')
    ax2.set_title('Tail Probability (S2 Antipair Regime)')
    ax2.legend()
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"Saved: {output_path}")


def main():
    ap = argparse.ArgumentParser(
        description='Frustration Analysis and S2 Tail Verification',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    ap.add_argument('--log', required=True, help='Path to simulation log with FRUST data')
    ap.add_argument('--out', default='analysis/frustration_analysis.png',
                    help='Output plot path')
    ap.add_argument('--epsilon-spark', type=float, default=0.002,
                    help='Current epsilon_spark value to compare')
    
    args = ap.parse_args()
    
    print("Loading frustration data...")
    frust_values = load_frustration_data(args.log)
    print(f"Loaded {len(frust_values)} frustration values")
    print(f"Range: [{frust_values.min():.3f}, {frust_values.max():.3f}]")
    print(f"Mean: {frust_values.mean():.3f}")
    print()
    
    print("Estimating S2 tail probability...")
    epsilon_est, mu_est, frust_threshold = estimate_s2_tail(frust_values)
    print(f"Estimated ε (from S2): {epsilon_est:.4f}")
    print(f"Current epsilon_spark: {args.epsilon_spark:.4f}")
    print()
    
    # Verdict
    ratio = epsilon_est / args.epsilon_spark if args.epsilon_spark > 0 else float('inf')
    
    print("=" * 60)
    print("VERDICT:")
    print("=" * 60)
    
    if 0.5 < ratio < 2.0:
        print("✅ MATCH: Estimated ε within factor of 2 of epsilon_spark")
        print("   Quantum Spark CAN BE DERIVED from S2 (Antipair tail)")
        print("   Recommendation: KEEP as theory-derived feature")
    elif ratio < 0.5:
        print("⚠️  UNDERESTIMATE: S2 tail gives lower ε than epsilon_spark")
        print(f"   Ratio: {ratio:.2f}x")
        print("   Recommendation: Reduce epsilon_spark or investigate mechanism")
    else:
        print("❌ MISMATCH: S2 tail does not explain epsilon_spark")
        print(f"   Ratio: {ratio:.2f}x")
        print("   Recommendation: REMOVE Quantum Spark as magic feature")
    
    print("=" * 60)
    
    # Plot
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plot_frustration_analysis(frust_values, epsilon_est, mu_est, output_path)
    
    return 0 if 0.5 < ratio < 2.0 else 1


if __name__ == "__main__":
    exit(main())
