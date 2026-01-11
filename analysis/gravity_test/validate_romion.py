"""Fail-closed validation for ROMION methodology.

Implements KROK 4 from GPT audit: Fail-closed w sensie ROMION (nie tylko technicznym).

Purpose:
- Eksperyment bez sensu ma się NIE WYKONAĆ
- Walidacja relacji progów (three-threshold separation)
- Walidacja geometrii tła
- Rozróżnienie: INVALID_TECH, INVALID_THEORY, PARTIAL

Three-Threshold Separation (MANDATORY):
- wcluster: defines OBJECTS (matter) - L2-FRACTURE
- wdist: defines GEOMETRY (background) - L2-FRACTURE  
- wbridge: defines FIELD (interactions) - L2-FRACTURE

Threshold Relations (MANDATORY):
- wcluster ≥ wdist > 0 (objects more stable than background)
- wbridge ≤ wcluster (field weaker than matter)
- All positive (no negative weights)

Status: v2.0 (ROMION O'LOGIC compliant)
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple
from enum import Enum


class ValidationStatus(Enum):
    """Validation outcome categories."""
    VALID = "VALID"
    INVALID_TECH = "INVALID_TECH"      # Technical error (NaN, negative, etc)
    INVALID_THEORY = "INVALID_THEORY"  # Violates ROMION methodology
    PARTIAL = "PARTIAL"                # Some metrics missing/degraded


def _is_finite_number(x: Any) -> bool:
    """Check if x is a finite number (int or float, not NaN/Inf)."""
    try:
        return isinstance(x, (int, float)) and math.isfinite(float(x))
    except (TypeError, ValueError):
        return False


def validate_thresholds(
    wcluster: float,
    wdist: float,
    wbridge: float
) -> Tuple[ValidationStatus, List[str]]:
    """Validate three-threshold separation (MANDATORY for ROMION).
    
    Args:
        wcluster: Threshold for objects/matter (L2-FRACTURE)
        wdist: Threshold for background geometry (L2-FRACTURE)
        wbridge: Threshold for field/interactions (L2-FRACTURE)
        
    Returns:
        (status, reasons) where status is ValidationStatus and reasons lists violations.
        
    MANDATORY Relations (from METHODOLOGY.md v2.0):
    1. wcluster ≥ wdist > 0
       - Objects must be more stable than background
       - Background must exist (positive threshold)
       
    2. wbridge ≤ wcluster
       - Field cannot be stronger than matter
       - Prevents "bridges stronger than clusters" paradox
       
    3. All thresholds positive
       - No negative weights in ROMION
       
    NOTE: wbridge can be < wdist (field weaker than background) - this is VALID.
          Field operates on sparse long-range connections, background is dense.
    """
    reasons: List[str] = []
    
    # Technical validation: finite numbers
    if not _is_finite_number(wcluster):
        reasons.append(f"wcluster not finite: {wcluster!r}")
    if not _is_finite_number(wdist):
        reasons.append(f"wdist not finite: {wdist!r}")
    if not _is_finite_number(wbridge):
        reasons.append(f"wbridge not finite: {wbridge!r}")
    
    if reasons:
        return ValidationStatus.INVALID_TECH, reasons
    
    # ROMION methodology validation: threshold relations
    
    # Rule 1: All positive
    if wcluster <= 0:
        reasons.append(f"wcluster must be > 0, got {wcluster}")
    if wdist <= 0:
        reasons.append(f"wdist must be > 0, got {wdist}")
    if wbridge < 0:
        reasons.append(f"wbridge must be >= 0, got {wbridge}")
    
    # Rule 2: wcluster >= wdist (objects more stable than background)
    if wcluster < wdist:
        reasons.append(
            f"THEORY VIOLATION: wcluster ({wcluster}) < wdist ({wdist}). "
            f"Objects must be more stable than background geometry."
        )
    
    # Rule 3: wbridge <= wcluster (field weaker than matter)
    if wbridge > wcluster:
        reasons.append(
            f"THEORY VIOLATION: wbridge ({wbridge}) > wcluster ({wcluster}). "
            f"Field cannot be stronger than matter."
        )
    
    # Warnings (not errors, but suspicious)
    warnings: List[str] = []
    
    if wbridge > wdist and wbridge < wcluster:
        # This is technically valid but unusual
        # Field is stronger than background but weaker than matter
        warnings.append(
            f"WARNING: wbridge ({wbridge}) between wdist ({wdist}) and wcluster ({wcluster}). "
            f"Field stronger than background - check if intentional."
        )
    
    if wcluster == wdist:
        warnings.append(
            f"WARNING: wcluster == wdist ({wcluster}). "
            f"Objects and background have same threshold - may cause degeneracy."
        )
    
    # Add warnings to reasons if present (but don't change status)
    if warnings and not reasons:
        # Valid but with warnings
        return ValidationStatus.VALID, warnings
    
    if reasons:
        return ValidationStatus.INVALID_THEORY, reasons
    
    return ValidationStatus.VALID, []


def validate_geometry(
    n_clusters: int,
    pairs_total: int,
    used_pairs: int,
    meta_bg_density: float = None
) -> Tuple[ValidationStatus, List[str]]:
    """Validate background geometry sanity.
    
    Args:
        n_clusters: Number of clusters detected
        pairs_total: Total possible cluster pairs (n_clusters choose 2)
        used_pairs: Pairs with defined distance
        meta_bg_density: Density of background meta-graph (optional)
        
    Returns:
        (status, reasons)
        
    Checks:
    1. Cluster count reasonable (2 <= n_clusters <= N)
    2. Pair counts consistent (used_pairs <= pairs_total)
    3. Background not over-dense (meta_bg_density < 0.5)
    4. Not fully fragmented (n_clusters < N/2)
    """
    reasons: List[str] = []
    
    # Technical checks
    if not isinstance(n_clusters, int) or n_clusters < 0:
        reasons.append(f"n_clusters invalid: {n_clusters!r}")
        return ValidationStatus.INVALID_TECH, reasons
    
    if not isinstance(pairs_total, int) or pairs_total < 0:
        reasons.append(f"pairs_total invalid: {pairs_total!r}")
        return ValidationStatus.INVALID_TECH, reasons
    
    if not isinstance(used_pairs, int) or used_pairs < 0:
        reasons.append(f"used_pairs invalid: {used_pairs!r}")
        return ValidationStatus.INVALID_TECH, reasons
    
    # Geometry sanity checks
    
    # Rule 1: Need at least 2 clusters for analysis
    if n_clusters < 2:
        reasons.append(
            f"GEOMETRY DEGENERATE: Only {n_clusters} cluster(s). "
            f"Need >= 2 for inter-cluster analysis."
        )
    
    # Rule 2: Pair consistency
    expected_pairs = n_clusters * (n_clusters - 1) // 2
    if pairs_total != expected_pairs:
        reasons.append(
            f"GEOMETRY INCONSISTENT: pairs_total ({pairs_total}) != "
            f"n_clusters choose 2 ({expected_pairs})"
        )
    
    if used_pairs > pairs_total:
        reasons.append(
            f"GEOMETRY INCONSISTENT: used_pairs ({used_pairs}) > "
            f"pairs_total ({pairs_total})"
        )
    
    # Rule 3: Background density check (if provided)
    if meta_bg_density is not None:
        if not _is_finite_number(meta_bg_density):
            reasons.append(f"meta_bg_density not finite: {meta_bg_density!r}")
        elif meta_bg_density > 0.8:
            reasons.append(
                f"GEOMETRY OVER-DENSE: meta_bg_density = {meta_bg_density:.1%}. "
                f"Background graph too dense (>80%), distances will be trivial (all dist=1). "
                f"Increase wdist threshold."
            )
        elif meta_bg_density > 0.5:
            reasons.append(
                f"WARNING: meta_bg_density = {meta_bg_density:.1%} (>50%). "
                f"Background may be too dense for meaningful range analysis. "
                f"Consider increasing wdist."
            )
    
    if reasons:
        # Check if any are critical (not just warnings)
        critical = any("GEOMETRY" in r and "WARNING" not in r for r in reasons)
        if critical:
            return ValidationStatus.INVALID_THEORY, reasons
        else:
            return ValidationStatus.VALID, reasons  # Just warnings
    
    return ValidationStatus.VALID, []


def validate_metrics(metrics: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate output metrics (backward compatibility with existing code).
    
    Args:
        metrics: Dictionary of metric names to values.
        
    Returns:
        (is_valid, reasons) where reasons lists all validation failures.
        
    This is the ORIGINAL validation from validate.py.
    For full ROMION validation, use validate_experiment() instead.
    """
    reasons: List[str] = []

    # List of keys that must be finite numbers if present
    numeric_keys = [
        "hub_share",
        "coverage",
        "unassigned_nodes",
        "skipped_edges_unassigned",
        "channel_capacity",
        "anisotropy",
        "bridges_count",
        "bridges_weight",
        "pairs_with_bridge",
    ]

    # Finite check for numeric values
    for k in numeric_keys:
        if k in metrics and metrics[k] is not None:
            if not _is_finite_number(metrics[k]):
                reasons.append(f"{k} is not finite: {metrics[k]!r}")

    # Bounds checks
    if "hub_share" in metrics and metrics["hub_share"] is not None:
        hs = float(metrics["hub_share"])
        if hs < 0.0 or hs > 100.0:
            reasons.append(f"hub_share out of [0,100]: {hs}")

    if "coverage" in metrics and metrics["coverage"] is not None:
        cv = float(metrics["coverage"])
        if cv < 0.0 or cv > 100.0:
            reasons.append(f"coverage out of [0,100]: {cv}")

    # Non-negative checks
    non_negative_keys = [
        "unassigned_nodes",
        "skipped_edges_unassigned",
        "channel_capacity",
        "anisotropy",
        "bridges_count",
        "bridges_weight",
        "pairs_with_bridge",
    ]
    
    for k in non_negative_keys:
        if k in metrics and metrics[k] is not None:
            val = metrics[k]
            if _is_finite_number(val) and float(val) < 0.0:
                reasons.append(f"{k} negative: {val}")

    return (len(reasons) == 0), reasons


