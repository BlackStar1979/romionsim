"""Channel / anisotropy metrics for gravity_test.

All metrics here MUST operate on the background cluster meta-graph
(i.e., constructed using wdist / clustering logic), not on bridge-only graphs.

Status: PARTIAL (MVP proxy - cut_weight only, no path-based capacity)

Notes:
- "Channel capacity" is implemented as a conservative MVP proxy: cut weight
  across a deterministic region split.
- "Anisotropy" is implemented as split-axis variability, since the meta-graph
  is undirected (no intrinsic direction) unless the simulation later adds it.
"""

from __future__ import annotations

import statistics
from typing import Dict, List, Optional, Set, Tuple

from .regions import split_regions, MetaGraph


def path_capacity(
    cluster_graph: MetaGraph,
    L: Set[int],
    R: Set[int],
    mode: str = "cut_weight",
    max_dist: Optional[int] = None
) -> Tuple[float, Dict]:
    """Compute channel capacity between regions on the cluster meta-graph.

    Args:
        cluster_graph: {(a,b): weight} background meta-graph.
        L, R: Disjoint region sets over cluster IDs.
        mode: Currently only 'cut_weight' (MVP).
        max_dist: Reserved for future path-based modes.

    Returns:
        (capacity, meta)

    Raises:
        ValueError: If unknown mode.
    """
    if mode != "cut_weight":
        raise ValueError(f"Unknown capacity mode: {mode}")

    cut_edges = 0
    cut_weight = 0.0
    
    for (a, b), w in cluster_graph.items():
        if (a in L and b in R) or (a in R and b in L):
            cut_edges += 1
            cut_weight += float(w)

    meta = {
        "mode": mode,
        "cut_edges": cut_edges,
        "max_dist": max_dist,
        "L_size": len(L),
        "R_size": len(R),
    }
    return cut_weight, meta


def anisotropy_index(
    cluster_graph: MetaGraph,
    n_clusters: int,
    n_splits: int = 5,
    split_method: str = "bfs_seed",
    capacity_mode: str = "cut_weight",
    eps: float = 1e-12
) -> Tuple[float, Dict]:
    """Compute a split-axis anisotropy index on the background meta-graph.

    Because the meta-graph is undirected, we define "anisotropy" as the
    variability of channel capacity across multiple deterministic split axes.

    Definition (MVP):
        Anisotropy = (max(Cap_i) - median(Cap_i)) / (median(Cap_i) + eps)

    Args:
        cluster_graph: Background meta-graph.
        n_clusters: Total clusters.
        n_splits: How many split axes (seed clusters) to evaluate.
        split_method: Region split method.
        capacity_mode: Capacity mode passed to path_capacity.
        eps: Numerical stabilizer.

    Returns:
        (anisotropy, meta)

    Raises:
        ValueError: If n_clusters < 2 or n_splits < 1.
    """
    if n_clusters < 2:
        raise ValueError(f"anisotropy_index requires n_clusters>=2, got {n_clusters}")
    if n_splits < 1:
        raise ValueError(f"n_splits must be >=1, got {n_splits}")

    # Choose candidate seeds deterministically by (degree desc, id asc)
    deg = [0] * n_clusters
    for (a, b) in cluster_graph.keys():
        if a != b:
            if 0 <= a < n_clusters:
                deg[a] += 1
            if 0 <= b < n_clusters:
                deg[b] += 1
    
    seeds = sorted(range(n_clusters), key=lambda i: (-deg[i], i))
    seeds = seeds[:min(n_splits, len(seeds))]

    caps: List[float] = []
    metas: List[Dict] = []
    
    for s in seeds:
        try:
            L, R, split_meta = split_regions(
                cluster_graph, n_clusters, method=split_method, seed_cluster=s
            )
            cap, cap_meta = path_capacity(cluster_graph, L, R, mode=capacity_mode)
            caps.append(float(cap))
            metas.append({"seed": s, "split": split_meta, "cap": cap_meta})
        except ValueError:
            # Skip degenerate splits
            continue

    if not caps:
        # All splits failed - degenerate
        return 0.0, {
            "split_method": split_method,
            "capacity_mode": capacity_mode,
            "n_splits": 0,
            "caps": [],
            "median": 0.0,
            "max": 0.0,
            "degenerate": True,
            "details": [],
        }

    med = statistics.median(caps)
    mx = max(caps)

    if med <= 0.0:
        # Degenerate: no cross-region capacity on any axis
        anis = 0.0
        degenerate = True
    else:
        anis = (mx - med) / (med + eps)
        degenerate = False

    meta = {
        "split_method": split_method,
        "capacity_mode": capacity_mode,
        "n_splits": len(seeds),
        "caps": caps,
        "median": med,
        "max": mx,
        "degenerate": degenerate,
        "details": metas,
    }
    return float(anis), meta
