#!/usr/bin/env python3
"""
ROMION Phase Propagation Test

Based on ROMION O'LOGIC theory (Annexes M-V):
- Photon is NOT a particle moving through graph
- Photon IS a phase mode (δθ) propagating through bridges
- Before measurement: superposition of all possible paths ("ways of possibility")
- Denser regions = more interference/retraction = slower propagation

This test measures:
1. Phase propagation speed through bridge network
2. Correlation between local density and propagation delay
3. Whether ~0.025 correlation is fundamental or artifact

Author's prediction: Effect should be 0.1% - 7% range
"""

import sys
import json
import argparse
import numpy as np
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set, Optional

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


class PhaseField:
    """
    Represents phase field θ on clusters.
    Phase propagates through bridges.
    """
    
    def __init__(self, n_clusters: int):
        self.n_clusters = n_clusters
        # Phase value for each cluster (0 to 2π)
        self.theta: Dict[int, float] = {c: 0.0 for c in range(n_clusters)}
        # Phase "amplitude" (how much signal is present)
        self.amplitude: Dict[int, float] = {c: 0.0 for c in range(n_clusters)}
    
    def inject_phase(self, cluster: int, phase: float = np.pi, amplitude: float = 1.0):
        """Inject phase signal at a cluster (simulates emission)."""
        self.theta[cluster] = phase
        self.amplitude[cluster] = amplitude
    
    def propagate_step(
        self, 
        bridges: Dict[Tuple[int, int], any],
        meta_bg: Dict[Tuple[int, int], float],
        damping: float = 0.1,
        coupling: float = 0.5
    ) -> Dict[int, float]:
        """
        One step of phase propagation through bridges.
        
        Returns dict of amplitude changes (for measuring propagation).
        
        Physics:
        - Phase flows through bridges
        - Amplitude decays with distance (damping)
        - Multiple paths can interfere (coupling)
        """
        new_theta = self.theta.copy()
        new_amplitude = self.amplitude.copy()
        changes = {}
        
        # For each bridge, propagate phase
        for (c1, c2), bridge_agg in bridges.items():
            # Get distance in meta_bg (affects damping)
            pair = (min(c1, c2), max(c1, c2))
            dist = meta_bg.get(pair, 1.0)
            
            # Bridge strength (count * weight)
            strength = bridge_agg.count * (bridge_agg.w_sum / max(bridge_agg.count, 1))
            
            # Propagation factor (stronger bridges = better propagation)
            prop_factor = coupling * strength / (1.0 + damping * dist)
            
            # Propagate from c1 to c2 if c1 has amplitude
            if self.amplitude[c1] > 0.01:
                delta = prop_factor * self.amplitude[c1]
                new_amplitude[c2] += delta
                # Phase follows (with some mixing)
                if new_amplitude[c2] > 0:
                    # Weighted average of phases
                    old_contrib = (new_amplitude[c2] - delta) * new_theta[c2]
                    new_contrib = delta * self.theta[c1]
                    new_theta[c2] = (old_contrib + new_contrib) / new_amplitude[c2]
                changes[c2] = changes.get(c2, 0) + delta
            
            # Propagate from c2 to c1 if c2 has amplitude
            if self.amplitude[c2] > 0.01:
                delta = prop_factor * self.amplitude[c2]
                new_amplitude[c1] += delta
                if new_amplitude[c1] > 0:
                    old_contrib = (new_amplitude[c1] - delta) * new_theta[c1]
                    new_contrib = delta * self.theta[c2]
                    new_theta[c1] = (old_contrib + new_contrib) / new_amplitude[c1]
                changes[c1] = changes.get(c1, 0) + delta
        
        # Apply damping to all amplitudes
        for c in range(self.n_clusters):
            new_amplitude[c] *= (1.0 - damping)
        
        self.theta = new_theta
        self.amplitude = new_amplitude
        
        return changes
    
    def get_reached_clusters(self, threshold: float = 0.01) -> Set[int]:
        """Get clusters where amplitude is above threshold."""
        return {c for c, a in self.amplitude.items() if a > threshold}


def compute_cluster_internal_density(
    edges: List,
    node2c: List[int],
    n_clusters: int
) -> Dict[int, float]:
    """
    Compute internal edge density for each cluster.
    Density = sum of internal edge weights / node count
    """
    nodes_per_cluster = defaultdict(int)
    for c in node2c:
        if c >= 0:
            nodes_per_cluster[c] += 1
    
    internal_weight = defaultdict(float)
    for e in edges:
        u, v, w = e[0], e[1], e[2]
        cu = node2c[u] if u < len(node2c) else -1
        cv = node2c[v] if v < len(node2c) else -1
        if cu >= 0 and cu == cv:
            internal_weight[cu] += w
    
    density = {}
    for c in range(n_clusters):
        n_nodes = nodes_per_cluster.get(c, 0)
        if n_nodes > 0:
            density[c] = internal_weight.get(c, 0.0) / n_nodes
        else:
            density[c] = 0.0
    
    return density


