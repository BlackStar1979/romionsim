"""
ROMION CORE Graph (relational structure)

Minimal in-memory representation of the CORE relational graph.

Rules:
- CORE must not contain metric geometry concepts.
- CORE must not import from boundary, fracture, analysis, or validation layers.
- Data must be serializable or convertible to serializable forms for logging.

Applies to ontology: THEORY_V3.9
Documentation status: v1-prerelease
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterator, List, Optional, Tuple


NodeId = int
EdgeKey = Tuple[NodeId, NodeId]


def _norm_pair(u: NodeId, v: NodeId) -> EdgeKey:
    if u == v:
        raise ValueError("Self-edges are not allowed in CORE graph.")
    return (u, v) if u < v else (v, u)


@dataclass
class Edge:
    """
    Undirected relation between two nodes.

    Fields:
    - u, v: endpoint node ids
    - w: relation weight (RI)
    - kappa: coherence placeholder (RI), optional
    - meta: optional small dict for internal tags (must remain serializable)
    """
    u: NodeId
    v: NodeId
    w: float
    kappa: Optional[float] = None
    meta: Optional[Dict[str, object]] = None

    def key(self) -> EdgeKey:
        return _norm_pair(self.u, self.v)


class CoreGraph:
    """
    Minimal undirected weighted graph with unique edges.
    """

    def __init__(self, n_nodes: int):
        if n_nodes <= 0:
            raise ValueError("n_nodes must be > 0")
        self._n: int = int(n_nodes)
        self._edges: Dict[EdgeKey, Edge] = {}
        self._adj: List[Dict[NodeId, float]] = [dict() for _ in range(self._n)]

    @property
    def n_nodes(self) -> int:
        return self._n

    @property
    def n_edges(self) -> int:
        return len(self._edges)

    def has_edge(self, u: NodeId, v: NodeId) -> bool:
        return _norm_pair(u, v) in self._edges

    def get_edge(self, u: NodeId, v: NodeId) -> Optional[Edge]:
        return self._edges.get(_norm_pair(u, v))

    def iter_edges(self) -> Iterator[Edge]:
        return iter(self._edges.values())

    def iter_edge_keys(self) -> Iterator[EdgeKey]:
        return iter(self._edges.keys())

    def neighbors(self, u: NodeId) -> Dict[NodeId, float]:
        if u < 0 or u >= self._n:
            raise IndexError("node id out of range")
        return self._adj[u]

    def add_or_update_edge(
        self,
        u: NodeId,
        v: NodeId,
        w: float,
        kappa: Optional[float] = None,
        meta: Optional[Dict[str, object]] = None,
    ) -> None:
        if w < 0:
            raise ValueError("Edge weight must be >= 0")
        if u < 0 or u >= self._n or v < 0 or v >= self._n:
            raise IndexError("node id out of range")

        key = _norm_pair(u, v)

        if key in self._edges:
            e = self._edges[key]
            e.w = float(w)
            e.kappa = kappa
            e.meta = meta
        else:
            e = Edge(u=key[0], v=key[1], w=float(w), kappa=kappa, meta=meta)
            self._edges[key] = e

        self._adj[key[0]][key[1]] = float(w)
        self._adj[key[1]][key[0]] = float(w)

    def remove_edge(self, u: NodeId, v: NodeId) -> bool:
        key = _norm_pair(u, v)
        e = self._edges.pop(key, None)
        if e is None:
            return False
        self._adj[key[0]].pop(key[1], None)
        self._adj[key[1]].pop(key[0], None)
        return True

    def prune_below(self, w_min: float) -> int:
        if w_min < 0:
            raise ValueError("w_min must be >= 0")
        to_remove: List[EdgeKey] = [k for k, e in self._edges.items() if e.w < w_min]
        for u, v in to_remove:
            self.remove_edge(u, v)
        return len(to_remove)

    def as_edge_list(self) -> List[Tuple[int, int, float]]:
        out: List[Tuple[int, int, float]] = []
        for e in self._edges.values():
            out.append((int(e.u), int(e.v), float(e.w)))
        return out

    def degree(self, u: NodeId, w_threshold: float = 0.0) -> int:
        if u < 0 or u >= self._n:
            raise IndexError("node id out of range")
        if w_threshold < 0:
            raise ValueError("w_threshold must be >= 0")
        return sum(1 for _, w in self._adj[u].items() if w >= w_threshold)

    def total_weight(self) -> float:
        return sum(e.w for e in self._edges.values())