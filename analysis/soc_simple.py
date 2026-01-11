#!/usr/bin/env python3
"""
Simple SOC Duration Calculator (no scipy required)

Reads simulation.jsonl and counts consecutive ticks with visible_edges in SOC range.

Usage:
    python analysis/soc_simple.py --log simulation.jsonl --out-json soc_simple.json
"""

import argparse
import json
from pathlib import Path


def compute_soc_duration(values, lo=0.7, hi=1.3, baseline_start=100, baseline_end=200):
    """
    Count longest consecutive run with normalized value in [lo, hi].
    
    Normalization: x_norm = x / mean(baseline)
    """
    if len(values) < baseline_end:
        return 0, float('nan'), float('nan'), float('nan')
    
    # Compute baseline mean
    baseline = values[baseline_start:baseline_end]
    baseline_mean = sum(baseline) / len(baseline) if baseline else 1.0
    
    # Normalize
    normalized = [v / baseline_mean for v in values]
    
    # Find longest SOC run
    max_run = 0
    current_run = 0
    
    for x in normalized:
        if lo <= x <= hi:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 0
    
    # Statistics
    valid = [x for x in normalized if x is not None]
    mean_val = sum(valid) / len(valid) if valid else float('nan')
    
    import math
    if len(valid) > 1:
        variance = sum((x - mean_val) ** 2 for x in valid) / len(valid)
        std_val = math.sqrt(variance)
    else:
        std_val = 0.0
    
    last_val = normalized[-1] if normalized else float('nan')
    
    return max_run, mean_val, std_val, last_val


def main():
    ap = argparse.ArgumentParser(description='Simple SOC Duration Calculator')
    ap.add_argument('--log', required=True, help='Path to simulation.jsonl')
    ap.add_argument('--signal', default='visible_edges', help='Signal to analyze')
    ap.add_argument('--out-json', required=True, help='Output JSON path')
    ap.add_argument('--lo', type=float, default=0.8, help='SOC window lower bound')
    ap.add_argument('--hi', type=float, default=1.2, help='SOC window upper bound')
    
    args = ap.parse_args()
    
    # Load signal
    values = []
    with open(args.log) as f:
        for line in f:
            rec = json.loads(line)
            if rec.get("type") == "TICK":
                val = rec.get(args.signal)
                if val is not None:
                    values.append(float(val))
    
    if not values:
        print(f"ERROR: No {args.signal} values found")
        return 1
    
    # Compute SOC duration
    soc_dur, mean_val, std_val, last_val = compute_soc_duration(values, args.lo, args.hi)
    
    # Save JSON
    result = {
        "soc_duration_ticks": soc_dur,
        "alpha_mean": mean_val,
        "alpha_std": std_val,
        "alpha_last": last_val,
        "signal": args.signal,
        "n_ticks": len(values)
    }
    
    Path(args.out_json).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_json, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"SOC duration: {soc_dur} ticks")
    print(f"Mean (normalized): {mean_val:.3f}")
    print(f"Saved: {args.out_json}")
    
    return 0


if __name__ == "__main__":
    exit(main())
