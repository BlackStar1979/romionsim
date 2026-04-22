"""
ROMION Simulation Engine API (public interface)

This module defines the public interface for the romionsim engine.
Experiments must import ONLY from this API layer.

This file now contains a minimal runnable implementation of run().
It is still MVP-level and intentionally simple.

Applies to ontology: THEORY_V3.9
Documentation status: v1-prerelease
"""

from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from .log_contract import (
    make_end_event,
    make_metadata_event,
    make_params_event,
    make_tick_event,
)
from ..core.params import normalize_core_params
from ..core.rng import CoreRng
from ..core.evolution import EvolutionParams, StabilizationParams, init_core_graph, step


@dataclass(frozen=True)
class EngineParams:
    """
    Parameter container for the engine.

    Rules:
    - All parameters must be explicit (no hidden constants).
    - Values are treated as RI (Relational Internal) unless documented otherwise.
    - This object must be serializable to a dict for logging.
    """
    seed: int = 0
    n_nodes: int = 0
    ticks: int = 0

    spawn_scale: float = 1.0
    decay_scale: float = 1.0

    w_max: Optional[float] = None

    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        out = {
            "seed": self.seed,
            "n_nodes": self.n_nodes,
            "ticks": self.ticks,
            "spawn_scale": self.spawn_scale,
            "decay_scale": self.decay_scale,
            "w_max": self.w_max,
        }
        if self.extra:
            out["extra"] = dict(self.extra)
        return out


@dataclass
class RunArtifacts:
    """
    Output container returned after a run.
    """
    params: Dict[str, Any]
    run_id: str
    log_path: Optional[str] = None
    summary: Dict[str, Any] = field(default_factory=dict)


def _write_jsonl_line(f, obj: Dict[str, Any]) -> None:
    f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def _build_evolution_params(core_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build explicit evolution and stabilization params from core params dict.

    We read from params["extra"] if present.
    Compatibility fallbacks are still permitted for MVP,
    but they are not canonical recommended baselines.
    We always write the final used values into the PARAMS event
    so that any fallback usage remains auditable.
    """
    extra = core_params.get("extra") or {}

    # These fallback values exist only so that wrapper-level tolerance can fail
    # inside the engine with a fully logged used-params block. Completed
    # experiments should still register their own explicit values in params.json.
    evo = EvolutionParams(
        w_init_min=float(extra.get("w_init_min", 0.01)),
        w_init_max=float(extra.get("w_init_max", 0.05)),
        p_add=float(extra.get("p_add", 0.02)),
        p_decay=float(extra.get("p_decay", 0.99)),
        w_prune=float(extra.get("w_prune", 0.0)),
    )

    # Same rule for stabilization: fallback support is an implementation detail,
    # not a recommended experiment baseline.
    stab = StabilizationParams(
        w_visible=float(extra.get("w_visible", 0.0)),
        w_cluster=float(extra["w_cluster"]) if extra.get("w_cluster") is not None else None,
        w_dist=float(extra["w_dist"]) if extra.get("w_dist") is not None else None,
        w_bridge=float(extra["w_bridge"]) if extra.get("w_bridge") is not None else None,
    )

    return {
        "evolution": {
            "w_init_min": evo.w_init_min,
            "w_init_max": evo.w_init_max,
            "p_add": evo.p_add,
            "p_decay": evo.p_decay,
            "w_prune": evo.w_prune,
            "units": "RI",
        },
        "stabilization": {
            "w_visible": stab.w_visible,
            "w_cluster": stab.w_cluster,
            "w_dist": stab.w_dist,
            "w_bridge": stab.w_bridge,
            "units": "RI",
        },
    }


class RomionEngine:
    """
    Public engine facade.
    """

    def __init__(self, params: EngineParams):
        self.params = params

    def run(self, out_dir: str) -> RunArtifacts:
        """
        Run the simulation and write schema-versioned logs to out_dir.

        Returns RunArtifacts with log_path and summary.
        """
        raw_params = self.params.to_dict()

        # Fail-closed normalization of CORE params
        core_params = normalize_core_params(raw_params). __dict__

        # Enrich with explicit evolution/stabilization params (also logged)
        used = _build_evolution_params(core_params)
        core_params["used"] = used

        run_id = str(uuid.uuid4())
        os.makedirs(out_dir, exist_ok=True)
        log_path = os.path.join(out_dir, f"simulation_{run_id}.jsonl")

        ok = True
        reason = None
        summary: Dict[str, Any] = {}

        try:
            with open(log_path, "w", encoding="utf-8") as f:
                _write_jsonl_line(f, make_metadata_event())
                _write_jsonl_line(f, make_params_event(core_params))

                rng = CoreRng(seed=int(core_params["seed"]))

                evo_cfg = used["evolution"]
                evo = EvolutionParams(
                    w_init_min=float(evo_cfg["w_init_min"]),
                    w_init_max=float(evo_cfg["w_init_max"]),
                    p_add=float(evo_cfg["p_add"]),
                    p_decay=float(evo_cfg["p_decay"]),
                    w_prune=float(evo_cfg["w_prune"]),
                )

                stab_cfg = used["stabilization"]
                stab = StabilizationParams(
                    w_visible=float(stab_cfg["w_visible"]),
                    w_cluster=float(stab_cfg["w_cluster"]) if stab_cfg.get("w_cluster") is not None else None,
                    w_dist=float(stab_cfg["w_dist"]) if stab_cfg.get("w_dist") is not None else None,
                    w_bridge=float(stab_cfg["w_bridge"]) if stab_cfg.get("w_bridge") is not None else None,
                )

                G = init_core_graph(n_nodes=int(core_params["n_nodes"]), rng=rng, p=evo)

                last_fracture = None
                for t in range(int(core_params["ticks"])):
                    core_log, fracture_state = step(
                        tick=t,
                        G=G,
                        rng=rng,
                        evo=evo,
                        stab=stab,
                    )
                    last_fracture = fracture_state
                    _write_jsonl_line(
                        f,
                        make_tick_event(
                            tick=t,
                            core=core_log,
                            fracture=fracture_state.to_dict(),
                        ),
                    )

                # Minimal summary
                if last_fracture is not None:
                    summary = {
                        "ticks": int(core_params["ticks"]),
                        "final_visible_edges": int(last_fracture.visible_edges),
                        "final_visible_ratio": float(last_fracture.visible_ratio),
                        "units": "RI",
                    }
                _write_jsonl_line(f, make_end_event(run_id=run_id, ok=True, summary=summary))

        except Exception as e:
            ok = False
            reason = str(e)
            # Best-effort END event append if possible
            try:
                with open(log_path, "a", encoding="utf-8") as f:
                    _write_jsonl_line(f, make_end_event(run_id=run_id, ok=False, reason=reason))
            except Exception:
                pass
            raise

        artifacts = RunArtifacts(
            params=core_params,
            run_id=run_id,
            log_path=log_path,
            summary=summary,
        )
        return artifacts

    def tick(self) -> Dict[str, Any]:
        """
        Tick-level execution is not implemented in MVP.
        Use run() for now.
        """
        raise NotImplementedError("Use run(out_dir) in MVP.")
