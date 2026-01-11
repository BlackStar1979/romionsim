"""
Distance analysis for gravity_test.

All-pairs shortest paths and distance table generation.

IMPORTANT: Distances must be computed on background geometry (wdist),
NOT on bridge graph (wbridge). Use build_background_cluster_graph()
to create the proper graph for distance calculations.
"""

from collections import defaultdict, deque
from typing import Dict, List, Sequence, Tuple


def build_background_cluster_graph(
    edges: Sequence[Sequence],
    node2c: List[int],
    n_nodes: int,
    wdist: float,
    mode: str = "threshold",
    k: int = 5,
    minw: float = 0.0,
) -> Dict[Tuple[int, int], float]:
    """
    Build cluster-level background graph for distance computation.
    
    This graph is used ONLY for distance calculations and must be
    independent from bridges (wbridge). This is a ROMION methodology
    requirement - background geometry != field.
    
    Args:
        edges: Raw edge list from simulation
        node2c: Node to cluster mapping
        n_nodes: Total number of nodes
        wdist: Weight threshold for background geometry
        mode: "threshold" or "topk"
        k: Top-k edges per node (for topk mode)
        minw: Minimum weight filter for topk prefilter
        
    Returns:
        Cluster meta-graph {(a,b): weight} for distance computation
    """
    from .metrics import build_cluster_graph_from_edges

    if mode == "threshold":
        return build_cluster_graph_from_edges(edges, node2c, min_w=wdist)

    if mode == "topk":
        # Build node topk adjacency first, then lift to clusters
        node_edges: Dict[int, List[Tuple[float, int]]] = defaultdict(list)
        for e in edges:
            u, v, w = int(e[0]), int(e[1]), float(e[2])
            if w < minw:
                continue
            node_edges[u].append((w, v))
            node_edges[v].append((w, u))

        node_adj: Dict[int, List[int]] = {}
        for node, lst in node_edges.items():
            lst.sort(reverse=True, key=lambda x: x[0])
            node_adj[node] = [nbr for (_, nbr) in lst[:k]]

        meta: Dict[Tuple[int, int], float] = defaultdict(float)
        for u, nbrs in node_adj.items():
            if u >= n_nodes:
                continue
            cu = node2c[u] if u < len(node2c) else -1
            if cu < 0:
                continue
            for v in nbrs:
                if v >= n_nodes:
                    continue
                cv = node2c[v] if v < len(node2c) else -1
                if cv < 0 or cu == cv:
                    continue
                a, b = (cu, cv) if cu < cv else (cv, cu)
                meta[(a, b)] += 1.0  # Count edges, not sum weights

        return dict(meta)

    raise ValueError(f"Unknown mode: {mode}")


def all_pairs_cluster_distances(
    meta_edges: Dict[Tuple[int, int], float],
    n_clusters: int
) -> Dict[Tuple[int, int], int]:
    """
    Compute all-pairs shortest path distances on cluster meta-graph.
    
    Uses BFS (unweighted distances).
    
    Args:
        meta_edges: Cluster graph edges
        n_clusters: Number of clusters
        
    Returns:
        Dict of {(a, b): distance}
    """
    # Build adjacency
    adj = [[] for _ in range(n_clusters)]
    for (a, b) in meta_edges.keys():
        adj[a].append(b)
        adj[b].append(a)
    
    # BFS from each cluster
    dists = {}
    for src in range(n_clusters):
        dist = [-1] * n_clusters
        dist[src] = 0
        queue = deque([src])
        
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        
        # Store distances
        for dst in range(n_clusters):
            if src < dst and dist[dst] >= 0:
                dists[(src, dst)] = dist[dst]
    
    return dists


def distance_table(
    bridges: Dict,
    dists: Dict[Tuple[int, int], int]
) -> List[Dict]:
    """
    Generate bridge distance distribution.
    
    ROMION SEMANTICS:
    Computes P(dist | bridge) - probability distribution of distances
    FOR ACTUAL BRIDGED PAIRS, not hypothetical "candidate pairs".
    
    Args:
        bridges: Bridge statistics {(cluster_i, cluster_j): aggregate}
        dists: Background distances {(cluster_i, cluster_j): distance}
        
    Returns:
        List of rows with ROMION-canonical metrics:
        {
            'dist': d,
            'bridged_pairs': count of bridged pairs at distance d,
            'p_dist_given_bridge': P(dist=d | bridge exists),
            'bridges': total bridge count at distance d,
            'weight': total bridge weight at distance d,
            'avg_bridges_per_pair': bridges per bridged pair,
            'avg_weight_per_pair': weight per bridged pair,
            
            # Optional diagnostic (not primary ROMION metric):
            'background_pairs': all pairs at distance d (for reference),
            'p_bridge_given_dist': bridged_pairs / background_pairs
        }
    """
    # Count background pairs at each distance (DIAGNOSTIC ONLY)
    background_pairs_at_dist = {}
    for (a, b), d in dists.items():
        background_pairs_at_dist[d] = background_pairs_at_dist.get(d, 0) + 1
    
    # Group bridges by distance (PRIMARY METRIC)
    by_dist = {}
    for (a, b), agg in bridges.items():
        d = dists.get((a, b), -1)
        if d < 0:
            continue
        
        if d not in by_dist:
            by_dist[d] = {'bridged_pairs': 0, 'bridges': 0, 'weight': 0.0}
        
        by_dist[d]['bridged_pairs'] += 1
        by_dist[d]['bridges'] += agg.count
        by_dist[d]['weight'] += agg.w_sum
    
    # Total bridged pairs (ROMION DENOMINATOR)
    total_bridged_pairs = sum(data['bridged_pairs'] for data in by_dist.values())
    
    # Format table with ROMION canonical metrics
    rows = []
    all_distances = set(background_pairs_at_dist.keys()) | set(by_dist.keys())
    
    for d in sorted(all_distances):
        background_pairs = background_pairs_at_dist.get(d, 0)
        bridge_data = by_dist.get(d, {'bridged_pairs': 0, 'bridges': 0, 'weight': 0.0})
        
        bridged_pairs = bridge_data['bridged_pairs']
        
        # PRIMARY ROMION METRIC: P(dist | bridge)
        p_dist_given_bridge = bridged_pairs / total_bridged_pairs if total_bridged_pairs > 0 else 0.0
        
        # DIAGNOSTIC: P(bridge | dist) - NOT primary physics metric
        p_bridge_given_dist = bridged_pairs / background_pairs if background_pairs > 0 else 0.0
        
        rows.append({
            'dist': d,
            'bridged_pairs': bridged_pairs,
            'p_dist_given_bridge': p_dist_given_bridge,
            'bridges': bridge_data['bridges'],
            'weight': bridge_data['weight'],
            'avg_bridges_per_pair': bridge_data['bridges'] / bridged_pairs if bridged_pairs > 0 else 0.0,
            'avg_weight_per_pair': bridge_data['weight'] / bridged_pairs if bridged_pairs > 0 else 0.0,
            # Diagnostic metrics
            'background_pairs': background_pairs,
            'p_bridge_given_dist': p_bridge_given_dist
        })
    
    return rows


def is_connectivity_only(distance_rows: List[Dict], maxdist_bucket: int) -> bool:
    """
    Check if all bridges are in maxdist bucket (connectivity-only pattern).
    
    Args:
        distance_rows: Distance table rows
        maxdist_bucket: Maximum distance bucket
        
    Returns:
        True if connectivity-only
    """
    return len(distance_rows) == 1 and distance_rows[0]['dist'] == maxdist_bucket