def validate_experiment(
    wcluster: float,
    wdist: float,
    wbridge: float,
    n_clusters: int,
    pairs_total: int,
    used_pairs: int,
    meta_bg_density: float = None,
    output_metrics: Dict[str, Any] = None
) -> Tuple[ValidationStatus, List[str]]:
    """Complete ROMION fail-closed validation.
    
    Validates entire experiment according to ROMION O'LOGIC™ methodology.
    
    Args:
        wcluster, wdist, wbridge: Three thresholds
        n_clusters, pairs_total, used_pairs: Geometry metrics
        meta_bg_density: Background density (optional)
        output_metrics: Output metrics dict (optional)
        
    Returns:
        (status, reasons)
        
    Status Priority:
    1. INVALID_TECH: Technical error (NaN, negative where impossible)
    2. INVALID_THEORY: Violates ROMION methodology (threshold relations)
    3. PARTIAL: Degraded but usable (warnings only)
    4. VALID: All checks passed
    """
    all_reasons: List[str] = []
    worst_status = ValidationStatus.VALID
    
    # 1. Validate thresholds (MANDATORY)
    thresh_status, thresh_reasons = validate_thresholds(wcluster, wdist, wbridge)
    all_reasons.extend(thresh_reasons)
    if thresh_status.value == "INVALID_TECH" or thresh_status.value == "INVALID_THEORY":
        worst_status = thresh_status
    
    # 2. Validate geometry
    geom_status, geom_reasons = validate_geometry(
        n_clusters, pairs_total, used_pairs, meta_bg_density
    )
    all_reasons.extend(geom_reasons)
    if geom_status.value == "INVALID_TECH" or geom_status.value == "INVALID_THEORY":
        worst_status = geom_status
    
    # 3. Validate output metrics (if provided)
    if output_metrics is not None:
        metrics_valid, metrics_reasons = validate_metrics(output_metrics)
        if not metrics_valid:
            all_reasons.extend(metrics_reasons)
            if worst_status == ValidationStatus.VALID:
                worst_status = ValidationStatus.INVALID_TECH
    
    # 4. Determine final status
    if worst_status == ValidationStatus.VALID and all_reasons:
        # Has warnings but technically valid
        worst_status = ValidationStatus.PARTIAL
    
    return worst_status, all_reasons


