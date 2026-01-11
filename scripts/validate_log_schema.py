#!/usr/bin/env python3
"""
ROMION Log Schema Validator

Enforces CANONICAL_LOG_CONTRACT.md v2.0

This is the AUTHORITATIVE validator for ROMION simulation logs.
All logs MUST pass validation before analysis.

Status codes:
- VALID: Fully compliant with schema v2.0
- LEGACY_V1: Old format (readable with warnings)
- INVALID_TECH: Technical error (malformed JSON, missing fields)
- INVALID_SEMANTIC: Methodology violation (layer confusion, wrong order)
- INCOMPLETE: Missing required events

Usage:
    from scripts.validate_log_schema import validate_log_schema
    
    result = validate_log_schema("experiments/run1/simulation.jsonl")
    
    if result.status == "VALID":
        # Proceed
    elif result.status == "LEGACY_V1":
        warnings.warn(result.message)
        # Proceed with caution
    else:
        # REJECT
        raise ValueError(result.message)
"""

import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum


class ValidationStatus(Enum):
    """Validation result status."""
    VALID = "VALID"
    LEGACY_V1 = "LEGACY_V1"
    INVALID_TECH = "INVALID_TECH"
    INVALID_SEMANTIC = "INVALID_SEMANTIC"
    INCOMPLETE = "INCOMPLETE"


@dataclass
class ValidationResult:
    """Result of log validation."""
    status: ValidationStatus
    version: Optional[str]  # "2.0", "1.0", or None
    message: str
    details: List[str]
    
    @property
    def is_valid(self) -> bool:
        """Check if log is valid for analysis."""
        return self.status == ValidationStatus.VALID
    
    @property
    def is_legacy(self) -> bool:
        """Check if log is legacy (acceptable with warnings)."""
        return self.status == ValidationStatus.LEGACY_V1
    
    @property
    def is_rejected(self) -> bool:
        """Check if log should be rejected."""
        return self.status in [
            ValidationStatus.INVALID_TECH,
            ValidationStatus.INVALID_SEMANTIC,
            ValidationStatus.INCOMPLETE
        ]


def validate_log_schema(log_path: Path | str) -> ValidationResult:
    """
    Validate log against CANONICAL_LOG_CONTRACT.md.
    
    This is fail-closed validation:
    - Any violation → REJECT
    - Legacy v1.0 → WARN
    - Unknown version → REJECT
    
    Args:
        log_path: Path to simulation.jsonl
        
    Returns:
        ValidationResult with status and details
    """
    log_path = Path(log_path)
    details = []
    
    # Check file exists
    if not log_path.exists():
        return ValidationResult(
            status=ValidationStatus.INVALID_TECH,
            version=None,
            message=f"File not found: {log_path}",
            details=["File does not exist"]
        )
    
    # Check extension
    if log_path.suffix != '.jsonl':
        details.append(f"Wrong extension: {log_path.suffix} (expected .jsonl)")
        return ValidationResult(
            status=ValidationStatus.INVALID_TECH,
            version=None,
            message="Invalid file extension",
            details=details
        )
    
    # Read and validate
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) == 0:
            return ValidationResult(
                status=ValidationStatus.INVALID_TECH,
                version=None,
                message="Empty log file",
                details=["File has no content"]
            )
        
        # Parse all events
        events = []
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                event = json.loads(line)
                events.append(event)
            except json.JSONDecodeError as e:
                return ValidationResult(
                    status=ValidationStatus.INVALID_TECH,
                    version=None,
                    message=f"Invalid JSON at line {i}",
                    details=[f"JSON parse error: {e}"]
                )
        
        if len(events) == 0:
            return ValidationResult(
                status=ValidationStatus.INVALID_TECH,
                version=None,
                message="No valid events in log",
                details=["All lines empty or invalid"]
            )
        
        # Validate schema
        return _validate_events(events, log_path, details)
        
    except Exception as e:
        return ValidationResult(
            status=ValidationStatus.INVALID_TECH,
            version=None,
            message=f"Error reading log: {e}",
            details=[str(e)]
        )


