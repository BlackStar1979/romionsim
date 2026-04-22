"""
ROMION CORE Evolution (minimal)

This module defines a minimal evolution step that ties together:
- CORE graph state
- CORE stats for logging
- boundary stabilization
- FRACTURE state construction

This is still MVP-level logic.
It is intentionally simple and does not implement full theoretical rules yet.

Rules:
- CORE evolution must not import analysis or validation layers.
- Boundary and FRACTURE may be invoked, but must remain minimal and serializable.

Applies to ontology: THEORY_V3.9
Documentation status: v1-prerelease
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Tuple

from .graph import CoreGraph
from .rng import CoreRng
from .core_metrics import compute_core_stats, core_stats_to_dict, compute_pressure_map, compute_mean_pressure
from ..boundary.stabilization import StabilizationParams, stabilize_to_fracture, fracture_snapshot_to_dict
from ..fracture.state import from_snapshot, FractureState


@dataclass(frozen=True)
class EvolutionParams:
    """
    Minimal evolution parameters for MVP.

    Interpretation:
    - w_init_min, w_init_max: initial edge weight range (RI)
    - p_add: probability to add a new edge on a tick (RI probability)
    - p_decay: multiplicative decay factor applied to all edges each tick
    - w_prune: prune edges below this weight after decay

    These are MVP knobs and must be explicit in params.extra.
    The dataclass defaults below are compatibility support only.
    They must not be read as canonical or preferred experiment settings.
    """
    w_init_min: float = 0.01
    w_init_max: float = 0.05
    p_add: float = 0.02
    p_decay: float = 0.99
    w_prune: float = 0.0


def _validate_evolution_params(p: EvolutionParams) -> Tuple[bool, str]:
    if p.w_init_min < 0.0 or p.w_init_max < 0.0:
        return False, "w_init_min and w_init_max must be >= 0"
    if p.w_init_max < p.w_init_min:
        return False, "w_init_max must be >= w_init_min"
    if p.p_add < 0.0 or p.p_add > 1.0:
        return False, "p_add must be in [0, 1]"
    if p.p_decay < 0.0 or p.p_decay > 1.0:
        return False, "p_decay must be in [0, 1]"
    if p.w_prune < 0.0:
        return False, "w_prune must be >= 0"
    return True, "ok"


def init_core_graph(n_nodes: int, rng: CoreRng, p: EvolutionParams) -> CoreGraph:
    """
    Initialize CORE graph with a sparse random set of edges.

    This is an MVP initializer.
    """
    ok, reason = _validate_evolution_params(p)
    if not ok:
        raise ValueError(f"invalid evolution params: {reason}")

    G = CoreGraph(n_nodes=n_nodes)

    # Create a minimal connected backbone by linking i -> i+1 with random weights
    for i in range(n_nodes - 1):
        w = rng.rand_weight(p.w_init_min, p.w_init_max)
        G.add_or_update_edge(i, i + 1, w=w)

    return G


def _decay_all_edges(G: CoreGraph, decay_factor: float) -> None:
    """
    Apply multiplicative decay to all edges.
    """
    for e in list(G.iter_edges()):
        new_w = float(e.w) * float(decay_factor)
        G.add_or_update_edge(e.u, e.v, w=new_w, kappa=e.kappa, meta=e.meta)


def _maybe_add_edge(G: CoreGraph, rng: CoreRng, p: EvolutionParams) -> bool:
    """
    With probability p_add, add one random edge between two distinct nodes.
    Returns True if an edge was added.
    """
    if not rng.maybe(p.p_add):
        return False

    u = rng.rand_int(0, G.n_nodes - 1)
    v = rng.rand_int(0, G.n_nodes - 1)
    while v == u:
        v = rng.rand_int(0, G.n_nodes - 1)

    w = rng.rand_weight(p.w_init_min, p.w_init_max)
    G.add_or_update_edge(u, v, w=w)
    return True


def step(
    tick: int,
    G: CoreGraph,
    rng: CoreRng,
    evo: EvolutionParams,
    stab: StabilizationParams,
) -> Tuple[Dict[str, Any], FractureState]:
    """
    Execute one MVP tick.

    Returns:
    - core_log: dict suitable for 'core' field in log_contract.make_tick_event
    - fracture_state: FractureState suitable for 'fracture' field
    """
    ok, reason = _validate_evolution_params(evo)
    if not ok:
        raise ValueError(f"invalid evolution params: {reason}")

    # 1) CORE update (MVP)
    added = _maybe_add_edge(G, rng, evo)
    _decay_all_edges(G, evo.p_decay)
    pruned = G.prune_below(evo.w_prune)

    # 2) CORE stats for logging
    stats = compute_core_stats(G, w_threshold=0.0)
    pressure = compute_pressure_map(G)
    mean_pressure = compute_mean_pressure(pressure)

    core_log: Dict[str, Any] = core_stats_to_dict(stats)
    core_log["mean_pressure"] = float(mean_pressure)
    core_log["edges_added"] = int(1 if added else 0)
    core_log["edges_pruned"] = int(pruned)

    # 3) Boundary stabilization -> FRACTURE snapshot
    snap = stabilize_to_fracture(G, stab)
    snap_dict = fracture_snapshot_to_dict(snap)

    # 4) FRACTURE state
    fracture_state = from_snapshot(tick=tick, snap=snap_dict)

    return core_log, fracture_state
