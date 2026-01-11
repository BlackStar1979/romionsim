"""Region split utilities for gravity_test.

This module provides deterministic ways to split the *cluster meta-graph*
(background geometry) into regions without assuming any embedding coordinates.

Why this exists (ROMION methodology):
- Channels / anisotropy must be measured on the background geometry (wdist),
  not on the bridge graph (wbridge).
- Region splits must be deterministic and auditable (fail-closed).

Status: MVP
"""

from __future__ import annotations

from collections import deque
from typing import Dict, List, Optional, Set, Tuple


MetaGraph = Dict[Tuple[int, int], float]


def _build_cluster_adj(meta_edges: MetaGraph, n_clusters: int) -> List[List[int]]:
    """Build adjacency list for clusters from meta-graph edges."""
    adj: List[List[int]] = [[] for _ in range(n_clusters)]
    for (a, b), _w in meta_edges.items():
        if a == b:
            continue
        if 0 <= a < n_clusters and 0 <= b < n_clusters:
            adj[a].append(b)
            adj[b].append(a)
    # Deterministic traversal - sort neighbors
    for i in range(n_clusters):
        adj[i] = sorted(set(adj[i]))
    return adj


def _degree(meta_edges: MetaGraph, n_clusters: int) -> List[int]:
    """Compute degree of each cluster in meta-graph."""
    deg = [0] * n_clusters
    for (a, b) in meta_edges.keys():
        if a != b:
            if 0 <= a < n_clusters:
                deg[a] += 1
            if 0 <= b < n_clusters:
                deg[b] += 1
    return deg


def split_regions(
    cluster_graph: MetaGraph,
    n_clusters: int,
    method: str = "bfs_seed",
    seed_cluster: Optional[int] = None,
    topk: Optional[int] = None
) -> Tuple[Set[int], Set[int], Dict]:
    """Split clusters into two regions (L, R) deterministically.

    Args:
        cluster_graph: Background meta-graph edges {(a,b): weight}.
        n_clusters: Total clusters (0..n_clusters-1).
        method: Split method. Currently: 'bfs_seed'.
        seed_cluster: Optional seed cluster for BFS.
        topk: Reserved for future methods.

    Returns:
        (L, R, meta) where meta contains diagnostics.

    Raises:
        ValueError: On invalid n_clusters or if split degenerates.
    """
    if n_clusters < 2:
        raise ValueError(f"split_regions requires n_clusters>=2, got {n_clusters}")

    if method != "bfs_seed":
        raise ValueError(f"Unknown split method: {method}")

    deg = _degree(cluster_graph, n_clusters)

    # Choose seed deterministically: highest degree, tie -> smallest id
    if seed_cluster is None:
        seed_cluster = min(
            range(n_clusters),
            key=lambda i: (-deg[i], i)
        )
    if not (0 <= seed_cluster < n_clusters):
        raise ValueError(f"Invalid seed_cluster={seed_cluster} for n_clusters={n_clusters}")

    adj = _build_cluster_adj(cluster_graph, n_clusters)

    # BFS traversal from seed; order is deterministic because adjacency sorted
    q = deque([seed_cluster])
    seen = [False] * n_clusters
    seen[seed_cluster] = True
    order: List[int] = []

    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                q.append(v)

    # Append unreachable clusters in sorted order (disconnected components)
    unreachable = sorted(i for i in range(n_clusters) if not seen[i])
    order.extend(unreachable)

    # Deterministic, balanced assignment
    L: Set[int] = set()
    R: Set[int] = set()
    for idx, cid in enumerate(order):
        if idx == 0:
            L.add(cid)
        elif idx == 1:
            R.add(cid)
        else:
            # Assign to smaller side, tie -> L
            if len(L) <= len(R):
                L.add(cid)
            else:
                R.add(cid)

    # Validation
    if not L or not R:
        raise ValueError(f"Degenerate split produced empty region: |L|={len(L)} |R|={len(R)}")

    if L & R:
        raise ValueError("Split regions are not disjoint")

    if len(L) + len(R) != n_clusters:
        raise ValueError("Split regions do not cover all clusters")

    meta = {
        "method": method,
        "seed_cluster": seed_cluster,
        "n_clusters": n_clusters,
        "degree_max": max(deg) if deg else 0,
        "disconnected_clusters": len(unreachable),
        "L_size": len(L),
        "R_size": len(R),
        "topk": topk,
    }
    return L, R, meta