def _validate_events(
    events: List[Dict[str, Any]],
    log_path: Path,
    details: List[str]
) -> ValidationResult:
    """Validate event sequence and content."""
    
    first_event = events[0]
    
    # Check schema_version in first event
    if 'schema_version' not in first_event:
        # Legacy v1.0 format
        return _handle_legacy_v1(events, log_path, details)
    
    version = first_event['schema_version']
    
    # Check supported version
    if version == "2.0":
        return _validate_v2(events, log_path, details)
    elif version == "1.0":
        # Explicit v1.0 (rare, treat as legacy)
        return _handle_legacy_v1(events, log_path, details)
    else:
        details.append(f"Unsupported schema version: {version}")
        return ValidationResult(
            status=ValidationStatus.INVALID_TECH,
            version=version,
            message=f"Unknown schema version: {version}",
            details=details
        )


def _handle_legacy_v1(
    events: List[Dict[str, Any]],
    log_path: Path,
    details: List[str]
) -> ValidationResult:
    """Handle legacy v1.0 logs."""
    
    details.append("Missing schema_version field - detected as LEGACY v1.0")
    details.append("WARNING: No metrics_pre/post separation")
    details.append("WARNING: No frustration metrics")
    details.append("WARNING: No layer labels")
    details.append("WARNING: Results should be marked [LEGACY-V1]")
    
    # Basic v1 validation
    errors = []
    
    # Check for STATE or STATS events (v1 used "STATS")
    has_state = any(e.get('type') in ['STATE', 'STATS'] for e in events)
    if not has_state:
        errors.append("No STATE/STATS events found")
    
    if errors:
        return ValidationResult(
            status=ValidationStatus.INVALID_TECH,
            version="1.0",
            message="Invalid legacy v1.0 log",
            details=details + errors
        )
    
    return ValidationResult(
        status=ValidationStatus.LEGACY_V1,
        version="1.0",
        message=f"Legacy v1.0 log: {log_path.name}",
        details=details
    )


def _validate_v2(
    events: List[Dict[str, Any]],
    log_path: Path,
    details: List[str]
) -> ValidationResult:
    """Validate schema v2.0 log."""
    
    errors = []
    
    # 1. First event MUST be METADATA
    first_event = events[0]
    if first_event.get('type') != 'METADATA':
        errors.append(
            f"First event must be METADATA, got: {first_event.get('type')}"
        )
        return ValidationResult(
            status=ValidationStatus.INVALID_SEMANTIC,
            version="2.0",
            message="Wrong event order",
            details=details + errors
        )
    
    # 2. Validate METADATA
    metadata_errors = _validate_metadata(first_event)
    if metadata_errors:
        return ValidationResult(
            status=ValidationStatus.INVALID_TECH,
            version="2.0",
            message="Invalid METADATA event",
            details=details + metadata_errors
        )
    
    # 3. Last event SHOULD be COMPLETION (not always present if interrupted)
    last_event = events[-1]
    has_completion = last_event.get('type') == 'COMPLETION'
    
    if not has_completion:
        details.append("WARNING: No COMPLETION event (run may be incomplete)")
    
    # 4. Find and validate STATE events
    state_events = [e for e in events if e.get('type') == 'STATE']
    
    if len(state_events) == 0:
        errors.append("No STATE events found")
        return ValidationResult(
            status=ValidationStatus.INCOMPLETE,
            version="2.0",
            message="Incomplete log - no STATE events",
            details=details + errors
        )
    
    # 5. Validate STATE events (sample first and last)
    for i, state in enumerate([state_events[0], state_events[-1]]):
        state_errors = _validate_state_v2(state, i)
        if state_errors:
            errors.extend(state_errors)
    
    if errors:
        return ValidationResult(
            status=ValidationStatus.INVALID_SEMANTIC,
            version="2.0",
            message="Schema v2.0 validation failed",
            details=details + errors
        )
    
    # 6. Check tick monotonicity
    ticks = [e['tick'] for e in state_events if 'tick' in e]
    if ticks != sorted(ticks):
        errors.append("Ticks not monotonically increasing")
        return ValidationResult(
            status=ValidationStatus.INVALID_SEMANTIC,
            version="2.0",
            message="Non-monotonic ticks",
            details=details + errors
        )
    
    # SUCCESS
    details.append("VALID: Schema v2.0 compliant")
    details.append(f"VALID: {len(state_events)} STATE events")
    details.append(f"VALID: Ticks {ticks[0]} -> {ticks[-1]}")
    
    return ValidationResult(
        status=ValidationStatus.VALID,
        version="2.0",
        message=f"Valid v2.0 log: {log_path.name}",
        details=details
    )