def format_invalid_report(reasons: List[str]) -> str:
    """Format validation failures for output (backward compatibility)."""
    lines = ["INVALID RUN (fail-closed):"]
    for r in reasons:
        lines.append(f"  - {r}")
    return "\n".join(lines)


def format_validation_report(
    status: ValidationStatus,
    reasons: List[str]
) -> str:
    """Format complete validation report with status."""
    if status == ValidationStatus.VALID:
        return "VALIDATION: PASSED"
    
    status_labels = {
        ValidationStatus.INVALID_TECH: "[INVALID] Technical Error",
        ValidationStatus.INVALID_THEORY: "[INVALID] Methodology Violation",
        ValidationStatus.PARTIAL: "[PARTIAL] Warnings Present"
    }
    
    lines = [status_labels.get(status, f"[INVALID] {status.value}")]
    for r in reasons:
        prefix = "  [WARNING] " if "WARNING" in r else "  [ERROR] "
        lines.append(prefix + r)
    
    return "\n".join(lines)


# ============================================================================
# KROK 3: CANONICAL METRICS VALIDATION (NEW - 2026-01-11)
# ============================================================================
# Enforcement of CANONICAL_METRICS.md v1.0
# Single source of truth for metric definitions, bounds, and layer separation

def validate_L1_metrics(metrics: Dict[str, Any], schema_version: str = "1.0") -> Tuple[ValidationStatus, List[str]]:
    """Validate L1-CORE metrics against CANONICAL_METRICS.md.
    
    Args:
        metrics: Metrics dictionary (from metrics_pre or metrics_post)
        schema_version: "1.0" (legacy) or "2.0" (current)
        
    Returns:
        (status, reasons)
        
    Required L1-CORE metrics (all schemas):
    - mean_kappa: [0, 1] (approximately)
    - mean_pressure: [0, ∞)
    - total_weight: [0, ∞)
    - n_edges: ℕ (>= 0)
    - n_nodes: ℕ (> 0)
    
    Required in schema v2.0 ONLY:
    - mean_frustration: [0, 1]
    """
    reasons: List[str] = []
    
    # Required fields (all schemas)
    required_base = ['mean_kappa', 'mean_pressure', 'total_weight', 'n_edges', 'n_nodes']
    
    for field in required_base:
        if field not in metrics:
            reasons.append(f"Missing required L1-CORE metric: {field}")
    
    # Schema v2.0 requirements
    if schema_version == "2.0":
        if 'mean_frustration' not in metrics:
            reasons.append("Missing required L1-CORE metric (v2.0): mean_frustration")
    
    # If missing required fields, return early
    if reasons:
        return ValidationStatus.INVALID_THEORY, reasons
    
    # Validate bounds (CANONICAL_METRICS.md definitions)
    
    # mean_kappa: [0, 1] approximately (sigmoid)
    kappa = metrics.get('mean_kappa')
    if kappa is not None:
        if not _is_finite_number(kappa):
            reasons.append(f"mean_kappa not finite: {kappa!r}")
        elif kappa < 0 or kappa > 1.5:  # Allow slight overshoot
            reasons.append(f"mean_kappa out of bounds [0,1]: {kappa} (check implementation)")
    
    # mean_pressure: [0, ∞)
    pressure = metrics.get('mean_pressure')
    if pressure is not None:
        if not _is_finite_number(pressure):
            reasons.append(f"mean_pressure not finite: {pressure!r}")
        elif pressure < 0:
            reasons.append(f"mean_pressure negative: {pressure}")
    
    # mean_frustration: [0, 1] (if present)
    if 'mean_frustration' in metrics:
        frust = metrics['mean_frustration']
        if not _is_finite_number(frust):
            reasons.append(f"mean_frustration not finite: {frust!r}")
        elif frust < 0:
            reasons.append(f"mean_frustration negative: {frust}")
        elif frust > 1:
            reasons.append(f"mean_frustration > 1: {frust} (bounded by κ range)")
    
    # total_weight: [0, ∞)
    weight = metrics.get('total_weight')
    if weight is not None:
        if not _is_finite_number(weight):
            reasons.append(f"total_weight not finite: {weight!r}")
        elif weight < 0:
            reasons.append(f"total_weight negative: {weight}")
    
    # n_edges: ℕ
    n_edges = metrics.get('n_edges')
    if n_edges is not None:
        if not isinstance(n_edges, int) or n_edges < 0:
            reasons.append(f"n_edges must be non-negative integer: {n_edges!r}")
    
    # n_nodes: ℕ (> 0)
    n_nodes = metrics.get('n_nodes')
    if n_nodes is not None:
        if not isinstance(n_nodes, int) or n_nodes <= 0:
            reasons.append(f"n_nodes must be positive integer: {n_nodes!r}")
    
    # Cross-metric consistency
    if n_edges is not None and weight is not None:
        if n_edges > 0 and weight == 0:
            reasons.append("Inconsistent: n_edges > 0 but total_weight = 0")
    
    if pressure is not None and n_edges is not None:
        if pressure == 0 and n_edges > 0:
            reasons.append("Inconsistent: mean_pressure = 0 but n_edges > 0")
    
    if reasons:
        return ValidationStatus.INVALID_TECH, reasons
    
    return ValidationStatus.VALID, []


