#!/usr/bin/env python3
"""
ROMION Gravity Test (Test B) - Fixed Version

Fixes based on ChatGPT requirements:
1. Separate thresholds: --wcluster vs --wbridge
2. All-pairs mode: compute correlation on ALL cluster pairs (zeros for no bridges)
3. Explicit degeneracy reporting (not just 'nan')
4. Temporal/batch analysis: --tick-range
5. Hubness metric: detect star topology
6. Multiple correlations: count, weight, log(count), log(weight)

Critical fix: Clusters defined by w>=wcluster, bridges by w>=wbridge
This separates "object" (cluster) from "field" (bridge)

Usage:
    # Single snapshot with proper thresholds
    python analysis/gravity_test.py --log simulation.jsonl --tick 200 --wcluster 0.02 --wbridge 0.0 --all-pairs
    
    # Temporal analysis (hysteresis)
    python analysis/gravity_test.py --log simulation.jsonl --tick-range 50:1200:50 --wcluster 0.02 --wbridge 0.0 --all-pairs --csv gravity_time.csv
"""

import argparse
import json
import math
import csv
from collections import defaultdict, deque
from pathlib import Path


def read_jsonl(path):
    """Yield parsed JSON objects from JSONL file."""
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def build_adj_from_edges(edges, wmin):
    """Build adjacency list for edges with w >= wmin."""
    adj = defaultdict(list)
    for u, v, w in edges:
        # Safe weight handling
        w = float(w) if w is not None else 0.0
        if w >= wmin:
            adj[u].append(v)
            adj[v].append(u)
    return adj


def find_components(adj):
    """Find connected components via DFS."""
    seen = set()
    comps = []
    
    for n in adj.keys():
        if n in seen:
            continue
            
        stack = [n]
        seen.add(n)
        comp = []
        
        while stack:
            x = stack.pop()
            comp.append(x)
            for y in adj.get(x, []):
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        
        comps.append(comp)
    
    return comps


def count_bridges(edges, comp_id, wbridge):
    """
    Count bridges between clusters.
    
    CRITICAL: Clusters are pre-defined (from wcluster)
    Bridges are ANY edge w>=wbridge connecting different clusters
    
    This separates "object definition" from "field/interaction"
    """
    bridge_count = defaultdict(int)
    bridge_weight = defaultdict(float)
    
    for u, v, w in edges:
        # Safe weight handling (A: treat missing/None as 0.0)
        w = float(w) if w is not None else 0.0
        
        if w < wbridge:
            continue
            
        ci = comp_id.get(u)
        cj = comp_id.get(v)
        
        if ci is None or cj is None or ci == cj:
            continue
        
        # Normalize pair
        a, b = (ci, cj) if ci < cj else (cj, ci)
        bridge_count[(a, b)] += 1
        bridge_weight[(a, b)] += w
    
    return bridge_count, bridge_weight


def bfs_distance(meta_adj, start):
    """BFS distances in meta-graph."""
    dist = {start: 0}
    queue = deque([start])
    
    while queue:
        x = queue.popleft()
        for y in meta_adj.get(x, []):
            if y not in dist:
                dist[y] = dist[x] + 1
                queue.append(y)
    
    return dist


def all_pairs_distances(n_clusters, meta_adj):
    """
    Compute distances for ALL pairs of clusters.
    
    Returns dict: (ci, cj) -> distance
    If disconnected: distance = None (will be filtered)
    """
    distances = {}
    
    for i in range(n_clusters):
        dist_from_i = bfs_distance(meta_adj, i)
        for j in range(i + 1, n_clusters):
            d = dist_from_i.get(j)
            distances[(i, j)] = d
    
    return distances


