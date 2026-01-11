"""Fail-closed validation for gravity_test metrics.

Purpose:
- Prevent silent propagation of invalid runs (NaN/inf, impossible percentages).
- Keep analysis outputs trustworthy and comparable.

This validator is intentionally conservative: it flags anything outside
expected bounds rather than trying to "correct" it.

Status: MVP
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple


def _is_finite_number(x: Any) -> bool:
    """Check if x is a finite number (int or float, not NaN/Inf)."""
    try:
        return isinstance(x, (int, float)) and math.isfinite(float(x))
    except (TypeError, ValueError):
        return False


def validate_metrics(metrics: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate a metrics dict for fail-closed analysis.
    
    Args:
        metrics: Dictionary of metric names to values.
        
    Returns:
        (is_valid, reasons) where reasons lists all validation failures.
        
    Checked metrics:
        - hub_share: must be in [0, 100]
        - coverage: must be in [0, 100]
        - unassigned_nodes: must be >= 0
        - skipped_edges_unassigned: must be >= 0
        - channel_capacity: must be >= 0
        - anisotropy: must be >= 0
        
    All numeric values must be finite (not NaN or Inf).
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


def format_invalid_report(reasons: List[str]) -> str:
    """Format validation failures for output."""
    lines = ["INVALID RUN (fail-closed):"]
    for r in reasons:
        lines.append(f"  - {r}")
    return "\n".join(lines)