def validate_L2_metrics(projection: Dict[str, Any], metrics_post: Dict[str, Any], theta: float) -> Tuple[ValidationStatus, List[str]]:
    """Validate L2-FRACTURE projection metrics against CANONICAL_METRICS.md.
    
    Args:
        projection: Projection metrics dictionary
        metrics_post: Post-evolution L1 metrics (for consistency)
        theta: Projection threshold
        
    Returns:
        (status, reasons)
        
    Required L2-FRACTURE metrics:
    - visible_edges: [0, n_edges]
    - visible_ratio: [0, 1]
    
    CRITICAL: Projection must use metrics_post (not metrics_pre)
    """
    reasons: List[str] = []
    
    # Required fields
    if 'visible_edges' not in projection:
        reasons.append("Missing required L2-FRACTURE metric: visible_edges")
        return ValidationStatus.INVALID_THEORY, reasons
    
    # Validate theta
    if not _is_finite_number(theta):
        reasons.append(f"theta not finite: {theta!r}")
    elif theta < 0 or theta > 1:
        reasons.append(f"theta out of bounds [0,1]: {theta}")
    
    # visible_edges: [0, n_edges]
    visible = projection.get('visible_edges')
    n_edges = metrics_post.get('n_edges')
    
    if visible is not None:
        if not isinstance(visible, int) or visible < 0:
            reasons.append(f"visible_edges must be non-negative integer: {visible!r}")
        elif n_edges is not None and visible > n_edges:
            reasons.append(f"visible_edges ({visible}) > n_edges ({n_edges})")
    
    # visible_ratio: [0, 1] (if present)
    if 'visible_ratio' in projection:
        ratio = projection['visible_ratio']
        if not _is_finite_number(ratio):
            reasons.append(f"visible_ratio not finite: {ratio!r}")
        elif ratio < 0 or ratio > 1:
            reasons.append(f"visible_ratio out of bounds [0,1]: {ratio}")
        
        # Consistency check
        if visible is not None and n_edges is not None and n_edges > 0:
            expected_ratio = visible / n_edges
            if abs(ratio - expected_ratio) > 0.01:  # Tolerance for float
                reasons.append(
                    f"visible_ratio ({ratio:.3f}) inconsistent with "
                    f"visible_edges/n_edges ({expected_ratio:.3f})"
                )
    
    # mean_kappa_visible: [theta, 1] (if present)
    if 'mean_kappa_visible' in projection:
        kappa_vis = projection['mean_kappa_visible']
        if not _is_finite_number(kappa_vis):
            reasons.append(f"mean_kappa_visible not finite: {kappa_vis!r}")
        elif kappa_vis < theta - 0.01:  # Small tolerance
            reasons.append(f"mean_kappa_visible ({kappa_vis}) < theta ({theta}) - impossible by definition")
        elif kappa_vis > 1.5:
            reasons.append(f"mean_kappa_visible out of bounds [theta,1]: {kappa_vis}")
    
    # CRITICAL: Check uses_metrics_post flag (schema v2.0)
    if 'uses_metrics_post' in projection:
        if not projection['uses_metrics_post']:
            reasons.append(
                "CRITICAL METHODOLOGY VIOLATION: projection.uses_metrics_post = false. "
                "Projection MUST use metrics_post (after evolution), not metrics_pre."
            )
    
    if reasons:
        # Check if critical (methodology violation)
        critical = any("CRITICAL" in r for r in reasons)
        if critical:
            return ValidationStatus.INVALID_THEORY, reasons
        else:
            return ValidationStatus.INVALID_TECH, reasons
    
    return ValidationStatus.VALID, []