def spearman_correlation(xs, ys):
    """Spearman rank correlation."""
    if len(xs) < 3:
        return float("nan"), "too_few_points"
    
    # Check for constant
    if len(set(xs)) == 1:
        return float("nan"), "x_constant"
    if len(set(ys)) == 1:
        return float("nan"), "y_constant"
    
    def rank(a):
        sorted_with_idx = sorted((v, i) for i, v in enumerate(a))
        ranks = [0.0] * len(a)
        
        i = 0
        while i < len(sorted_with_idx):
            j = i
            while j + 1 < len(sorted_with_idx) and sorted_with_idx[j + 1][0] == sorted_with_idx[i][0]:
                j += 1
            
            avg_rank = (i + j) / 2.0 + 1
            
            for k in range(i, j + 1):
                ranks[sorted_with_idx[k][1]] = avg_rank
            
            i = j + 1
        
        return ranks
    
    rx = rank(xs)
    ry = rank(ys)
    n = len(xs)
    
    mx = sum(rx) / n
    my = sum(ry) / n
    
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    
    denx = math.sqrt(sum((rx[i] - mx) ** 2 for i in range(n)))
    deny = math.sqrt(sum((ry[i] - my) ** 2 for i in range(n)))
    
    if denx == 0 or deny == 0:
        return float("nan"), "zero_variance"
    
    return num / (denx * deny), "ok"


def compute_hubness(meta_adj, n_clusters):
    """
    Compute hubness metric.
    
    Detects if topology is star-like (one central hub)
    vs distributed network.
    
    Returns:
        hub_id: cluster with max degree
        hub_degree: its degree
        hub_share: degree / total_edges
        max_mean_ratio: max_deg / mean_deg
    """
    degrees = [0] * n_clusters
    
    for i in meta_adj:
        degrees[i] = len(meta_adj[i])
    
    if not degrees or max(degrees) == 0:
        return -1, 0, 0.0, 0.0
    
    hub_id = degrees.index(max(degrees))
    hub_degree = degrees[hub_id]
    
    total_edges = sum(degrees) // 2  # Undirected
    hub_share = hub_degree / total_edges if total_edges > 0 else 0.0
    
    mean_deg = sum(degrees) / len(degrees) if len(degrees) > 0 else 0.0
    max_mean_ratio = hub_degree / mean_deg if mean_deg > 0 else 0.0
    
    return hub_id, hub_degree, hub_share, max_mean_ratio