def _validate_metadata(event: Dict[str, Any]) -> List[str]:
    """Validate METADATA event."""
    errors = []
    
    required_fields = [
        'schema_version',
        'type',
        'run_id',
        'seed',
        'config_hash',
        'timestamp_utc',
        'python_version',
        'platform',
        'experiment_name',
        'parameters'
    ]
    
    for field in required_fields:
        if field not in event:
            errors.append(f"METADATA missing required field: {field}")
    
    # Type checks
    if 'seed' in event and not isinstance(event['seed'], int):
        errors.append(f"METADATA.seed must be integer, got: {type(event['seed'])}")
    
    if 'seed' in event and event['seed'] < 0:
        errors.append(f"METADATA.seed must be >= 0, got: {event['seed']}")
    
    if 'parameters' in event and not isinstance(event['parameters'], dict):
        errors.append("METADATA.parameters must be dict")
    
    # Check config_hash format (should be hex string)
    if 'config_hash' in event:
        hash_str = event['config_hash']
        if not isinstance(hash_str, str):
            errors.append("METADATA.config_hash must be string")
        elif len(hash_str) not in [64, 40]:  # SHA256 or SHA1
            errors.append(f"METADATA.config_hash wrong length: {len(hash_str)}")
    
    return errors


def _validate_state_v2(event: Dict[str, Any], index: int) -> List[str]:
    """Validate STATE event (schema v2.0)."""
    errors = []
    
    # Required fields
    if 'tick' not in event:
        errors.append(f"STATE[{index}] missing 'tick'")
    
    # Required sections
    required_sections = [
        'metrics_pre',
        'evolution',
        'metrics_post',
        'projection',
        'observables'
    ]
    
    for section in required_sections:
        if section not in event:
            errors.append(f"STATE[{index}] missing required section: {section}")
    
    # If sections present, validate structure
    if 'metrics_pre' in event:
        pre_errors = _validate_metrics_pre(event['metrics_pre'], index)
        errors.extend(pre_errors)
    
    if 'metrics_post' in event:
        post_errors = _validate_metrics_post(event['metrics_post'], index)
        errors.extend(post_errors)
    
    if 'projection' in event:
        proj_errors = _validate_projection(event['projection'], index)
        errors.extend(proj_errors)
    
    if 'evolution' in event:
        evo_errors = _validate_evolution(event['evolution'], index)
        errors.extend(evo_errors)
    
    return errors


def _validate_metrics_pre(metrics: Dict[str, Any], index: int) -> List[str]:
    """Validate metrics_pre section."""
    errors = []
    
    # Layer label
    if metrics.get('layer') != 'L1-CORE':
        errors.append(
            f"STATE[{index}].metrics_pre.layer must be 'L1-CORE', "
            f"got: {metrics.get('layer')}"
        )
    
    # Temporal flag
    if not metrics.get('computed_before_U'):
        errors.append(
            f"STATE[{index}].metrics_pre must have computed_before_U=true"
        )
    
    # Required metrics
    required = ['mean_kappa', 'mean_pressure', 'mean_frustration', 'n_edges', 'n_nodes']
    for field in required:
        if field not in metrics:
            errors.append(f"STATE[{index}].metrics_pre missing: {field}")
        elif field.startswith('mean_') or field == 'total_weight':
            # Check finite
            value = metrics[field]
            if not isinstance(value, (int, float)):
                errors.append(f"STATE[{index}].metrics_pre.{field} not numeric")
            elif not _is_finite(value):
                errors.append(f"STATE[{index}].metrics_pre.{field} not finite (NaN/Inf)")
    
    # New in v2.0: frustration REQUIRED
    if 'mean_frustration' not in metrics:
        errors.append(
            f"STATE[{index}].metrics_pre missing 'mean_frustration' (required in v2.0)"
        )
    
    return errors


