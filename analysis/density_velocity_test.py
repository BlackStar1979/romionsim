#!/usr/bin/env python3
"""
ROMION Density-Velocity Test

Hypothesis: In denser regions of the hypergraph, "propagation" is slower.

This script measures:
1. Local density of each cluster (sum of internal edge weights / node count)
2. Bridge "reach" for each cluster (average distance to bridged clusters)
3. Correlation between density and reach

Prediction: Negative correlation (denser clusters have shorter reach)
"""

import sys
import json
import argparse
import numpy as np
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from gravity_test import (
    load_graph_snapshot,
    infer_n, 
    build_node_adj_threshold, 
    find_components, 
    assign_clusters,
    build_cluster_graph_from_edges,
    count_bridges,
    all_pairs_cluster_distances
)


def compute_cluster_density(
    edges: List,
    node2c: List[int],
    n_clusters: int
) -> Dict[int, float]:
    """
    Compute internal density for each cluster.
    
    Density = sum of weights of internal edges / number of nodes in cluster
    """
    # Count nodes per cluster
    nodes_per_cluster = defaultdict(int)
    for c in node2c:
        if c >= 0:
            nodes_per_cluster[c] += 1
    
    # Sum internal edge weights per cluster
    internal_weight = defaultdict(float)
    for e in edges:
        u, v, w = e[0], e[1], e[2]  # edges are [u, v, w] lists
        cu = node2c[u] if u < len(node2c) else -1
        cv = node2c[v] if v < len(node2c) else -1
        
        if cu >= 0 and cu == cv:  # Internal edge
            internal_weight[cu] += w
    
    # Compute density
    density = {}
    for c in range(n_clusters):
        n_nodes = nodes_per_cluster.get(c, 0)
        if n_nodes > 0:
            density[c] = internal_weight.get(c, 0.0) / n_nodes
        else:
            density[c] = 0.0
    
    return density


def compute_cluster_reach(
    meta_bg: Dict[Tuple[int, int], float],
    bridges: Dict[Tuple[int, int], Dict],
    n_clusters: int
) -> Dict[int, float]:
    """
    Compute average "reach" for each cluster.
    
    Reach = average distance (in meta_bg) to clusters connected by bridges
    """
    # Get all-pairs distances (already imported at top level)
    dists = all_pairs_cluster_distances(meta_bg, n_clusters)
    
    # For each cluster, compute average distance to bridged neighbors
    reach = {}
    for c in range(n_clusters):
        distances_to_bridged = []
        for (c1, c2), bridge_info in bridges.items():
            if c1 == c or c2 == c:
                other = c2 if c1 == c else c1
                pair = (min(c, other), max(c, other))
                if pair in dists:
                    distances_to_bridged.append(dists[pair])
        
        if distances_to_bridged:
            reach[c] = np.mean(distances_to_bridged)
        else:
            reach[c] = 0.0  # No bridges
    
    return reach


def compute_cluster_bridge_count(
    bridges: Dict[Tuple[int, int], 'BridgeAgg'],
    n_clusters: int
) -> Dict[int, int]:
    """Count number of bridge connections per cluster."""
    count = defaultdict(int)
    for (c1, c2), bridge_agg in bridges.items():
        count[c1] += bridge_agg.count
        count[c2] += bridge_agg.count
    return dict(count)


