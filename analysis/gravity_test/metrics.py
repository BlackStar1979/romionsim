"""
Metrics computation for gravity_test.

Bridge counting, hub analysis, correlations, and distance analysis.
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple


@dataclass
class BridgeAgg:
    """Aggregated bridge statistics between clusters."""
    w_sum: float = 0.0
    count: int = 0


def _mean(xs: Sequence[float]) -> float:
    """Compute mean of sequence."""
    return sum(xs) / len(xs) if xs else 0.0


def _rankdata(values: Sequence[float]) -> List[float]:
    """
    Convert values to ranks (average rank for ties).
    
    Args:
        values: Input values
        
    Returns:
        Ranks (1-based)
    """
    n = len(values)
    indexed = [(v, i) for i, v in enumerate(values)]
    indexed.sort()
    
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j < n and indexed[j][0] == indexed[i][0]:
            j += 1
        avg_rank = (i + j - 1) / 2.0 + 1.0
        for k in range(i, j):
            ranks[indexed[k][1]] = avg_rank
        i = j
    
    return ranks


def _pearson(x: Sequence[float], y: Sequence[float]) -> float:
    """Pearson correlation coefficient."""
    n = len(x)
    if n == 0:
        return 0.0
    
    mx = _mean(x)
    my = _mean(y)
    
    num = sum((x[i] - mx) * (y[i] - my) for i in range(n))
    dx = sum((x[i] - mx) ** 2 for i in range(n))
    dy = sum((y[i] - my) ** 2 for i in range(n))
    
    if dx == 0 or dy == 0:
        return 0.0
    
    return num / (dx * dy) ** 0.5


def spearmanr(x: Sequence[float], y: Sequence[float]) -> float:
    """
    Spearman rank correlation.
    
    Args:
        x, y: Input sequences
        
    Returns:
        Correlation coefficient
    """
    if len(x) != len(y) or len(x) == 0:
        return 0.0
    
    rx = _rankdata(x)
    ry = _rankdata(y)
    
    return _pearson(rx, ry)


def count_bridges(
    edges: Sequence[Sequence],
    node2c: List[int],
    wbridge: float
) -> Tuple[Dict[Tuple[int, int], BridgeAgg], int]:
    """
    Count inter-cluster bridges.
    
    Args:
        edges: Edge list [u, v, w, ...]
        node2c: Cluster assignment array
        wbridge: Minimum bridge weight
        
    Returns:
        (bridges dict, skipped_edges_unassigned)
        
    Note:
        skipped_edges_unassigned counts EDGES skipped because one or both
        endpoints have node2c[x] == -1. To count unassigned NODES, use:
        sum(1 for c in node2c if c < 0)
    """
    bridges = defaultdict(BridgeAgg)
    skipped_edges_unassigned = 0
    
    for e in edges:
        u, v, w = int(e[0]), int(e[1]), float(e[2])
        
        # Bounds check (safety for malformed data)
        if u >= len(node2c) or v >= len(node2c):
            skipped_edges_unassigned += 1
            continue
        
        cu = node2c[u]
        cv = node2c[v]
        
        # Skip edges with unassigned endpoints
        if cu < 0 or cv < 0:
            skipped_edges_unassigned += 1
            continue
        
        # Skip intra-cluster
        if cu == cv:
            continue
        
        # Skip weak bridges
        if w < wbridge:
            continue
        
        # Add to bridges (ordered pair)
        if cu > cv:
            cu, cv = cv, cu
        
        bridges[(cu, cv)].w_sum += w
        bridges[(cu, cv)].count += 1
    
    return dict(bridges), skipped_edges_unassigned


def build_cluster_graph_from_edges(
    edges: Sequence[Sequence],
    node2c: List[int],
    min_w: float
) -> Dict[Tuple[int, int], float]:
    """
    Build meta-graph of clusters from inter-cluster edges.
    
    CRITICAL: Parameter is min_w (generic threshold), NOT wbridge (field-specific).
    This function is used for BOTH background (wdist) and bridges (wbridge).
    
    Args:
        edges: Edge list
        node2c: Cluster assignments
        min_w: Minimum weight threshold (wdist for background, wbridge for bridges)
        
    Returns:
        Dict of {(cu, cv): total_weight}
    """
    meta = defaultdict(float)
    
    for e in edges:
        u, v, w = int(e[0]), int(e[1]), float(e[2])
        cu, cv = node2c[u], node2c[v]
        
        if cu < 0 or cv < 0 or cu == cv or w < min_w:
            continue
        
        if cu > cv:
            cu, cv = cv, cu
        
        meta[(cu, cv)] += w
    
    return dict(meta)


def compute_hub(
    bridges: Dict[Tuple[int, int], BridgeAgg],
    n_clusters: int
) -> Tuple[int, int, float, float]:
    """
    Compute hub statistics.
    
    Args:
        bridges: Bridge dict
        n_clusters: Total clusters
        
    Returns:
        (hub_id, hub_degree, hub_share, coverage)
    """
    if not bridges:
        return -1, 0, 0.0, 0.0
    
    # Count degree per cluster
    degree = defaultdict(int)
    for (a, b) in bridges.keys():
        # Sanity check
        assert 0 <= a < n_clusters, f"Invalid cluster {a}"
        assert 0 <= b < n_clusters, f"Invalid cluster {b}"
        
        degree[a] += 1
        degree[b] += 1
    
    # Find hub
    hub = max(degree.items(), key=lambda x: x[1])
    hub_id, hub_deg = hub
    
    # Calculate share
    total_connections = sum(degree.values())
    hub_share = (hub_deg / total_connections * 100) if total_connections > 0 else 0.0
    
    # Calculate coverage
    clusters_with_bridges = len(degree)
    coverage = (clusters_with_bridges / n_clusters * 100) if n_clusters > 0 else 0.0
    
    return hub_id, hub_deg, hub_share, coverage


def correlations(
    bridges: Dict[Tuple[int, int], BridgeAgg],
    dists: Dict[Tuple[int, int], int]
) -> Tuple[float, float, float, float]:
    """
    Compute correlations between bridge weight and distance.
    
    Args:
        bridges: Bridge statistics
        dists: Cluster distances
        
    Returns:
        (w_d_pearson, w_d_spearman, n_d_pearson, n_d_spearman)
    """
    pairs = []
    for (a, b), agg in bridges.items():
        d = dists.get((a, b), -1)
        if d >= 0:
            pairs.append((agg.w_sum, agg.count, d))
    
    if not pairs:
        return 0.0, 0.0, 0.0, 0.0
    
    ws = [p[0] for p in pairs]
    ns = [p[1] for p in pairs]
    ds = [float(p[2]) for p in pairs]
    
    w_d_p = _pearson(ws, ds)
    w_d_s = spearmanr(ws, ds)
    n_d_p = _pearson(ns, ds)
    n_d_s = spearmanr(ns, ds)
    
    return w_d_p, w_d_s, n_d_p, n_d_s