def _validate_metrics_post(metrics: Dict[str, Any], index: int) -> List[str]:
    """Validate metrics_post section."""
    errors = []
    
    # Layer label
    if metrics.get('layer') != 'L1-CORE':
        errors.append(
            f"STATE[{index}].metrics_post.layer must be 'L1-CORE', "
            f"got: {metrics.get('layer')}"
        )
    
    # Temporal flag
    if not metrics.get('computed_after_U'):
        errors.append(
            f"STATE[{index}].metrics_post must have computed_after_U=true"
        )
    
    # Required metrics (same as pre)
    required = ['mean_kappa', 'mean_pressure', 'mean_frustration', 'n_edges', 'n_nodes']
    for field in required:
        if field not in metrics:
            errors.append(f"STATE[{index}].metrics_post missing: {field}")
        elif field.startswith('mean_') or field == 'total_weight':
            value = metrics[field]
            if not isinstance(value, (int, float)):
                errors.append(f"STATE[{index}].metrics_post.{field} not numeric")
            elif not _is_finite(value):
                errors.append(f"STATE[{index}].metrics_post.{field} not finite")
    
    # Frustration required
    if 'mean_frustration' not in metrics:
        errors.append(
            f"STATE[{index}].metrics_post missing 'mean_frustration' (required in v2.0)"
        )
    
    return errors


def _validate_projection(projection: Dict[str, Any], index: int) -> List[str]:
    """Validate projection section."""
    errors = []
    
    # Layer label
    if projection.get('layer') != 'L2-FRACTURE':
        errors.append(
            f"STATE[{index}].projection.layer must be 'L2-FRACTURE', "
            f"got: {projection.get('layer')}"
        )
    
    # CRITICAL: Must use metrics_post
    if not projection.get('uses_metrics_post'):
        errors.append(
            f"STATE[{index}].projection must have uses_metrics_post=true "
            f"(projection MUST use post-evolution metrics)"
        )
    
    # Required fields
    if 'theta' not in projection:
        errors.append(f"STATE[{index}].projection missing 'theta'")
    
    if 'visible_edges' not in projection:
        errors.append(f"STATE[{index}].projection missing 'visible_edges'")
    
    # Check theta value
    if 'theta' in projection:
        theta = projection['theta']
        if not isinstance(theta, (int, float)):
            errors.append(f"STATE[{index}].projection.theta not numeric")
        elif theta < 0 or theta > 1:
            errors.append(f"STATE[{index}].projection.theta out of range [0,1]: {theta}")
    
    return errors


def _validate_evolution(evolution: Dict[str, Any], index: int) -> List[str]:
    """Validate evolution section."""
    errors = []
    
    # Layer label
    if evolution.get('layer') != 'L1-CORE':
        errors.append(
            f"STATE[{index}].evolution.layer must be 'L1-CORE', "
            f"got: {evolution.get('layer')}"
        )
    
    # Count fields (all should be >= 0)
    count_fields = ['spawn_new', 'spawn_reinf', 'field_tail_added', 'removed', 'norm_ops']
    
    for field in count_fields:
        if field in evolution:
            value = evolution[field]
            if not isinstance(value, int):
                errors.append(f"STATE[{index}].evolution.{field} must be integer")
            elif value < 0:
                errors.append(f"STATE[{index}].evolution.{field} must be >= 0, got: {value}")
    
    return errors


def _is_finite(value: float) -> bool:
    """Check if value is finite (not NaN or Inf)."""
    import math
    return math.isfinite(value)


def main():
    """CLI interface for validation."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python validate_log_schema.py <log_file>")
        print()
        print("Example:")
        print("  python validate_log_schema.py experiments/run1/simulation.jsonl")
        sys.exit(1)
    
    log_path = Path(sys.argv[1])
    
    print("=" * 70)
    print("ROMION Log Schema Validator")
    print("=" * 70)
    print(f"File: {log_path}")
    print()
    
    result = validate_log_schema(log_path)
    
    print(f"Status: {result.status.value}")
    print(f"Version: {result.version or 'UNKNOWN'}")
    print(f"Message: {result.message}")
    print()
    
    if result.details:
        print("Details:")
        for detail in result.details:
            print(f"  {detail}")
        print()
    
    if result.is_valid:
        print("[VALID] Ready for analysis")
        sys.exit(0)
    elif result.is_legacy:
        print("[LEGACY] Use with warnings, mark results [LEGACY-V1]")
        sys.exit(0)
    else:
        print("[REJECTED] Fix and rerun")
        sys.exit(1)


if __name__ == "__main__":
    main()
