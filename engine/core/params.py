"""
ROMION CORE Params (sanity validation)

This module provides CORE-level parameter validation.
It does not define ontology and does not perform logging.
It enforces:
- explicit parameters
- fail-closed checks
- no hidden defaults with ontological meaning

Rules:
- CORE must not import from boundary, fracture, analysis, or validation layers.
- All checks must be deterministic and side-effect free.

Applies to ontology: THEORY_V3.9
Documentation status: v1-prerelease
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple


@dataclass(frozen=True)
class CoreParams:
    """
    Minimal CORE parameters.

    These are engine-internal sanitized parameters derived from API params.
    Values are treated as RI unless explicitly documented otherwise.
    """
    seed: int
    n_nodes: int
    ticks: int
    spawn_scale: float
    decay_scale: float
    w_max: Optional[float]
    extra: Dict[str, Any]


def _is_finite_number(x: Any) -> bool:
    try:
        v = float(x)
    except Exception:
        return False
    return v == v and v not in (float("inf"), float("-inf"))


def validate_core_params(params: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate raw params dict (usually EngineParams.to_dict()).

    Returns:
    - (ok, reason)
      ok True means params are acceptable for CORE execution.
      ok False means fail-closed: do not run.

    This is a minimal validator. It does not validate domain-specific hypotheses.
    """
    required = ["seed", "n_nodes", "ticks", "spawn_scale", "decay_scale"]
    for k in required:
        if k not in params:
            return False, f"missing required param: {k}"

    # seed
    try:
        int(params["seed"])
    except Exception:
        return False, "seed must be an int"

    # n_nodes
    try:
        n = int(params["n_nodes"])
    except Exception:
        return False, "n_nodes must be an int"
    if n <= 0:
        return False, "n_nodes must be > 0"

    # ticks
    try:
        t = int(params["ticks"])
    except Exception:
        return False, "ticks must be an int"
    if t <= 0:
        return False, "ticks must be > 0"

    # scales
    for name in ["spawn_scale", "decay_scale"]:
        if not _is_finite_number(params[name]):
            return False, f"{name} must be a finite number"
        if float(params[name]) <= 0.0:
            return False, f"{name} must be > 0"

    # optional clamp
    if "w_max" in params and params["w_max"] is not None:
        if not _is_finite_number(params["w_max"]):
            return False, "w_max must be a finite number if provided"
        if float(params["w_max"]) <= 0.0:
            return False, "w_max must be > 0 if provided"

    # extra must be dict if present
    if "extra" in params and params["extra"] is not None:
        if not isinstance(params["extra"], dict):
            return False, "extra must be a dict if provided"

    return True, "ok"


def normalize_core_params(params: Dict[str, Any]) -> CoreParams:
    """
    Convert raw params dict into CoreParams (sanitized).

    Fail-closed:
    - raises ValueError if validate_core_params fails
    """
    ok, reason = validate_core_params(params)
    if not ok:
        raise ValueError(f"invalid params: {reason}")

    extra = params.get("extra") or {}
    # enforce copy to avoid accidental mutation
    extra = dict(extra)

    return CoreParams(
        seed=int(params["seed"]),
        n_nodes=int(params["n_nodes"]),
        ticks=int(params["ticks"]),
        spawn_scale=float(params["spawn_scale"]),
        decay_scale=float(params["decay_scale"]),
        w_max=float(params["w_max"]) if params.get("w_max") is not None else None,
        extra=extra,
    )