def measure_propagation_time(
    source: int,
    targets: Set[int],
    bridges: Dict[Tuple[int, int], any],
    meta_bg: Dict[Tuple[int, int], float],
    n_clusters: int,
    max_steps: int = 100,
    threshold: float = 0.01
) -> Dict[int, int]:
    """
    Measure how many steps it takes for phase to reach each target from source.
    Returns {target_cluster: steps_to_reach} or -1 if not reached.
    """
    field = PhaseField(n_clusters)
    field.inject_phase(source)
    
    arrival_times = {}
    
    for step in range(max_steps):
        field.propagate_step(bridges, meta_bg)
        reached = field.get_reached_clusters(threshold)
        
        for t in targets:
            if t in reached and t not in arrival_times:
                arrival_times[t] = step + 1
        
        # Stop if all targets reached
        if all(t in arrival_times for t in targets):
            break
    
    # Mark unreached as -1
    for t in targets:
        if t not in arrival_times:
            arrival_times[t] = -1
    
    return arrival_times


def analyze_phase_propagation(
    log_path: str,
    tick: int,
    wcluster: float = 0.02,
    wdist: float = 0.01,
    wbridge: float = 0.0,
    min_cluster_size: int = 2,
    n_sources: int = 10
) -> Dict:
    """
    Main analysis: measure phase propagation and correlate with density.
    """
    # Load data
    snapshot = load_graph_snapshot(log_path, tick)
    if not snapshot:
        return {"error": f"No GRAPH snapshot at tick {tick}"}
    
    edges = snapshot['edges']
    n = infer_n(edges)
    
    # Build clusters
    adj = build_node_adj_threshold(edges, wcluster)
    comps = find_components(n, adj)
    if min_cluster_size > 1:
        comps = [c for c in comps if len(c) >= min_cluster_size]
    
    node2c = assign_clusters(comps, n)
    n_clusters = len(comps)
    
    if n_clusters < 5:
        return {"error": f"Not enough clusters: {n_clusters}"}
    
    # Build meta-graph and bridges
    meta_bg = build_cluster_graph_from_edges(edges, node2c, wdist)
    bridges, _ = count_bridges(edges, node2c, wbridge)
    
    if len(bridges) < 3:
        return {"error": f"Not enough bridges: {len(bridges)}"}
    
    # Compute densities
    density = compute_cluster_internal_density(edges, node2c, n_clusters)
    
    # Find clusters with bridges (can be sources/targets)
    clusters_with_bridges = set()
    for (c1, c2) in bridges.keys():
        clusters_with_bridges.add(c1)
        clusters_with_bridges.add(c2)
    
    clusters_list = list(clusters_with_bridges)
    
    if len(clusters_list) < 5:
        return {"error": f"Not enough clusters with bridges: {len(clusters_list)}"}
    
    # Sample sources and measure propagation
    np.random.seed(42)
    sources = np.random.choice(clusters_list, size=min(n_sources, len(clusters_list)), replace=False)
    
    propagation_data = []
    
    for source in sources:
        targets = set(clusters_list) - {source}
        arrival_times = measure_propagation_time(
            source, targets, bridges, meta_bg, n_clusters
        )
        
        source_density = density.get(source, 0.0)
        
        for target, time in arrival_times.items():
            if time > 0:  # Successfully reached
                target_density = density.get(target, 0.0)
                avg_density = (source_density + target_density) / 2
                
                # Get meta-distance
                pair = (min(source, target), max(source, target))
                meta_dist = meta_bg.get(pair, -1)
                
                propagation_data.append({
                    'source': source,
                    'target': target,
                    'time': time,
                    'source_density': source_density,
                    'target_density': target_density,
                    'avg_density': avg_density,
                    'meta_dist': meta_dist
                })
    
    if len(propagation_data) < 5:
        return {"error": f"Not enough propagation data: {len(propagation_data)}"}
    
    # Compute correlations
    times = [d['time'] for d in propagation_data]
    avg_densities = [d['avg_density'] for d in propagation_data]
    meta_dists = [d['meta_dist'] for d in propagation_data if d['meta_dist'] > 0]
    times_with_dist = [d['time'] for d in propagation_data if d['meta_dist'] > 0]
    
    from scipy.stats import spearmanr, pearsonr
    
    # Density vs Time correlation
    # ROMION predicts: POSITIVE (denser = slower = more time)
    if np.std(avg_densities) > 0 and np.std(times) > 0:
        density_time_pearson, _ = pearsonr(avg_densities, times)
        density_time_spearman, _ = spearmanr(avg_densities, times)
    else:
        density_time_pearson = 0.0
        density_time_spearman = 0.0
    
    # Distance vs Time correlation (sanity check - should be positive)
    if len(meta_dists) > 3 and np.std(meta_dists) > 0 and np.std(times_with_dist) > 0:
        dist_time_spearman, _ = spearmanr(meta_dists, times_with_dist)
    else:
        dist_time_spearman = 0.0
    
    # Compute "propagation speed" effect
    # Group by density quartiles and compare average times
    sorted_by_density = sorted(propagation_data, key=lambda x: x['avg_density'])
    n_data = len(sorted_by_density)
    q1_data = sorted_by_density[:n_data//4]
    q4_data = sorted_by_density[3*n_data//4:]
    
    if q1_data and q4_data:
        avg_time_low_density = np.mean([d['time'] for d in q1_data])
        avg_time_high_density = np.mean([d['time'] for d in q4_data])
        speed_effect_percent = 100 * (avg_time_high_density - avg_time_low_density) / avg_time_low_density if avg_time_low_density > 0 else 0
    else:
        avg_time_low_density = 0
        avg_time_high_density = 0
        speed_effect_percent = 0
    
    return {
        "tick": tick,
        "n_clusters": n_clusters,
        "clusters_with_bridges": len(clusters_with_bridges),
        "n_bridges": len(bridges),
        "n_propagations_measured": len(propagation_data),
        "correlations": {
            "density_vs_time_pearson": density_time_pearson,
            "density_vs_time_spearman": density_time_spearman,
            "distance_vs_time_spearman": dist_time_spearman
        },
        "speed_effect": {
            "avg_time_low_density_quartile": avg_time_low_density,
            "avg_time_high_density_quartile": avg_time_high_density,
            "slowdown_percent": speed_effect_percent
        },
        "prediction": "ROMION predicts density_vs_time should be POSITIVE (denser = slower)",
        "expected_effect_range": "0.1% to 7% (author estimate)"
    }


def print_report(result: Dict):
    """Print formatted report."""
    if "error" in result:
        print(f"ERROR: {result['error']}")
        return
    
    print("=" * 70)
    print("ROMION PHASE PROPAGATION TEST")
    print("=" * 70)
    print()
    print(f"Tick: {result['tick']}")
    print(f"Total clusters: {result['n_clusters']}")
    print(f"Clusters with bridges: {result['clusters_with_bridges']}")
    print(f"Total bridges: {result['n_bridges']}")
    print(f"Propagations measured: {result['n_propagations_measured']}")
    print()
    
    print("CORRELATIONS:")
    corr = result['correlations']
    print(f"  Density vs Time (Pearson):  {corr['density_vs_time_pearson']:+.4f}")
    print(f"  Density vs Time (Spearman): {corr['density_vs_time_spearman']:+.4f}")
    print(f"  Distance vs Time (Spearman): {corr['distance_vs_time_spearman']:+.4f} (sanity check)")
    print()
    
    print("SPEED EFFECT (comparing density quartiles):")
    se = result['speed_effect']
    print(f"  Avg time in LOW density quartile:  {se['avg_time_low_density_quartile']:.2f} steps")
    print(f"  Avg time in HIGH density quartile: {se['avg_time_high_density_quartile']:.2f} steps")
    print(f"  Slowdown effect: {se['slowdown_percent']:+.2f}%")
    print()
    
    print("ROMION PREDICTION:")
    print(f"  {result['prediction']}")
    print(f"  Expected effect range: {result['expected_effect_range']}")
    print()
    
    # Interpretation
    rho = corr['density_vs_time_spearman']
    effect = se['slowdown_percent']
    
    if rho > 0.1 and effect > 0:
        verdict = "CONSISTENT with ROMION (denser regions slow propagation)"
    elif rho < -0.1 and effect < 0:
        verdict = "OPPOSITE to ROMION prediction"
    else:
        verdict = "WEAK EFFECT - may need more data or different parameters"
    
    print(f"VERDICT: {verdict}")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="ROMION Phase Propagation Test")
    parser.add_argument("--log", required=True, help="Path to simulation.jsonl")
    parser.add_argument("--tick", type=int, required=True, help="Tick to analyze")
    parser.add_argument("--wcluster", type=float, default=0.02)
    parser.add_argument("--wdist", type=float, default=0.01)
    parser.add_argument("--wbridge", type=float, default=0.0)
    parser.add_argument("--n-sources", type=int, default=10, help="Number of source clusters to test")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    result = analyze_phase_propagation(
        args.log,
        args.tick,
        args.wcluster,
        args.wdist,
        args.wbridge,
        n_sources=args.n_sources
    )
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
