#!/usr/bin/env python3
"""
Quick visualization of partial decay sweep results.
Creates simple text-based chart + identifies patterns.
"""

import csv
from pathlib import Path
from collections import defaultdict

RESULTS_CSV = Path("tests/sweep_decay_inprocess/results/analysis_results.csv")

def load_results():
    """Load and organize results by decay value."""
    if not RESULTS_CSV.exists():
        print(f"Results file not found: {RESULTS_CSV}")
        return None
    
    by_decay = defaultdict(list)
    with open(RESULTS_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            decay = float(row['decay'])
            bridges = int(row['total_bridge_count'])
            weight = float(row['total_bridge_weight'])
            cap = float(row['channel_capacity']) if row['channel_capacity'] else None
            aniso = float(row['anisotropy']) if row['anisotropy'] else None
            
            by_decay[decay].append({
                'seed': int(row['seed']),
                'bridges': bridges,
                'weight': weight,
                'capacity': cap,
                'anisotropy': aniso,
            })
    
    return dict(by_decay)

def print_text_chart(data):
    """Print ASCII bar chart of bridges vs decay."""
    print("\n" + "="*70)
    print("BRIDGES @ TICK 400 vs DECAY")
    print("="*70)
    
    # Sort by decay descending
    decays = sorted(data.keys(), reverse=True)
    
    # Get max bridges for scaling
    max_bridges = max(
        max(r['bridges'] for r in runs)
        for runs in data.values()
    )
    
    scale = 50 / max(max_bridges, 1)  # Scale to 50 chars width
    
    for decay in decays:
        runs = data[decay]
        avg_bridges = sum(r['bridges'] for r in runs) / len(runs)
        
        bar_len = int(avg_bridges * scale)
        bar = '#' * bar_len
        
        # Status indicator
        if avg_bridges == 0:
            status = "FROZEN"
        elif avg_bridges < 100:
            status = "DYING"
        elif avg_bridges < 500:
            status = "LOW"
        elif avg_bridges < 1000:
            status = "MEDIUM"
        else:
            status = "HIGH"
        
        print(f"decay={decay:.2f} [{status:6s}] {bar} {avg_bridges:.0f}")
    
    print("="*70)

def analyze_pattern(data):
    """Identify emerging patterns in data."""
    print("\nPATTERN ANALYSIS:")
    print("-" * 70)
    
    # Sort by decay
    decays = sorted(data.keys(), reverse=True)
    
    frozen = []
    active = []
    
    for decay in decays:
        runs = data[decay]
        avg_bridges = sum(r['bridges'] for r in runs) / len(runs)
        
        if avg_bridges == 0:
            frozen.append(decay)
        elif avg_bridges > 0:
            active.append(decay)
    
    print(f"\nFROZEN systems (0 bridges): {len(frozen)}")
    if frozen:
        print(f"  Decay values: {sorted(frozen, reverse=True)}")
        print(f"  Range: decay in [{min(frozen):.2f}, {max(frozen):.2f}]")
    
    print(f"\nACTIVE systems (>0 bridges): {len(active)}")
    if active:
        print(f"  Decay values: {sorted(active, reverse=True)}")
        print(f"  Range: decay in [{min(active):.2f}, {max(active):.2f}]")
    
    # Identify boundary
    if frozen and active:
        max_frozen = min(frozen)  # LOWEST frozen decay
        min_active = max(active)  # HIGHEST active decay
        print(f"\nFREEZE BOUNDARY:")
        print(f"  Lowest frozen: decay = {max_frozen:.2f}")
        print(f"  Highest active: decay = {min_active:.2f}")
        
        if max_frozen < min_active:
            # Boundary is between these two points
            print(f"  Boundary interval: ({min_active:.2f}, {max_frozen:.2f})")
            width = max_frozen - min_active
            print(f"  Width: delta = {abs(width):.2f}")
        else:
            print("  WARNING: Overlap - need more data points")

def capacity_analysis(data):
    """Analyze channel capacity patterns."""
    print("\n" + "="*70)
    print("CHANNEL CAPACITY ANALYSIS")
    print("="*70)
    
    decays = sorted(data.keys(), reverse=True)
    
    for decay in decays:
        runs = data[decay]
        caps = [r['capacity'] for r in runs if r['capacity'] is not None]
        
        if not caps:
            print(f"η={decay:.2f}: No capacity data")
            continue
        
        avg_cap = sum(caps) / len(caps)
        print(f"decay={decay:.2f}: capacity = {avg_cap:.3f}")
    
    # Find peak
    valid_points = []
    for decay in decays:
        runs = data[decay]
        caps = [r['capacity'] for r in runs if r['capacity'] is not None]
        if caps:
            avg_cap = sum(caps) / len(caps)
            valid_points.append((decay, avg_cap))
    
    if valid_points:
        peak_decay, peak_cap = max(valid_points, key=lambda x: x[1])
        print(f"\nPeak capacity: {peak_cap:.3f} @ decay={peak_decay:.2f}")

def main():
    data = load_results()
    
    if not data:
        print("No results to analyze yet.")
        return
    
    total_points = sum(len(runs) for runs in data.values())
    print("="*70)
    print(f"PARTIAL DECAY SWEEP ANALYSIS")
    print(f"Data points: {total_points}/18 expected")
    print("="*70)
    
    print_text_chart(data)
    analyze_pattern(data)
    capacity_analysis(data)
    
    print("\n" + "="*70)
    print("STATUS: Analysis based on partial data")
    print("Run full analysis after sweep completes: python scripts/analyze_sweep.py")
    print("="*70)

if __name__ == "__main__":
    main()