def validate_L3_metrics(metrics: Dict[str, Any]) -> Tuple[ValidationStatus, List[str]]:
    """Validate L3-INTERPRETATION metrics against CANONICAL_METRICS.md.
    
    Args:
        metrics: Analysis metrics dictionary
        
    Returns:
        (status, reasons)
        
    L3-INTERPRETATION metrics (all optional, but must be valid if present):
    - hub_share: [0, 100] (percentage)
    - coverage: [0, 100] (percentage)
    - R0: (0, ∞) (ratio)
    - R2: [0, 1] (probability)
    """
    reasons: List[str] = []
    
    # hub_share: [0, 100]
    if 'hub_share' in metrics and metrics['hub_share'] is not None:
        hs = metrics['hub_share']
        if not _is_finite_number(hs):
            reasons.append(f"hub_share not finite: {hs!r}")
        elif hs < 0 or hs > 100:
            reasons.append(f"hub_share out of bounds [0,100]: {hs}")
    
    # coverage: [0, 100]
    if 'coverage' in metrics and metrics['coverage'] is not None:
        cov = metrics['coverage']
        if not _is_finite_number(cov):
            reasons.append(f"coverage not finite: {cov!r}")
        elif cov < 0 or cov > 100:
            reasons.append(f"coverage out of bounds [0,100]: {cov}")
    
    # R0: (0, ∞)
    if 'R0' in metrics and metrics['R0'] is not None:
        r0 = metrics['R0']
        if not _is_finite_number(r0):
            reasons.append(f"R0 not finite: {r0!r}")
        elif r0 <= 0:
            reasons.append(f"R0 must be positive: {r0}")
    
    # R2: [0, 1]
    if 'R2' in metrics and metrics['R2'] is not None:
        r2 = metrics['R2']
        if not _is_finite_number(r2):
            reasons.append(f"R2 not finite: {r2!r}")
        elif r2 < 0 or r2 > 1:
            reasons.append(f"R2 out of bounds [0,1]: {r2}")
    
    # Cross-metric consistency (R0 = hub_share / coverage)
    if 'hub_share' in metrics and 'coverage' in metrics and 'R0' in metrics:
        hs = metrics['hub_share']
        cov = metrics['coverage']
        r0 = metrics['R0']
        
        if _is_finite_number(hs) and _is_finite_number(cov) and _is_finite_number(r0):
            if cov > 0:
                expected_r0 = hs / cov
                if abs(r0 - expected_r0) > 0.01:
                    reasons.append(
                        f"R0 ({r0:.3f}) inconsistent with hub_share/coverage ({expected_r0:.3f})"
                    )
    
    if reasons:
        return ValidationStatus.INVALID_TECH, reasons
    
    return ValidationStatus.VALID, []