def analyze_snapshot(edges, wcluster, wbridge, all_pairs=True, exclude_hub=False, 
                     disconnected_policy='drop', tick=None):
    """
    Analyze single snapshot with proper cluster/bridge separation.
    
    Args:
        edges: List of [u, v, w]
        wcluster: Threshold for defining clusters (objects)
        wbridge: Threshold for counting bridges (field)
        all_pairs: If True, include pairs with no bridges (count=0)
        exclude_hub: If True, compute correlations excluding hub pairs
        disconnected_policy: 'drop' or 'maxdist' for pairs without path
        tick: Tick number for reporting
    """
    # 1. Define clusters (objects) using wcluster
    adj_cluster = build_adj_from_edges(edges, wcluster)
    comps = find_components(adj_cluster)
    n_clusters = len(comps)
    
    # Map nodes to clusters
    comp_id = {}
    for i, c in enumerate(comps):
        for n in c:
            comp_id[n] = i
    
    # 2. Count bridges (field/interactions) using wbridge
    bridge_count, bridge_weight = count_bridges(edges, comp_id, wbridge)
    
    # 3. Build meta-graph from bridges
    meta_adj = defaultdict(list)
    for (a, b) in bridge_count.keys():
        meta_adj[a].append(b)
        meta_adj[b].append(a)
    
    # 4. Compute hubness
    hub_id, hub_deg, hub_share, hub_ratio = compute_hubness(meta_adj, n_clusters)
    
    # 5. Prepare data for correlation
    if all_pairs:
        # ALL pairs of clusters
        all_dists = all_pairs_distances(n_clusters, meta_adj)
        
        dists = []
        counts = []
        weights = []
        
        for (i, j), d in all_dists.items():
            if d is None:
                continue  # Disconnected in meta-graph
            
            cnt = bridge_count.get((i, j), 0)
            wgt = bridge_weight.get((i, j), 0.0)
            
            dists.append(d)
            counts.append(cnt)
            weights.append(wgt)
        
        n_pairs = len(dists)
        n_with_bridges = sum(1 for c in counts if c > 0)
    else:
        # Only pairs with bridges
        dists = []
        counts = []
        weights = []
        
        for (a, b), cnt in bridge_count.items():
            distmap = bfs_distance(meta_adj, a)
            d = distmap.get(b)
            
            if d is None:
                continue
            
            dists.append(d)
            counts.append(cnt)
            weights.append(bridge_weight[(a, b)])
        
        n_pairs = len(dists)
        n_with_bridges = n_pairs
    
    # 6. Compute correlations (ChatGPT requirement: 4 correlations)
    rho_count, status_count = spearman_correlation(dists, counts)
    rho_weight, status_weight = spearman_correlation(dists, weights)
    
    # Log transforms (stabilize heavy tails)
    log_counts = [math.log(1 + c) for c in counts]
    log_weights = [math.log(1 + w) for w in weights]
    
    rho_log_count, status_log_count = spearman_correlation(dists, log_counts)
    rho_log_weight, status_log_weight = spearman_correlation(dists, log_weights)
    
    # Statistics
    total_bridge_count = sum(counts)
    total_bridge_weight = sum(weights)
    
    return {
        "tick": tick,
        "n_clusters": n_clusters,
        "n_pairs": n_pairs,
        "n_with_bridges": n_with_bridges,
        "rho_count": rho_count,
        "rho_weight": rho_weight,
        "rho_log_count": rho_log_count,
        "rho_log_weight": rho_log_weight,
        "status_count": status_count,
        "status_weight": status_weight,
        "status_log_count": status_log_count,
        "status_log_weight": status_log_weight,
        "total_bridge_count": total_bridge_count,
        "total_bridge_weight": total_bridge_weight,
        "hub_id": hub_id,
        "hub_degree": hub_deg,
        "hub_share": hub_share,
        "hub_ratio": hub_ratio,
        "top_bridges": sorted(zip(counts, weights, dists), reverse=True)[:10] if counts else []
    }


def format_rho(rho, status):
    """Format correlation with status."""
    if status != "ok":
        return f"nan ({status})"
    if math.isnan(rho):
        return "nan"
    return f"{rho:>6.3f}"


def print_report(result):
    """Print detailed report for single snapshot."""
    print("=" * 70)
    print(f"ROMION Gravity Test @ tick={result['tick']}")
    print("=" * 70)
    print(f"Clusters: {result['n_clusters']} | "
          f"Pairs analyzed: {result['n_pairs']} | "
          f"With bridges: {result['n_with_bridges']}")
    print()
    
    # Hubness
    if result['hub_id'] >= 0:
        print(f"Hub topology: cluster {result['hub_id']} "
              f"(degree={result['hub_degree']}, "
              f"share={result['hub_share']:.1%}, "
              f"max/mean={result['hub_ratio']:.1f})")
        if result['hub_ratio'] > 3.0:
            print("  WARNING: Strong hub detected - may dominate correlation")
        print()
    
    # Correlations
    print("Spearman correlations (dist vs bridges):")
    print(f"  count:        {format_rho(result['rho_count'], result['status_count'])}")
    print(f"  weight:       {format_rho(result['rho_weight'], result['status_weight'])}")
    print(f"  log(1+count): {format_rho(result['rho_log_count'], result['status_log_count'])}")
    print(f"  log(1+weight):{format_rho(result['rho_log_weight'], result['status_log_weight'])}")
    print()
    
    # Interpretation
    best_rho = result['rho_weight']
    if not math.isnan(best_rho):
        if best_rho < -0.3:
            print("[PASS] Negative correlation: 'closer' -> 'more bridges'")
            print("       Consistent with gravity-like attraction")
        elif best_rho > 0.3:
            print("[WARN] Positive correlation: 'farther' -> 'more bridges'")
            print("       Anti-gravitational or hub-dominated")
        else:
            print("[WEAK] Weak correlation: no clear gravitational effect")
    
    # Top bridges
    if result['top_bridges']:
        print()
        print("Top 10 bridges (count, weight, dist):")
        for cnt, wgt, d in result['top_bridges']:
            print(f"  {cnt:>5}  {wgt:>7.2f}  {d:>3}")


