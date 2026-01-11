"""
Clustering algorithms for gravity_test.

Graph algorithms for component detection and cluster assignment.
"""

from collections import deque
from typing import Dict, List, Sequence, Tuple


def infer_n(edges: Sequence[Sequence]) -> int:
    """Infer number of nodes from edge list."""
    if not edges:
        return 0
    max_node = 0
    for e in edges:
        u, v = int(e[0]), int(e[1])
        if u > max_node:
            max_node = u
        if v > max_node:
            max_node = v
    return max_node + 1


def build_node_adj_threshold(edges: Sequence[Sequence], wmin: float) -> Dict[int, List[int]]:
    """
    Build adjacency list from edges with weight >= wmin.
    
    Args:
        edges: List of [u, v, w, ...]
        wmin: Minimum weight threshold
        
    Returns:
        Adjacency dict {node: [neighbors]}
    """
    adj = {}
    for e in edges:
        u, v, w = int(e[0]), int(e[1]), float(e[2])
        if w >= wmin:
            adj.setdefault(u, []).append(v)
            adj.setdefault(v, []).append(u)
    return adj


def build_node_adj_topk(
    edges: Sequence[Sequence],
    k: int,
    disconnected_policy: str = "threshold"
) -> Dict[int, List[int]]:
    """
    Build adjacency using top-k strongest edges per node.
    
    Args:
        edges: List of [u, v, w, ...]
        k: Number of strongest edges to keep per node
        disconnected_policy: "threshold" or "maxdist"
        
    Returns:
        Adjacency dict {node: [neighbors]}
    """
    # Group edges by node
    node_edges = {}
    for e in edges:
        u, v, w = int(e[0]), int(e[1]), float(e[2])
        node_edges.setdefault(u, []).append((w, v))
        node_edges.setdefault(v, []).append((w, u))
    
    # Keep top-k per node
    adj = {}
    for node, edge_list in node_edges.items():
        edge_list.sort(reverse=True, key=lambda x: x[0])
        top_k = edge_list[:k]
        adj[node] = [neighbor for (w, neighbor) in top_k]
    
    return adj


def find_components(n: int, adj: Dict[int, List[int]]) -> List[List[int]]:
    """
    Find connected components via BFS.
    
    Args:
        n: Number of nodes
        adj: Adjacency dict
        
    Returns:
        List of components, each component is list of node IDs
    """
    visited = [False] * n
    components = []
    
    for start in range(n):
        if visited[start]:
            continue
        
        component = []
        queue = deque([start])
        visited[start] = True
        
        while queue:
            u = queue.popleft()
            component.append(u)
            
            for v in adj.get(u, []):
                if not visited[v]:
                    visited[v] = True
                    queue.append(v)
        
        components.append(component)
    
    return components


def assign_clusters(comps: List[List[int]], n_nodes: int) -> List[int]:
    """
    Assign cluster IDs to nodes.
    
    Args:
        comps: List of components (may be filtered, e.g. by min_cluster_size)
        n_nodes: Total number of nodes in the graph (ensures correct array length)
        
    Returns:
        Array where node2c[i] = cluster ID of node i, or -1 if unassigned
        
    Note:
        Always returns array of length n_nodes, regardless of which nodes
        appear in comps. This prevents IndexError when comps is filtered
        and doesn't contain all node IDs.
    """
    node2c = [-1] * n_nodes
    
    for cluster_id, comp in enumerate(comps):
        for node in comp:
            if 0 <= node < n_nodes:
                node2c[node] = cluster_id
    
    return node2c
