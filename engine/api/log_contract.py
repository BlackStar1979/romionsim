"""
ROMION Engine Log Contract (API-level)

This module defines the minimal logging contract for romionsim.
It is a contract specification, not an implementation.

Goals:
- schema-versioned logs
- explicit parameters
- reproducibility
- fail-closed behavior

Applies to ontology: THEORY_V3.9
Documentation status: v1-prerelease
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


SCHEMA_VERSION_CURRENT = "2.0"


@dataclass(frozen=True)
class LogEventTypes:
    """
    Canonical event types written to simulation logs.

    The engine must write these event types.
    Validators and analyzers must expect these event types.
    """
    METADATA: str = "METADATA"
    PARAMS: str = "PARAMS"
    TICK: str = "TICK"
    END: str = "END"


def make_metadata_event(schema_version: str = SCHEMA_VERSION_CURRENT) -> Dict[str, Any]:
    """
    First line of every simulation log.

    Must include:
    - type = METADATA
    - schema_version
    """
    return {
        "type": LogEventTypes.METADATA,
        "schema_version": schema_version,
    }


def make_params_event(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Second line of every simulation log.

    Must include:
    - type = PARAMS
    - params: explicit parameter dict
    """
    return {
        "type": LogEventTypes.PARAMS,
        "params": dict(params),
    }


def make_tick_event(
    tick: int,
    core: Optional[Dict[str, Any]] = None,
    fracture: Optional[Dict[str, Any]] = None,
    notes: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Standard tick event.

    Rules:
    - tick is required
    - core and fracture fields must be serializable dicts if present
    - no engine internal objects may be embedded
    - domain interpretations must not appear here

    Minimal recommended structure:
    - core: internal structural stats (RI)
    - fracture: observable stats (RI unless explicitly SI)
    """
    ev: Dict[str, Any] = {
        "type": LogEventTypes.TICK,
        "tick": int(tick),
    }
    if core is not None:
        ev["core"] = dict(core)
    if fracture is not None:
        ev["fracture"] = dict(fracture)
    if notes is not None:
        ev["notes"] = dict(notes)
    return ev


def make_exclusion_rejection_note(
    *,
    rejection_stage: str = "stabilization",
    rejection_reason: str = "duplicate_niche_identity",
    rejection_identity_complete: bool = True,
) -> Dict[str, Any]:
    """
    Minimal Stage 5 rejection-note helper.

    This helper records a process/event fact rather than a FRACTURE state field.
    It is intentionally narrow:
    - one explicit rejection signal
    - one rejection stage
    - one MVP reason
    """
    return {
        "exclusion_rejection": True,
        "rejection_stage": str(rejection_stage),
        "rejection_reason": str(rejection_reason),
        "rejection_identity_complete": bool(rejection_identity_complete),
    }


def make_end_event(
    run_id: str,
    ok: bool,
    reason: Optional[str] = None,
    summary: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    End event written after the last tick.

    Must include:
    - type = END
    - run_id
    - ok: success flag

    If ok is false, reason should be provided (fail-closed trace).
    """
    ev: Dict[str, Any] = {
        "type": LogEventTypes.END,
        "run_id": str(run_id),
        "ok": bool(ok),
    }
    if reason:
        ev["reason"] = str(reason)
    if summary is not None:
        ev["summary"] = dict(summary)
    return ev


def minimal_log_order() -> Dict[str, Any]:
    """
    Human-readable description of the minimal log order.

    This is a contract helper, not used by the engine directly.
    """
    return {
        "required_order": [
            LogEventTypes.METADATA,
            LogEventTypes.PARAMS,
            LogEventTypes.TICK,
            LogEventTypes.END,
        ],
        "notes": [
            "METADATA must be the first line.",
            "PARAMS must be the second line and must include all explicit parameters.",
            "TICK events follow in ascending tick order.",
            "END is the final line.",
        ],
    }