def main():
    ap = argparse.ArgumentParser(
        description='ROMION Gravity Test - Fixed with Cluster/Bridge Separation',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    ap.add_argument('--log', required=True,
                    help='Path to simulation.jsonl with GRAPH dumps')
    
    # Thresholds (CRITICAL FIX)
    ap.add_argument('--wcluster', type=float, default=0.02,
                    help='Threshold for defining clusters (objects/matter)')
    ap.add_argument('--wbridge', type=float, default=0.0,
                    help='Threshold for counting bridges (field/interaction)')
    
    # Analysis mode
    ap.add_argument('--all-pairs', action='store_true',
                    help='Include ALL cluster pairs (zeros for no bridges)')
    
    # Snapshot selection
    ap.add_argument('--tick', type=int, default=None,
                    help='Single snapshot at this tick')
    ap.add_argument('--tick-range', default=None,
                    help='Temporal analysis: start:end:step (e.g., 50:1200:50)')
    
    # Output
    ap.add_argument('--csv', default=None,
                    help='Save temporal results to CSV')
    
    args = ap.parse_args()
    
    # Collect snapshots
    snapshots = []
    for rec in read_jsonl(args.log):
        if rec.get("type") == "GRAPH":
            t = rec.get("tick")
            edges = rec.get("edges", [])
            snapshots.append((t, edges))
    
    if not snapshots:
        print("ERROR: No GRAPH records found in log.")
        print("Run with: run_romion_extended.py --dump-graph-every N")
        return 1
    
    # Parse tick range
    if args.tick_range:
        parts = args.tick_range.split(':')
        if len(parts) != 3:
            print("ERROR: --tick-range must be start:end:step")
            return 1
        
        start, end, step = map(int, parts)
        target_ticks = list(range(start, end + 1, step))
        
        # Find nearest snapshots
        results = []
        for target in target_ticks:
            best_idx = min(range(len(snapshots)),
                          key=lambda i: abs(snapshots[i][0] - target))
            tick, edges = snapshots[best_idx]
            
            result = analyze_snapshot(edges, args.wcluster, args.wbridge,
                                     args.all_pairs, tick)
            results.append(result)
        
        # Save CSV
        if args.csv:
            csv_path = Path(args.csv)
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(csv_path, 'w', newline='') as f:
                fieldnames = ['tick', 'n_clusters', 'n_pairs', 'n_with_bridges',
                             'rho_count', 'rho_weight', 'rho_log_count', 'rho_log_weight',
                             'total_bridge_count', 'total_bridge_weight',
                             'hub_id', 'hub_degree', 'hub_share', 'hub_ratio']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for r in results:
                    writer.writerow({k: r[k] for k in fieldnames})
            
            print(f"Saved temporal results: {csv_path}")
        
        # Print summary
        print(f"Temporal Analysis: {len(results)} snapshots")
        print("=" * 70)
        print(f"{'Tick':<6} | {'Clusters':<8} | {'Pairs':<6} | "
              f"{'rho_wgt':<8} | {'Bridges':<8}")
        print("-" * 70)
        
        for r in results:
            rho_str = format_rho(r['rho_weight'], r['status_weight'])
            print(f"{r['tick']:<6} | {r['n_clusters']:<8} | {r['n_pairs']:<6} | "
                  f"{rho_str:<8} | {r['n_with_bridges']:<8}")
        
        return 0
    
    # Single snapshot
    if args.tick is None:
        tick, edges = snapshots[-1]
    else:
        best_idx = min(range(len(snapshots)),
                      key=lambda i: abs(snapshots[i][0] - args.tick))
        tick, edges = snapshots[best_idx]
    
    result = analyze_snapshot(edges, args.wcluster, args.wbridge,
                             args.all_pairs, tick)
    print_report(result)
    
    return 0


if __name__ == "__main__":
    exit(main())
