"""
ROMION Boundary Stabilization (minimal)

This module defines a minimal boundary-level stabilization step.
It converts CORE relational structure into a minimal FRACTURE snapshot.

Rules:
- This is boundary logic, not CORE.
- No analysis, no plotting, no domain interpretation.
- No metric geometry here (no distances, no clustering).
- Output must be JSON-serializable for logging.

Applies to ontology: THEORY_V3.9
Documentation status: v1-prerelease
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple

from ..core.graph import CoreGraph


@dataclass(frozen=True)
class StabilizationParams:
    """
    Minimal stabilization parameters.

    Interpretation:
    - w_visible: threshold for what becomes visible in FRACTURE (RI)
    - w_cluster: threshold for object-supporting edges (RI)
    - w_dist: threshold for background-supporting edges (RI)
    - w_bridge: threshold for bridge / interaction-supporting edges (RI)
    """
    w_visible: float = 0.0
    w_cluster: Optional[float] = None
    w_dist: Optional[float] = None
    w_bridge: Optional[float] = None


@dataclass(frozen=True)
class FractureSnapshot:
    """
    Minimal FRACTURE snapshot derived from CORE.

    This is not a full FRACTURE model.
    It is the minimal observable representation for MVP logging and validation.

    Fields are RI unless explicitly documented otherwise.
    """
    visible_edges: int
    visible_weight: float
    visible_ratio: float
    cluster_edges: Optional[int] = None
    cluster_ratio: Optional[float] = None
    background_edges: Optional[int] = None
    background_ratio: Optional[float] = None
    bridge_edges: Optional[int] = None
    bridge_weight: Optional[float] = None
    bridge_ratio: Optional[float] = None
    projection_regime: Optional[str] = None
    projection_contaminated: Optional[bool] = None
    freeze_state: Optional[bool] = None
    freeze_reason: Optional[str] = None
    loop_count: Optional[int] = None
    max_loop_length: Optional[int] = None
    min_loop_length: Optional[int] = None
    mean_loop_length: Optional[float] = None
    loop_edge_coverage_ratio: Optional[float] = None
    loop_detection_regime: Optional[str] = None
    loop_signatures: Optional[List[str]] = None
    loop_identity_regime: Optional[str] = None
    loop_orientation: Optional[List[int]] = None
    loop_charge: Optional[List[int]] = None
    loop_excitation_index: Optional[List[int]] = None
    loop_niche_anchor: Optional[List[int]] = None
    exclusion_candidate_regime: Optional[str] = None
    units: str = "RI"


def _validate_optional_threshold(name: str, value: Optional[float]) -> Tuple[bool, str]:
    if value is None:
        return True, "ok"
    if not math.isfinite(float(value)):
        return False, f"{name} must be finite if provided"
    if float(value) < 0.0:
        return False, f"{name} must be >= 0 if provided"
    return True, "ok"


def validate_stabilization_params(p: StabilizationParams) -> Tuple[bool, str]:
    ok, reason = _validate_optional_threshold("w_visible", p.w_visible)
    if not ok:
        return False, reason
    ok, reason = _validate_optional_threshold("w_cluster", p.w_cluster)
    if not ok:
        return False, reason
    ok, reason = _validate_optional_threshold("w_dist", p.w_dist)
    if not ok:
        return False, reason
    ok, reason = _validate_optional_threshold("w_bridge", p.w_bridge)
    if not ok:
        return False, reason

    provided = [p.w_cluster is not None, p.w_dist is not None, p.w_bridge is not None]
    if any(provided) and not all(provided):
        return False, "w_cluster, w_dist, and w_bridge must be provided together"

    if p.w_cluster is not None and p.w_dist is not None and float(p.w_cluster) < float(p.w_dist):
        return False, "w_cluster must be >= w_dist"

    return True, "ok"


def projection_regime(p: StabilizationParams) -> str:
    if p.w_cluster is None and p.w_dist is None and p.w_bridge is None:
        return "legacy_visible_only"
    if float(p.w_bridge) > float(p.w_dist):
        return "canonical_separated"
    return "diagnostic_contaminated"


def _safe_ratio(count: int, total_edges: int) -> float:
    return count / total_edges if total_edges > 0 else 0.0


def _compute_projection_layers(G: CoreGraph, p: StabilizationParams) -> Dict[str, Any]:
    regime = projection_regime(p)
    total_edges = G.n_edges
    cluster_edges = 0
    background_edges = 0
    bridge_edges = 0
    bridge_weight = 0.0

    for e in G.iter_edges():
        w = float(e.w)
        if w >= float(p.w_cluster):
            cluster_edges += 1
        if w >= float(p.w_bridge):
            bridge_edges += 1
            bridge_weight += w
        if w >= float(p.w_dist):
            if regime == "canonical_separated":
                if w < float(p.w_bridge):
                    background_edges += 1
            else:
                background_edges += 1

    return {
        "cluster_edges": int(cluster_edges),
        "cluster_ratio": float(_safe_ratio(cluster_edges, total_edges)),
        "background_edges": int(background_edges),
        "background_ratio": float(_safe_ratio(background_edges, total_edges)),
        "bridge_edges": int(bridge_edges),
        "bridge_weight": float(bridge_weight),
        "bridge_ratio": float(_safe_ratio(bridge_edges, total_edges)),
        "projection_regime": regime,
        "projection_contaminated": bool(regime == "diagnostic_contaminated"),
    }


def _canonicalize_cycle(cycle_nodes: List[int]) -> Tuple[int, ...]:
    """
    Canonicalize an undirected simple cycle under rotation and reversal.

    The input must not repeat the start node at the end.
    """
    if len(cycle_nodes) < 3:
        raise ValueError("cycle must contain at least 3 nodes")

    variants: List[Tuple[int, ...]] = []
    n = len(cycle_nodes)
    seqs = [tuple(cycle_nodes), tuple(reversed(cycle_nodes))]
    for seq in seqs:
        for i in range(n):
            variants.append(seq[i:] + seq[:i])
    return min(variants)


def _find_simple_cycles_in_cluster_graph(G: CoreGraph, p: StabilizationParams) -> Set[Tuple[int, ...]]:
    """
    Enumerate canonicalized simple cycles in the cluster-supporting subgraph.

    This is intentionally small-scope and suited to the current sparse MVP graphs.
    """
    adjacency: Dict[int, Set[int]] = {node: set() for node in range(G.n_nodes)}
    for e in G.iter_edges():
        if float(e.w) >= float(p.w_cluster):
            adjacency[e.u].add(e.v)
            adjacency[e.v].add(e.u)

    cycles: Set[Tuple[int, ...]] = set()

    def dfs(start: int, current: int, visited: Set[int], path: List[int]) -> None:
        for nxt in adjacency[current]:
            if nxt == start:
                if len(path) >= 3:
                    cycles.add(_canonicalize_cycle(path))
                continue
            if nxt in visited:
                continue
            if nxt < start:
                continue
            visited.add(nxt)
            path.append(nxt)
            dfs(start, nxt, visited, path)
            path.pop()
            visited.remove(nxt)

    for start in range(G.n_nodes):
        if len(adjacency[start]) < 2:
            continue
        visited = {start}
        dfs(start, start, visited, [start])

    return cycles


def _orientation_from_canonical_cycle(cycle: Tuple[int, ...]) -> int:
    """
    Derive a deterministic provisional orientation from canonical cycle order.

    This is an operational convention for exclusion-readiness instrumentation,
    not yet a final ontological orientation law.
    """
    if len(cycle) < 3:
        raise ValueError("cycle must contain at least 3 nodes")
    return 1 if cycle[1] < cycle[-1] else -1


def _charge_from_cycle(cycle: Tuple[int, ...], orientation: int) -> int:
    """
    Compute provisional topological charge from current canonical theory.
    """
    return int(orientation * (len(cycle) % 2))


def _compute_loop_summary(G: CoreGraph, p: StabilizationParams, layer_summary: Dict[str, Any]) -> Dict[str, Any]:
    regime = str(layer_summary["projection_regime"])
    if regime == "legacy_visible_only":
        return {}
    if regime == "diagnostic_contaminated":
        return {
            "loop_detection_regime": "not_applicable_contaminated",
            "loop_identity_regime": "not_applicable_contaminated",
            "exclusion_candidate_regime": "not_applicable_contaminated",
        }

    cycles = _find_simple_cycles_in_cluster_graph(G, p)
    if not cycles:
        return {
            "loop_count": 0,
            "max_loop_length": 0,
            "min_loop_length": 0,
            "mean_loop_length": 0.0,
            "loop_edge_coverage_ratio": 0.0,
            "loop_detection_regime": "canonical_cluster_graph",
            "loop_signatures": [],
            "loop_identity_regime": "canonical_exact_signature",
            "loop_orientation": [],
            "loop_charge": [],
            "loop_excitation_index": [],
            "loop_niche_anchor": [],
            "exclusion_candidate_regime": "canonical_identity_only",
        }

    sorted_cycles = sorted(cycles)
    lengths = [len(cycle) for cycle in sorted_cycles]
    signatures = ["-".join(str(node) for node in cycle) for cycle in sorted_cycles]
    orientations = [_orientation_from_canonical_cycle(cycle) for cycle in sorted_cycles]
    charges = [_charge_from_cycle(cycle, orientation) for cycle, orientation in zip(sorted_cycles, orientations)]
    excitation = [0 for _ in sorted_cycles]
    niche_anchors = [min(cycle) for cycle in sorted_cycles]
    cycle_edges: Set[Tuple[int, int]] = set()
    for cycle in sorted_cycles:
        nodes = list(cycle)
        for i in range(len(nodes)):
            u = nodes[i]
            v = nodes[(i + 1) % len(nodes)]
            edge = (u, v) if u < v else (v, u)
            cycle_edges.add(edge)

    cluster_edges = int(layer_summary["cluster_edges"])
    coverage = len(cycle_edges) / cluster_edges if cluster_edges > 0 else 0.0
    return {
        "loop_count": len(cycles),
        "max_loop_length": max(lengths),
        "min_loop_length": min(lengths),
        "mean_loop_length": sum(lengths) / float(len(lengths)),
        "loop_edge_coverage_ratio": float(coverage),
        "loop_detection_regime": "canonical_cluster_graph",
        "loop_signatures": signatures,
        "loop_identity_regime": "canonical_exact_signature",
        "loop_orientation": orientations,
        "loop_charge": charges,
        "loop_excitation_index": excitation,
        "loop_niche_anchor": niche_anchors,
        "exclusion_candidate_regime": "canonical_identity_only",
    }


def _compute_freeze_fields(layer_summary: Dict[str, Any]) -> Dict[str, Any]:
    """
    Freeze is a projection-level state derived from bridge observables.

    Stage 3B refines freeze using bridge_edges OR bridge_weight.
    """
    bridge_edges = int(layer_summary["bridge_edges"])
    bridge_weight = float(layer_summary["bridge_weight"])
    if bridge_edges == 0:
        return {
            "freeze_state": True,
            "freeze_reason": "no_bridges",
        }
    if bridge_weight == 0.0:
        return {
            "freeze_state": True,
            "freeze_reason": "zero_bridge_weight",
        }
    return {
        "freeze_state": False,
        "freeze_reason": "active",
    }


def stabilize_to_fracture(G: CoreGraph, p: StabilizationParams) -> FractureSnapshot:
    """
    Convert CORE graph into a minimal FRACTURE snapshot.

    The legacy visibility rule remains:
    - an edge is visible if its weight >= w_visible

    Optional projection thresholds add a richer projection summary:
    - cluster edges use w_cluster
    - background edges use w_dist and w_bridge
    - bridge edges use w_bridge

    Returns:
    - FractureSnapshot (serializable via fracture_snapshot_to_dict)
    """
    ok, reason = validate_stabilization_params(p)
    if not ok:
        raise ValueError(f"invalid stabilization params: {reason}")

    total_edges = G.n_edges
    if total_edges == 0:
        layer_summary: Dict[str, Any] = {}
        if projection_regime(p) != "legacy_visible_only":
            layer_summary = _compute_projection_layers(G, p)
            layer_summary.update(_compute_freeze_fields(layer_summary))
            layer_summary.update(_compute_loop_summary(G, p, layer_summary))
        return FractureSnapshot(
            visible_edges=0,
            visible_weight=0.0,
            visible_ratio=0.0,
            **layer_summary,
        )

    vis_cnt = 0
    vis_w = 0.0
    for e in G.iter_edges():
        if e.w >= p.w_visible:
            vis_cnt += 1
            vis_w += float(e.w)

    vis_ratio = _safe_ratio(vis_cnt, total_edges)
    layer_summary = {}
    if projection_regime(p) != "legacy_visible_only":
        layer_summary = _compute_projection_layers(G, p)
        layer_summary.update(_compute_freeze_fields(layer_summary))
        layer_summary.update(_compute_loop_summary(G, p, layer_summary))

    return FractureSnapshot(
        visible_edges=int(vis_cnt),
        visible_weight=float(vis_w),
        visible_ratio=float(vis_ratio),
        **layer_summary,
    )


def fracture_snapshot_to_dict(s: FractureSnapshot) -> Dict[str, Any]:
    """
    Convert FractureSnapshot to JSON-serializable dict for logging.
    """
    out: Dict[str, Any] = {
        "visible_edges": s.visible_edges,
        "visible_weight": s.visible_weight,
        "visible_ratio": s.visible_ratio,
        "units": s.units,
    }
    optional_fields = {
        "cluster_edges": s.cluster_edges,
        "cluster_ratio": s.cluster_ratio,
        "background_edges": s.background_edges,
        "background_ratio": s.background_ratio,
        "bridge_edges": s.bridge_edges,
        "bridge_weight": s.bridge_weight,
        "bridge_ratio": s.bridge_ratio,
        "projection_regime": s.projection_regime,
        "projection_contaminated": s.projection_contaminated,
        "freeze_state": s.freeze_state,
        "freeze_reason": s.freeze_reason,
        "loop_count": s.loop_count,
        "max_loop_length": s.max_loop_length,
        "min_loop_length": s.min_loop_length,
        "mean_loop_length": s.mean_loop_length,
        "loop_edge_coverage_ratio": s.loop_edge_coverage_ratio,
        "loop_detection_regime": s.loop_detection_regime,
        "loop_signatures": s.loop_signatures,
        "loop_identity_regime": s.loop_identity_regime,
        "loop_orientation": s.loop_orientation,
        "loop_charge": s.loop_charge,
        "loop_excitation_index": s.loop_excitation_index,
        "loop_niche_anchor": s.loop_niche_anchor,
        "exclusion_candidate_regime": s.exclusion_candidate_regime,
    }
    for key, value in optional_fields.items():
        if value is not None:
            out[key] = value
    return out