def analyze_density_velocity(
    log_path: str,
    tick: int,
    wcluster: float = 0.02,
    wdist: float = 0.01,
    wbridge: float = 0.0,
    min_cluster_size: int = 2
) -> Dict:
    """
    Main analysis: measure density and reach for all clusters.
    """
    # Bridges are already imported at top level
    
    # Load data
    snapshot = load_graph_snapshot(log_path, tick)
    if not snapshot:
        return {"error": f"No GRAPH snapshot at tick {tick}"}
    
    edges = snapshot['edges']
    n = infer_n(edges)
    
    # Build clusters (using wcluster)
    adj = build_node_adj_threshold(edges, wcluster)
    comps = find_components(n, adj)
    
    # Filter small clusters
    if min_cluster_size > 1:
        comps = [c for c in comps if len(c) >= min_cluster_size]
    
    node2c = assign_clusters(comps, n)
    n_clusters = len(comps)
    
    if n_clusters == 0:
        return {"error": "No clusters found"}
    
    # Build background meta-graph (using wdist)
    meta_bg = build_cluster_graph_from_edges(edges, node2c, wdist)
    
    # Count bridges (using wbridge)
    bridges, _ = count_bridges(edges, node2c, wbridge)
    
    # Compute metrics
    density = compute_cluster_density(edges, node2c, n_clusters)
    reach = compute_cluster_reach(meta_bg, bridges, n_clusters)
    bridge_count = compute_cluster_bridge_count(bridges, n_clusters)
    
    # Collect data for clusters with bridges
    data_points = []
    for c in range(n_clusters):
        if bridge_count.get(c, 0) > 0:  # Only clusters with bridges
            data_points.append({
                'cluster': c,
                'density': density.get(c, 0.0),
                'reach': reach.get(c, 0.0),
                'bridge_count': bridge_count.get(c, 0),
                'size': len(comps[c])
            })
    
    if len(data_points) < 3:
        return {
            "error": "Not enough clusters with bridges for correlation",
            "n_clusters": n_clusters,
            "clusters_with_bridges": len(data_points)
        }
    
    # Compute correlations
    densities = [d['density'] for d in data_points]
    reaches = [d['reach'] for d in data_points]
    counts = [d['bridge_count'] for d in data_points]
    
    from scipy.stats import spearmanr, pearsonr
    
    # Density vs Reach correlation
    if np.std(densities) > 0 and np.std(reaches) > 0:
        density_reach_pearson, _ = pearsonr(densities, reaches)
        density_reach_spearman, _ = spearmanr(densities, reaches)
    else:
        density_reach_pearson = 0.0
        density_reach_spearman = 0.0
    
    # Density vs Bridge Count correlation
    if np.std(densities) > 0 and np.std(counts) > 0:
        density_count_pearson, _ = pearsonr(densities, counts)
        density_count_spearman, _ = spearmanr(densities, counts)
    else:
        density_count_pearson = 0.0
        density_count_spearman = 0.0
    
    return {
        "tick": tick,
        "n_clusters": n_clusters,
        "clusters_with_bridges": len(data_points),
        "density_stats": {
            "min": min(densities),
            "max": max(densities),
            "mean": np.mean(densities),
            "std": np.std(densities)
        },
        "reach_stats": {
            "min": min(reaches),
            "max": max(reaches),
            "mean": np.mean(reaches),
            "std": np.std(reaches)
        },
        "correlations": {
            "density_vs_reach_pearson": density_reach_pearson,
            "density_vs_reach_spearman": density_reach_spearman,
            "density_vs_bridge_count_pearson": density_count_pearson,
            "density_vs_bridge_count_spearman": density_count_spearman
        },
        "prediction": "ROMION predicts density_vs_reach should be NEGATIVE",
        "data_points": data_points
    }


def print_report(result: Dict):
    """Print formatted report."""
    if "error" in result:
        print(f"ERROR: {result['error']}")
        return
    
    print("=" * 70)
    print("ROMION DENSITY-VELOCITY TEST")
    print("=" * 70)
    print()
    print(f"Tick: {result['tick']}")
    print(f"Total clusters: {result['n_clusters']}")
    print(f"Clusters with bridges: {result['clusters_with_bridges']}")
    print()
    
    print("DENSITY STATISTICS (internal edge weight / node count):")
    ds = result['density_stats']
    print(f"  Min: {ds['min']:.4f}")
    print(f"  Max: {ds['max']:.4f}")
    print(f"  Mean: {ds['mean']:.4f}")
    print(f"  Std: {ds['std']:.4f}")
    print()
    
    print("REACH STATISTICS (avg distance to bridged clusters):")
    rs = result['reach_stats']
    print(f"  Min: {rs['min']:.2f}")
    print(f"  Max: {rs['max']:.2f}")
    print(f"  Mean: {rs['mean']:.2f}")
    print(f"  Std: {rs['std']:.2f}")
    print()
    
    print("CORRELATIONS:")
    corr = result['correlations']
    print(f"  Density vs Reach (Pearson):  {corr['density_vs_reach_pearson']:+.3f}")
    print(f"  Density vs Reach (Spearman): {corr['density_vs_reach_spearman']:+.3f}")
    print(f"  Density vs Bridge Count (Pearson):  {corr['density_vs_bridge_count_pearson']:+.3f}")
    print(f"  Density vs Bridge Count (Spearman): {corr['density_vs_bridge_count_spearman']:+.3f}")
    print()
    
    print("ROMION PREDICTION:")
    print(f"  {result['prediction']}")
    print()
    
    # Interpretation
    rho_reach = corr['density_vs_reach_spearman']
    if rho_reach < -0.3:
        verdict = "CONSISTENT with ROMION (denser clusters have shorter reach)"
    elif rho_reach > 0.3:
        verdict = "OPPOSITE to ROMION prediction"
    else:
        verdict = "INCONCLUSIVE (weak correlation)"
    
    print(f"VERDICT: {verdict}")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="ROMION Density-Velocity Test")
    parser.add_argument("--log", required=True, help="Path to simulation.jsonl")
    parser.add_argument("--tick", type=int, required=True, help="Tick to analyze")
    parser.add_argument("--wcluster", type=float, default=0.02, help="Cluster threshold")
    parser.add_argument("--wdist", type=float, default=0.01, help="Background threshold")
    parser.add_argument("--wbridge", type=float, default=0.0, help="Bridge threshold")
    parser.add_argument("--min-cluster-size", type=int, default=2, help="Min cluster size")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    result = analyze_density_velocity(
        args.log,
        args.tick,
        args.wcluster,
        args.wdist,
        args.wbridge,
        args.min_cluster_size
    )
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
