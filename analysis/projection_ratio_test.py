#!/usr/bin/env python3
"""
ROMION Projection Ratio Test

Hypothesis (from author):
- CORE has density ~94%
- FRACTURE sees density ~9%  
- Ratio ~9-10% correlates with baryonic matter fraction (~5%)

This test measures:
- How much of CORE structure "projects" to FRACTURE at different thresholds
- Whether there's a natural threshold where ~5-10% is visible

If confirmed, this suggests "dark matter/energy" = CORE structure that doesn't project!
"""

import sys
import json
import argparse
import numpy as np
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from gravity_test import (
    load_graph_snapshot,
    infer_n,
    build_node_adj_threshold,
    find_components,
    assign_clusters,
    build_cluster_graph_from_edges,
    count_bridges
)


def measure_projection_ratio(
    log_path: str,
    tick: int,
    thresholds: List[float] = None
) -> Dict:
    """
    Measure how much structure is "visible" at different projection thresholds.
    
    At threshold θ:
    - Only edges with w > θ are visible
    - Ratio = visible_edges / total_edges
    """
    if thresholds is None:
        # Scan from 0 to 0.5 in steps
        thresholds = [0.0, 0.001, 0.005, 0.01, 0.02, 0.03, 0.05, 0.07, 0.1, 0.15, 0.2, 0.3, 0.5]
    
    # Load data
    snapshot = load_graph_snapshot(log_path, tick)
    if not snapshot:
        return {"error": f"No GRAPH snapshot at tick {tick}"}
    
    edges = snapshot['edges']
    n = infer_n(edges)
    
    # Total edges and weight
    total_edges = len(edges)
    total_weight = sum(e[2] for e in edges)
    
    # Weight distribution
    weights = [e[2] for e in edges]
    
    results = {
        "tick": tick,
        "total_nodes": n,
        "total_edges": total_edges,
        "total_weight": total_weight,
        "weight_stats": {
            "min": min(weights),
            "max": max(weights),
            "mean": np.mean(weights),
            "median": np.median(weights),
            "std": np.std(weights)
        },
        "projections": []
    }
    
    for theta in thresholds:
        # Count edges above threshold
        visible_edges = [e for e in edges if e[2] > theta]
        n_visible = len(visible_edges)
        visible_weight = sum(e[2] for e in visible_edges)
        
        # Compute ratios
        edge_ratio = n_visible / total_edges if total_edges > 0 else 0
        weight_ratio = visible_weight / total_weight if total_weight > 0 else 0
        
        # Build clusters at this threshold
        adj = build_node_adj_threshold(edges, theta)
        comps = find_components(n, adj)
        comps_filtered = [c for c in comps if len(c) >= 2]
        
        # Nodes in clusters
        nodes_in_clusters = sum(len(c) for c in comps_filtered)
        node_ratio = nodes_in_clusters / n if n > 0 else 0
        
        results["projections"].append({
            "theta": theta,
            "visible_edges": n_visible,
            "edge_ratio": edge_ratio,
            "edge_ratio_percent": edge_ratio * 100,
            "weight_ratio": weight_ratio,
            "weight_ratio_percent": weight_ratio * 100,
            "n_clusters": len(comps_filtered),
            "nodes_in_clusters": nodes_in_clusters,
            "node_ratio_percent": node_ratio * 100
        })
    
    # Find threshold where ~5-10% is visible
    target_ratios = [5, 10]
    for target in target_ratios:
        for proj in results["projections"]:
            if proj["edge_ratio_percent"] <= target:
                results[f"theta_for_{target}pct"] = proj["theta"]
                break
    
    return results


def print_report(result: Dict):
    if "error" in result:
        print(f"ERROR: {result['error']}")
        return
    
    print("=" * 80)
    print("ROMION PROJECTION RATIO TEST")
    print("Hypothesis: CORE->FRACTURE projection ratio correlates with baryonic fraction")
    print("=" * 80)
    print()
    print(f"Tick: {result['tick']}")
    print(f"Total nodes: {result['total_nodes']}")
    print(f"Total edges: {result['total_edges']}")
    print(f"Total weight: {result['total_weight']:.4f}")
    print()
    
    ws = result['weight_stats']
    print(f"Weight distribution: min={ws['min']:.4f}, max={ws['max']:.4f}, "
          f"mean={ws['mean']:.4f}, median={ws['median']:.4f}")
    print()
    
    print("PROJECTION AT DIFFERENT THRESHOLDS (theta):")
    print("-" * 80)
    print(f"{'theta':>8} | {'edges':>7} | {'edge%':>7} | {'weight%':>8} | {'clusters':>8} | {'node%':>7}")
    print("-" * 80)
    
    for proj in result["projections"]:
        print(f"{proj['theta']:>8.3f} | {proj['visible_edges']:>7} | "
              f"{proj['edge_ratio_percent']:>6.1f}% | {proj['weight_ratio_percent']:>7.1f}% | "
              f"{proj['n_clusters']:>8} | {proj['node_ratio_percent']:>6.1f}%")
    
    print("-" * 80)
    print()
    
    # Highlight key findings
    print("KEY FINDINGS:")
    if "theta_for_5pct" in result:
        print(f"  Threshold for ~5% visible edges: theta = {result['theta_for_5pct']}")
    if "theta_for_10pct" in result:
        print(f"  Threshold for ~10% visible edges: theta = {result['theta_for_10pct']}")
    
    print()
    print("INTERPRETATION:")
    print("  If baryonic matter (~5%) = 'visible' CORE structure,")
    print("  then 'dark matter/energy' (~95%) = CORE structure below projection threshold!")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="ROMION Projection Ratio Test")
    parser.add_argument("--log", required=True, help="Path to simulation.jsonl")
    parser.add_argument("--tick", type=int, required=True, help="Tick to analyze")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    result = measure_projection_ratio(args.log, args.tick)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
