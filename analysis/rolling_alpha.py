#!/usr/bin/env python3
"""
Rolling Alpha Analysis with CLI

Tracks spectral exponent α over time to detect phase transitions.

Supports:
- Configurable signal field (visible_edges, tension, pressure, etc.)
- First differencing (--diff)
- JSON output for automation (--out-json)
- PNG output for visualization (--out-png)

Usage:
    # Basic (plot only)
    python analysis/rolling_alpha.py --log simulation.jsonl
    
    # For phase_sweep.py (JSON output)
    python analysis/rolling_alpha.py --log simulation.jsonl --signal visible_edges --diff --out-json alphas.json
    
    # Custom parameters
    python analysis/rolling_alpha.py --log sim.jsonl --start 500 --window 300 --step 30
"""

import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from pathlib import Path


def load_signal(log_path, signal_field, start_tick=0):
    """
    Load time series from simulation log.
    
    Args:
        log_path: Path to simulation.jsonl
        signal_field: Field name to extract (e.g., 'visible_edges', 'mean_pressure')
        start_tick: Ignore data before this tick
        
    Returns:
        numpy array of signal values
    """
    data = []
    
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                
                # Handle both direct stats and nested data
                if obj.get("type") == "STATS":
                    stats = obj.get("data", {})
                else:
                    stats = obj
                
                tick = stats.get("tick", 0)
                if tick < start_tick:
                    continue
                
                value = stats.get(signal_field)
                if value is not None:
                    data.append(float(value))
                    
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
    
    if not data:
        raise ValueError(f"No data found for field '{signal_field}' after tick {start_tick}")
    
    return np.array(data)


def compute_rolling_alpha(signal, window=200, step=20, apply_diff=True):
    """
    Compute spectral exponent α in rolling windows.
    
    Args:
        signal: Time series data
        window: Window size in samples
        step: Step size between windows
        apply_diff: If True, apply first differencing (removes trends)
        
    Returns:
        centers: Window center tick positions
        alphas: Spectral exponents for each window
    """
    alphas = []
    centers = []

    for i in range(0, len(signal) - window, step):
        # Extract window
        w = signal[i:i + window]
        
        # First difference (optional, recommended for trending signals)
        if apply_diff:
            w = np.diff(w)
        
        # Remove mean
        w = w - np.mean(w)
        
        if len(w) < 10:
            continue
        
        # Power spectral density
        nperseg = min(128, len(w))
        f, P = welch(w, nperseg=nperseg)
        
        # Remove DC component
        f, P = f[1:], P[1:]
        
        if len(f) < 5:
            continue
        
        # Fit α in log-log space
        # S(f) ∝ f^(-α) → log(S) = -α·log(f) + const
        mask = (f > 0) & (f < 0.2)  # Focus on low frequencies
        
        if np.sum(mask) < 5:
            alphas.append(None)
            centers.append(i + window // 2)
            continue
        
        lf = np.log10(f[mask])
        lP = np.log10(P[mask])
        
        try:
            slope, _ = np.polyfit(lf, lP, 1)
            alpha = -slope  # S(f) ∝ f^(-α)
        except:
            alpha = None
        
        alphas.append(alpha)
        centers.append(i + window // 2)

    return np.array(centers), np.array(alphas)


def plot_rolling_alpha(centers, alphas, output_path, signal_field):
    """Generate visualization of rolling α."""
    # Filter out None values for plotting
    valid_mask = np.array([a is not None for a in alphas])
    plot_centers = centers[valid_mask]
    plot_alphas = np.array([a for a in alphas if a is not None])
    
    if len(plot_alphas) == 0:
        print("Warning: No valid alpha values to plot")
        return
    
    plt.figure(figsize=(12, 6))
    plt.plot(plot_centers, plot_alphas, marker="o", markersize=3, alpha=0.7)
    
    # SOC region (pink noise: α ∈ [0.7, 1.3])
    plt.axhspan(0.7, 1.3, color="green", alpha=0.15, label="SOC (pink noise)")
    plt.axhline(1.0, linestyle="--", color="black", alpha=0.5, label="α=1.0 (ideal 1/f)")
    
    plt.xlabel("Window Center (tick)")
    plt.ylabel("α (spectral exponent)")
    plt.title(f"Rolling α - {signal_field}")
    plt.legend()
    plt.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"Saved plot: {output_path}")


def save_json(centers, alphas, output_path):
    """Save results as JSON for automation."""
    # Convert to lists, handling None values
    data = {
        "centers": [int(c) if c is not None else None for c in centers],
        "alphas": [float(a) if a is not None and not np.isnan(a) else None for a in alphas]
    }
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved JSON: {output_path}")


def main():
    ap = argparse.ArgumentParser(
        description='Rolling Alpha Analysis - Phase Transition Detection',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Input
    ap.add_argument('--log', required=True,
                    help='Path to simulation.jsonl')
    ap.add_argument('--signal', default='visible_edges',
                    help='Signal field to analyze (visible_edges, mean_pressure, etc.)')
    ap.add_argument('--start', type=int, default=300,
                    help='Start analysis from this tick (skip transient)')
    
    # Analysis parameters
    ap.add_argument('--window', type=int, default=200,
                    help='Rolling window size')
    ap.add_argument('--step', type=int, default=20,
                    help='Step size between windows')
    ap.add_argument('--diff', action='store_true',
                    help='Apply first differencing (recommended for trending signals)')
    
    # Output
    ap.add_argument('--out-json', default=None,
                    help='Save results as JSON (for automation)')
    ap.add_argument('--out-png', default=None,
                    help='Save plot as PNG (default: analysis/rolling_alpha.png)')
    ap.add_argument('--no-plot', action='store_true',
                    help='Skip plotting (useful for automation)')
    
    args = ap.parse_args()
    
    # Load signal
    print(f"Loading signal '{args.signal}' from {args.log}...")
    signal = load_signal(args.log, args.signal, args.start)
    print(f"Loaded {len(signal)} samples (starting from tick {args.start})")
    
    # Compute rolling alpha
    print(f"Computing rolling α (window={args.window}, step={args.step}, diff={args.diff})...")
    centers, alphas = compute_rolling_alpha(signal, args.window, args.step, args.diff)
    
    # Statistics
    valid_alphas = [a for a in alphas if a is not None and not np.isnan(a)]
    if valid_alphas:
        print(f"Computed {len(valid_alphas)} windows")
        print(f"α range: [{min(valid_alphas):.2f}, {max(valid_alphas):.2f}]")
        print(f"α mean: {np.mean(valid_alphas):.2f}")
        
        # SOC statistics
        soc_count = sum(1 for a in valid_alphas if 0.7 <= a <= 1.3)
        soc_pct = 100 * soc_count / len(valid_alphas)
        print(f"SOC windows: {soc_count}/{len(valid_alphas)} ({soc_pct:.1f}%)")
    else:
        print("Warning: No valid alpha values computed")
    
    # Save JSON (for automation)
    if args.out_json:
        save_json(centers, alphas, args.out_json)
    
    # Save/show plot
    if not args.no_plot:
        output_png = args.out_png or "analysis/rolling_alpha.png"
        Path(output_png).parent.mkdir(parents=True, exist_ok=True)
        plot_rolling_alpha(centers, alphas, output_png, args.signal)
        
        # Show plot if not in automation mode
        if not args.out_json:
            plt.show()


if __name__ == "__main__":
    main()
