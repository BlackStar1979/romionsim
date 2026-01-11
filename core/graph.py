# romionsim/core/graph.py
"""
Hypergraph structure for ROMION CORE layer.

Implements H_n = (V_n, E_n, w_n, σ_n) where:
- V_n: nodes (romions)
- E_n: edges (relations)  
- w_n: weights (relational strength)
- σ_n: types (future: different interaction types)
"""

import random
from dataclasses import dataclass
from typing import Dict, Tuple, ValuesView


@dataclass
class Edge:
    """
    Relation (Mediating Romion) in CORE layer.
    
    Attributes:
        u: First node index (always smaller in key normalization)
        v: Second node index (always larger in key normalization)
        w: Weight (relational energy/strength)
        sigma: Relation type (reserved for future: different interaction types)
        age: Relation age in simulation ticks
        kappa_cache: Cached coherence value κ(e) ∈ [0,1]
    """
    u: int
    v: int
    w: float
    sigma: int = 0
    age: int = 0
    kappa_cache: float = 0.0


class Graph:
    """
    Undirected hypergraph with unique edges.
    
    In MVP: simplified to undirected graph.
    Future: full hypergraph support (n-ary relations).
    
    Key invariants:
    - Each relation exists exactly once (u,v) ≡ (v,u)
    - Edges indexed by normalized tuple (min, max)
    - Fast adjacency lookup via dual indexing
    """
    
    def __init__(self, num_nodes: int):
        self.num_nodes = num_nodes
        # Fast neighbor access: adj[u][v] -> Edge object
        self.adj: Dict[int, Dict[int, Edge]] = {i: {} for i in range(num_nodes)}
        # Unique edge list: key (min, max) -> Edge object
        self.edges: Dict[Tuple[int, int], Edge] = {}

    def add_edge(self, u: int, v: int, w: float, limit: float = None) -> bool:
        """
        Add or update relation.
        
        ONTOLOGICAL PRINCIPLE: Relation is unique. If adding new relation
        with same endpoints, collapse to stronger value (max).
        
        Args:
            u: First node
            v: Second node
            w: Weight
            limit: Hard weight limit (safety cap)
            
        Returns:
            True if new relation created, False if existing updated
        """
        if u == v:
            return False
        
        # Normalize indices for uniqueness (undirected graph)
        low, high = (u, v) if u < v else (v, u)
        key = (low, high)
        
        # Apply limit (safety cap)
        val = w
        if limit is not None:
            val = min(val, limit)

        if key in self.edges:
            # MERGE: Keep stronger memory trace
            e = self.edges[key]
            if val > e.w:
                e.w = val
            return False  # Merge (existed)
        else:
            # CREATE: New relation
            e = Edge(low, high, val)
            self.edges[key] = e
            self.adj[low][high] = e
            self.adj[high][low] = e
            return True  # New (created)

    def get_edge(self, u: int, v: int) -> Edge | None:
        """Return edge object or None."""
        return self.adj[u].get(v)

    def all_edges(self) -> ValuesView[Edge]:
        """Return view of all unique edges."""
        return self.edges.values()