def validate_canonical_metrics(
    metrics_pre: Dict[str, Any] = None,
    metrics_post: Dict[str, Any] = None,
    projection: Dict[str, Any] = None,
    analysis_metrics: Dict[str, Any] = None,
    theta: float = None,
    schema_version: str = "1.0"
) -> Tuple[ValidationStatus, List[str]]:
    """Complete canonical metrics validation (KROK 3 enforcement).
    
    Validates all metrics against CANONICAL_METRICS.md v1.0.
    
    Args:
        metrics_pre: L1-CORE metrics before U (optional)
        metrics_post: L1-CORE metrics after U (required if projection given)
        projection: L2-FRACTURE projection metrics (optional)
        analysis_metrics: L3-INTERPRETATION metrics (optional)
        theta: Projection threshold (required if projection given)
        schema_version: "1.0" or "2.0"
        
    Returns:
        (status, reasons)
        
    Validation layers:
    1. L1-CORE: Primary metrics (mean_kappa, pressure, frustration, etc)
    2. L2-FRACTURE: Projection metrics (visible_edges, uses_metrics_post)
    3. L3-INTERPRETATION: Analysis metrics (hub_share, coverage, R0, R2)
    """
    all_reasons: List[str] = []
    worst_status = ValidationStatus.VALID
    
    # 1. Validate L1-CORE metrics_pre (if provided)
    if metrics_pre is not None:
        status, reasons = validate_L1_metrics(metrics_pre, schema_version)
        if reasons:
            all_reasons.extend([f"[metrics_pre] {r}" for r in reasons])
        if status.value in ["INVALID_TECH", "INVALID_THEORY"]:
            worst_status = status
    
    # 2. Validate L1-CORE metrics_post (if provided)
    if metrics_post is not None:
        status, reasons = validate_L1_metrics(metrics_post, schema_version)
        if reasons:
            all_reasons.extend([f"[metrics_post] {r}" for r in reasons])
        if status.value in ["INVALID_TECH", "INVALID_THEORY"]:
            worst_status = status
    
    # 3. Validate L2-FRACTURE projection (if provided)
    if projection is not None:
        if metrics_post is None:
            all_reasons.append("[projection] CRITICAL: projection given but metrics_post missing")
            worst_status = ValidationStatus.INVALID_THEORY
        elif theta is None:
            all_reasons.append("[projection] theta missing (required for projection validation)")
            worst_status = ValidationStatus.INVALID_THEORY
        else:
            status, reasons = validate_L2_metrics(projection, metrics_post, theta)
            if reasons:
                all_reasons.extend([f"[projection] {r}" for r in reasons])
            if status.value in ["INVALID_TECH", "INVALID_THEORY"]:
                worst_status = status
    
    # 4. Validate L3-INTERPRETATION metrics (if provided)
    if analysis_metrics is not None:
        status, reasons = validate_L3_metrics(analysis_metrics)
        if reasons:
            all_reasons.extend([f"[analysis] {r}" for r in reasons])
        if status.value in ["INVALID_TECH", "INVALID_THEORY"]:
            worst_status = status
    
    # 5. Determine final status
    if worst_status == ValidationStatus.VALID and all_reasons:
        worst_status = ValidationStatus.PARTIAL
    
    return worst_status, all_reasons
