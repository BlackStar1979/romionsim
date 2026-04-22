"""
ROMION FRACTURE State (minimal)

This module defines the minimal FRACTURE-level state representation.

Rules:
- FRACTURE is derived from CORE via boundary stabilization.
- This module stores only observable, serializable values.
- No analysis, no plotting, no domain interpretation.
- Units are RI unless explicitly documented otherwise.

Applies to ontology: THEORY_V3.9
Documentation status: v1-prerelease
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class FractureState:
    """
    Minimal observable state.

    This is intentionally small for MVP.
    It is suitable for:
    - logging in TICK events under the 'fracture' field
    - basic validation and downstream analysis

    Fields:
    - tick: current tick number
    - visible_edges: count of visible edges (RI)
    - visible_weight: sum of weights of visible edges (RI)
    - visible_ratio: fraction of visible edges among all CORE edges (RI)
    - meta: optional small dict for additional serializable facts
    - units: unit system label (RI by default)
    """
    tick: int
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
    loop_signatures: Optional[list[str]] = None
    loop_identity_regime: Optional[str] = None
    loop_orientation: Optional[list[int]] = None
    loop_charge: Optional[list[int]] = None
    loop_excitation_index: Optional[list[int]] = None
    loop_niche_anchor: Optional[list[int]] = None
    exclusion_candidate_regime: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)
    units: str = "RI"

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "tick": int(self.tick),
            "visible_edges": int(self.visible_edges),
            "visible_weight": float(self.visible_weight),
            "visible_ratio": float(self.visible_ratio),
            "units": self.units,
        }
        optional_fields = {
            "cluster_edges": self.cluster_edges,
            "cluster_ratio": self.cluster_ratio,
            "background_edges": self.background_edges,
            "background_ratio": self.background_ratio,
            "bridge_edges": self.bridge_edges,
            "bridge_weight": self.bridge_weight,
            "bridge_ratio": self.bridge_ratio,
            "projection_regime": self.projection_regime,
            "projection_contaminated": self.projection_contaminated,
            "freeze_state": self.freeze_state,
            "freeze_reason": self.freeze_reason,
            "loop_count": self.loop_count,
            "max_loop_length": self.max_loop_length,
            "min_loop_length": self.min_loop_length,
            "mean_loop_length": self.mean_loop_length,
            "loop_edge_coverage_ratio": self.loop_edge_coverage_ratio,
            "loop_detection_regime": self.loop_detection_regime,
            "loop_signatures": self.loop_signatures,
            "loop_identity_regime": self.loop_identity_regime,
            "loop_orientation": self.loop_orientation,
            "loop_charge": self.loop_charge,
            "loop_excitation_index": self.loop_excitation_index,
            "loop_niche_anchor": self.loop_niche_anchor,
            "exclusion_candidate_regime": self.exclusion_candidate_regime,
        }
        for key, value in optional_fields.items():
            if value is not None:
                out[key] = value
        if self.meta:
            out["meta"] = dict(self.meta)
        return out


def from_snapshot(tick: int, snap: Dict[str, Any]) -> FractureState:
    """
    Construct FractureState from a snapshot dict.

    Expected keys:
    - visible_edges
    - visible_weight
    - visible_ratio

    This function is fail-closed: raises ValueError on missing or invalid data.
    """
    for k in ["visible_edges", "visible_weight", "visible_ratio"]:
        if k not in snap:
            raise ValueError(f"missing fracture snapshot field: {k}")

    ve = int(snap["visible_edges"])
    vw = float(snap["visible_weight"])
    vr = float(snap["visible_ratio"])

    if ve < 0:
        raise ValueError("visible_edges must be >= 0")
    if vw < 0.0:
        raise ValueError("visible_weight must be >= 0")
    if vr < 0.0 or vr > 1.0:
        raise ValueError("visible_ratio must be in [0, 1]")

    def optional_int(name: str) -> Optional[int]:
        if name not in snap or snap[name] is None:
            return None
        value = int(snap[name])
        if value < 0:
            raise ValueError(f"{name} must be >= 0")
        return value

    def optional_ratio(name: str) -> Optional[float]:
        if name not in snap or snap[name] is None:
            return None
        value = float(snap[name])
        if value < 0.0 or value > 1.0:
            raise ValueError(f"{name} must be in [0, 1]")
        return value

    cluster_edges = optional_int("cluster_edges")
    cluster_ratio = optional_ratio("cluster_ratio")
    background_edges = optional_int("background_edges")
    background_ratio = optional_ratio("background_ratio")
    bridge_edges = optional_int("bridge_edges")
    bridge_weight = snap.get("bridge_weight")
    bridge_ratio = optional_ratio("bridge_ratio")
    projection_regime = snap.get("projection_regime")
    projection_contaminated = snap.get("projection_contaminated")
    freeze_state = snap.get("freeze_state")
    freeze_reason = snap.get("freeze_reason")
    loop_count = snap.get("loop_count")
    max_loop_length = snap.get("max_loop_length")
    min_loop_length = snap.get("min_loop_length")
    mean_loop_length = snap.get("mean_loop_length")
    loop_edge_coverage_ratio = snap.get("loop_edge_coverage_ratio")
    loop_detection_regime = snap.get("loop_detection_regime")
    loop_signatures = snap.get("loop_signatures")
    loop_identity_regime = snap.get("loop_identity_regime")
    loop_orientation = snap.get("loop_orientation")
    loop_charge = snap.get("loop_charge")
    loop_excitation_index = snap.get("loop_excitation_index")
    loop_niche_anchor = snap.get("loop_niche_anchor")
    exclusion_candidate_regime = snap.get("exclusion_candidate_regime")

    if projection_regime is not None and not isinstance(projection_regime, str):
        raise ValueError("projection_regime must be a string if provided")
    if projection_contaminated is not None and not isinstance(projection_contaminated, bool):
        raise ValueError("projection_contaminated must be a bool if provided")
    if bridge_weight is not None:
        bridge_weight = float(bridge_weight)
        if bridge_weight < 0.0:
            raise ValueError("bridge_weight must be >= 0 if provided")
    if freeze_state is not None and not isinstance(freeze_state, bool):
        raise ValueError("freeze_state must be a bool if provided")
    if freeze_reason is not None and not isinstance(freeze_reason, str):
        raise ValueError("freeze_reason must be a string if provided")
    if loop_detection_regime is not None and not isinstance(loop_detection_regime, str):
        raise ValueError("loop_detection_regime must be a string if provided")
    if loop_identity_regime is not None and not isinstance(loop_identity_regime, str):
        raise ValueError("loop_identity_regime must be a string if provided")
    if exclusion_candidate_regime is not None and not isinstance(exclusion_candidate_regime, str):
        raise ValueError("exclusion_candidate_regime must be a string if provided")

    allowed_freeze_reasons = {"no_bridges", "zero_bridge_weight", "active", "not_applicable"}
    if freeze_reason is not None and freeze_reason not in allowed_freeze_reasons:
        raise ValueError("freeze_reason is not recognized")
    allowed_loop_regimes = {
        "canonical_cluster_graph",
        "not_applicable_legacy",
        "not_applicable_contaminated",
    }
    if loop_detection_regime is not None and loop_detection_regime not in allowed_loop_regimes:
        raise ValueError("loop_detection_regime is not recognized")
    allowed_loop_identity_regimes = {
        "canonical_exact_signature",
        "not_applicable_legacy",
        "not_applicable_contaminated",
    }
    if loop_identity_regime is not None and loop_identity_regime not in allowed_loop_identity_regimes:
        raise ValueError("loop_identity_regime is not recognized")
    allowed_exclusion_candidate_regimes = {
        "canonical_identity_only",
        "canonical_candidate_path",
        "not_applicable_legacy",
        "not_applicable_contaminated",
    }
    if (
        exclusion_candidate_regime is not None
        and exclusion_candidate_regime not in allowed_exclusion_candidate_regimes
    ):
        raise ValueError("exclusion_candidate_regime is not recognized")

    if freeze_state is not None or freeze_reason is not None:
        if projection_regime is None:
            raise ValueError("freeze fields require projection_regime")
        if bridge_edges is None:
            raise ValueError("freeze fields require bridge_edges")
        if bridge_weight is None:
            raise ValueError("freeze fields require bridge_weight")
        if freeze_state is None or freeze_reason is None:
            raise ValueError("freeze_state and freeze_reason must be provided together")
        if freeze_state:
            if freeze_reason not in {"no_bridges", "zero_bridge_weight"}:
                raise ValueError("frozen state requires a frozen freeze_reason")
        else:
            if freeze_reason not in {"active", "not_applicable"}:
                raise ValueError("active state requires a non-frozen freeze_reason")
        if freeze_reason == "no_bridges" and bridge_edges != 0:
            raise ValueError("freeze_reason=no_bridges requires bridge_edges == 0")
        if freeze_reason == "zero_bridge_weight":
            if bridge_edges <= 0:
                raise ValueError("freeze_reason=zero_bridge_weight requires bridge_edges > 0")
            if bridge_weight != 0.0:
                raise ValueError("freeze_reason=zero_bridge_weight requires bridge_weight == 0")
        if freeze_reason == "active" and bridge_edges == 0:
            raise ValueError("freeze_reason=active requires bridge_edges > 0")
        if freeze_reason == "active" and bridge_weight <= 0.0:
            raise ValueError("freeze_reason=active requires bridge_weight > 0")

    if loop_detection_regime is not None:
        if projection_regime is None:
            raise ValueError("loop_detection_regime requires projection_regime")
        if loop_detection_regime == "canonical_cluster_graph":
            if projection_regime != "canonical_separated":
                raise ValueError("canonical loop detection requires canonical_separated regime")
            for name, value in {
                "loop_count": loop_count,
                "max_loop_length": max_loop_length,
                "min_loop_length": min_loop_length,
                "mean_loop_length": mean_loop_length,
                "loop_edge_coverage_ratio": loop_edge_coverage_ratio,
            }.items():
                if value is None:
                    raise ValueError(f"{name} is required for canonical loop detection")
            loop_count = int(loop_count)
            max_loop_length = int(max_loop_length)
            min_loop_length = int(min_loop_length)
            mean_loop_length = float(mean_loop_length)
            loop_edge_coverage_ratio = float(loop_edge_coverage_ratio)
            if loop_count < 0:
                raise ValueError("loop_count must be >= 0")
            if max_loop_length < 0 or min_loop_length < 0:
                raise ValueError("loop lengths must be >= 0")
            if mean_loop_length < 0.0:
                raise ValueError("mean_loop_length must be >= 0")
            if loop_edge_coverage_ratio < 0.0 or loop_edge_coverage_ratio > 1.0:
                raise ValueError("loop_edge_coverage_ratio must be in [0, 1]")
            if loop_count == 0:
                if max_loop_length != 0 or min_loop_length != 0 or mean_loop_length != 0.0:
                    raise ValueError("zero-loop summaries must keep zero-valued length metrics")
            else:
                if min_loop_length < 3:
                    raise ValueError("detected loops must have topological length >= 3")
                if max_loop_length < min_loop_length:
                    raise ValueError("max_loop_length must be >= min_loop_length")
                if mean_loop_length < float(min_loop_length) or mean_loop_length > float(max_loop_length):
                    raise ValueError("mean_loop_length must lie between min and max loop length")
        else:
            if loop_detection_regime == "not_applicable_contaminated" and projection_regime != "diagnostic_contaminated":
                raise ValueError("contaminated loop detection regime requires diagnostic_contaminated projection")
            if loop_detection_regime == "not_applicable_legacy" and projection_regime != "legacy_visible_only":
                raise ValueError("legacy loop detection regime requires legacy_visible_only projection")
            for name, value in {
                "loop_count": loop_count,
                "max_loop_length": max_loop_length,
                "min_loop_length": min_loop_length,
                "mean_loop_length": mean_loop_length,
                "loop_edge_coverage_ratio": loop_edge_coverage_ratio,
            }.items():
                if value is not None:
                    raise ValueError(f"{name} must be absent when loop detection is not applicable")

    if loop_identity_regime is not None:
        if projection_regime is None:
            raise ValueError("loop_identity_regime requires projection_regime")
        if loop_identity_regime == "canonical_exact_signature":
            if projection_regime != "canonical_separated":
                raise ValueError("canonical loop identity requires canonical_separated regime")
            if loop_detection_regime != "canonical_cluster_graph":
                raise ValueError("canonical loop identity requires canonical loop detection")
            if loop_signatures is None or not isinstance(loop_signatures, list):
                raise ValueError("canonical loop identity requires loop_signatures list")
            normalized_signatures: list[str] = []
            for item in loop_signatures:
                if not isinstance(item, str):
                    raise ValueError("loop_signatures must contain strings only")
                if not item:
                    raise ValueError("loop_signatures entries must be non-empty")
                parts = item.split("-")
                if len(parts) < 3:
                    raise ValueError("loop signatures must describe cycles of length >= 3")
                try:
                    nodes = [int(part) for part in parts]
                except Exception as exc:
                    raise ValueError("loop signature contains non-integer node ids") from exc
                if len(nodes) != len(set(nodes)):
                    raise ValueError("loop signature must not repeat internal nodes")
                normalized_signatures.append("-".join(str(node) for node in nodes))
            if normalized_signatures != sorted(set(normalized_signatures)):
                raise ValueError("loop_signatures must be sorted and unique")
            if loop_count is None:
                raise ValueError("loop_count required with canonical loop identity")
            if len(normalized_signatures) != int(loop_count):
                raise ValueError("loop_signatures count must match loop_count")
            loop_signatures = normalized_signatures
        else:
            if loop_identity_regime == "not_applicable_contaminated" and projection_regime != "diagnostic_contaminated":
                raise ValueError("contaminated loop identity regime requires diagnostic_contaminated projection")
            if loop_identity_regime == "not_applicable_legacy" and projection_regime != "legacy_visible_only":
                raise ValueError("legacy loop identity regime requires legacy_visible_only projection")
            if loop_signatures is not None:
                raise ValueError("loop_signatures must be absent when loop identity is not applicable")

    if exclusion_candidate_regime is not None:
        if projection_regime is None:
            raise ValueError("exclusion_candidate_regime requires projection_regime")
        if exclusion_candidate_regime == "not_applicable_legacy" and projection_regime != "legacy_visible_only":
            raise ValueError("legacy exclusion candidate regime requires legacy_visible_only projection")
        if exclusion_candidate_regime == "not_applicable_contaminated" and projection_regime != "diagnostic_contaminated":
            raise ValueError("contaminated exclusion candidate regime requires diagnostic_contaminated projection")
        if exclusion_candidate_regime in {"canonical_identity_only", "canonical_candidate_path"}:
            if projection_regime != "canonical_separated":
                raise ValueError("canonical exclusion candidate regime requires canonical_separated projection")
            if loop_identity_regime != "canonical_exact_signature":
                raise ValueError("canonical exclusion candidate regime requires canonical loop identity")

    def optional_int_list(name: str) -> Optional[list[int]]:
        raw = snap.get(name)
        if raw is None:
            return None
        if not isinstance(raw, list):
            raise ValueError(f"{name} must be a list if provided")
        values: list[int] = []
        for item in raw:
            value = int(item)
            values.append(value)
        return values

    loop_orientation = optional_int_list("loop_orientation")
    loop_charge = optional_int_list("loop_charge")
    loop_excitation_index = optional_int_list("loop_excitation_index")
    loop_niche_anchor = optional_int_list("loop_niche_anchor")

    richer_identity_fields_present = any(
        value is not None
        for value in (loop_orientation, loop_charge, loop_excitation_index, loop_niche_anchor)
    )
    if richer_identity_fields_present:
        if projection_regime != "canonical_separated":
            raise ValueError("richer exclusion identity fields require canonical_separated projection")
        if loop_signatures is None:
            raise ValueError("richer exclusion identity fields require loop_signatures")
        expected_len = len(loop_signatures)
        for name, value in {
            "loop_orientation": loop_orientation,
            "loop_charge": loop_charge,
            "loop_excitation_index": loop_excitation_index,
            "loop_niche_anchor": loop_niche_anchor,
        }.items():
            if value is None:
                raise ValueError(f"{name} must be present with the full richer identity layer")
            if len(value) != expected_len:
                raise ValueError(f"{name} length must match loop_signatures")
        for value in loop_orientation:
            if value not in {-1, 1}:
                raise ValueError("loop_orientation values must be in {-1, +1}")
        for value in loop_excitation_index:
            if value < 0:
                raise ValueError("loop_excitation_index values must be >= 0")
        for value in loop_niche_anchor:
            if value < 0:
                raise ValueError("loop_niche_anchor values must be >= 0")
        for signature, orientation, charge in zip(loop_signatures, loop_orientation, loop_charge):
            loop_len = len(signature.split("-"))
            expected_charge = int(orientation * (loop_len % 2))
            if charge != expected_charge:
                raise ValueError("loop_charge must match orientation * (loop_length mod 2)")

    units = snap.get("units", "RI")
    meta = snap.get("meta") or {}

    if not isinstance(meta, dict):
        raise ValueError("meta must be a dict if provided")

    return FractureState(
        tick=int(tick),
        visible_edges=ve,
        visible_weight=vw,
        visible_ratio=vr,
        cluster_edges=cluster_edges,
        cluster_ratio=cluster_ratio,
        background_edges=background_edges,
        background_ratio=background_ratio,
        bridge_edges=bridge_edges,
        bridge_weight=bridge_weight,
        bridge_ratio=bridge_ratio,
        projection_regime=str(projection_regime) if projection_regime is not None else None,
        projection_contaminated=projection_contaminated,
        freeze_state=freeze_state,
        freeze_reason=str(freeze_reason) if freeze_reason is not None else None,
        loop_count=int(loop_count) if loop_count is not None else None,
        max_loop_length=int(max_loop_length) if max_loop_length is not None else None,
        min_loop_length=int(min_loop_length) if min_loop_length is not None else None,
        mean_loop_length=float(mean_loop_length) if mean_loop_length is not None else None,
        loop_edge_coverage_ratio=float(loop_edge_coverage_ratio) if loop_edge_coverage_ratio is not None else None,
        loop_detection_regime=str(loop_detection_regime) if loop_detection_regime is not None else None,
        loop_signatures=list(loop_signatures) if loop_signatures is not None else None,
        loop_identity_regime=str(loop_identity_regime) if loop_identity_regime is not None else None,
        loop_orientation=list(loop_orientation) if loop_orientation is not None else None,
        loop_charge=list(loop_charge) if loop_charge is not None else None,
        loop_excitation_index=list(loop_excitation_index) if loop_excitation_index is not None else None,
        loop_niche_anchor=list(loop_niche_anchor) if loop_niche_anchor is not None else None,
        exclusion_candidate_regime=str(exclusion_candidate_regime) if exclusion_candidate_regime is not None else None,
        meta=dict(meta),
        units=str(units),
    )
