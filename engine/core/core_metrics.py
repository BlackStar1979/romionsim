"""
ROMION CORE Metrics (minimal structural statistics)

This module computes minimal CORE-layer metrics suitable for logging.

Rules:
- CORE metrics must not depend on FRACTURE, boundary, analysis, or validation layers.
- No metric geometry here. No clustering here.
- Values are RI (Relational Internal) unless explicitly documented otherwise.
- All outputs must be JSON-serializable.

Applies to ontology: THEORY_V3.9
Documentation status: v1-prerelease
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional

from .graph import CoreGraph


@dataclass(frozen=True)
class CoreStats:
    """
    Minimal CORE structural stats.

    All values are RI.
    """
    n_nodes: int
    n_edges: int
    total_weight: float
    mean_weight: float
    mean_degree: float
    max_degree: int


def compute_core_stats(G: CoreGraph, w_threshold: float = 0.0) -> CoreStats:
    """
    Compute minimal CORE stats.

    Parameters:
    - w_threshold: threshold used for degree counting (RI)
      This does not prune edges; it only affects degree reporting.

    Fail-closed:
    - raises ValueError for invalid threshold
    """
    if w_threshold < 0.0:
        raise ValueError("w_threshold must be >= 0")

    n_nodes = G.n_nodes
    n_edges = G.n_edges
    total_w = float(G.total_weight())
    mean_w = total_w / n_edges if n_edges > 0 else 0.0

    # Degree stats
    degrees = [G.degree(u, w_threshold=w_threshold) for u in range(n_nodes)]
    max_deg = max(degrees) if degrees else 0
    mean_deg = sum(degrees) / len(degrees) if degrees else 0.0

    return CoreStats(
        n_nodes=int(n_nodes),
        n_edges=int(n_edges),
        total_weight=total_w,
        mean_weight=float(mean_w),
        mean_degree=float(mean_deg),
        max_degree=int(max_deg),
    )


def core_stats_to_dict(stats: CoreStats) -> Dict[str, Any]:
    """
    Convert CoreStats to a JSON-serializable dict for logging.
    """
    return {
        "n_nodes": stats.n_nodes,
        "n_edges": stats.n_edges,
        "total_weight": stats.total_weight,
        "mean_weight": stats.mean_weight,
        "mean_degree": stats.mean_degree,
        "max_degree": stats.max_degree,
        "units": "RI",
    }


def compute_pressure_map(G: CoreGraph) -> Dict[int, float]:
    """
    Compute a simple pressure proxy per node.

    Definition (RI):
    pressure[u] = sum of weights of incident edges on u

    This is a structural proxy used for diagnostics and normalization.
    """
    pressure: Dict[int, float] = {u: 0.0 for u in range(G.n_nodes)}
    for e in G.iter_edges():
        pressure[e.u] += float(e.w)
        pressure[e.v] += float(e.w)
    return pressure


def compute_mean_pressure(pressure: Dict[int, float]) -> float:
    """
    Compute mean pressure across nodes (RI).
    """
    if not pressure:
        return 0.0
    return sum(pressure.values()) / len(pressure)
