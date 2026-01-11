"""
Run metadata structure for ROMION experiments.

Implements KROK 6: Complete, reproducible run tracking.

Each run must have:
- config.json: Full parameter set + hash
- metadata.json: Seed, timestamps, git info, system info
- simulation.jsonl: Evolution log
- validation.json: Fail-closed validation report
- status.json: Final completion status

Without ALL files, run is INCOMPLETE and ignored by analysis.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Optional
import hashlib
import json
import platform


@dataclass
class RunMetadata:
    """Complete metadata for experiment reproducibility."""
    
    # Identity
    run_id: str              # Unique identifier (datetime + hash)
    seed: int                # RNG seed
    config_hash: str         # SHA256 of sorted params
    
    # Timing
    start_time: str          # ISO 8601 UTC
    end_time: Optional[str]  # ISO 8601 UTC (None if incomplete)
    duration_seconds: Optional[float]  # Wall-clock time
    
    # Code state
    git_commit: Optional[str]    # Git SHA (if available)
    git_branch: Optional[str]    # Git branch
    git_dirty: Optional[bool]    # Uncommitted changes?
    
    # Environment
    python_version: str      # "3.11.5"
    platform: str            # "Linux-5.15.0-x86_64"
    hostname: str            # Machine identifier
    
    # Purpose
    experiment_name: str     # "decay_sweep"
    sweep_param: Optional[str]  # "decay" (if part of sweep)
    sweep_value: Optional[float]  # 0.7 (if part of sweep)
    notes: Optional[str]     # User notes
    
    def to_dict(self) -> Dict:
        """Convert to JSON-serializable dict."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'RunMetadata':
        """Load from dict."""
        return cls(**data)


@dataclass
class RunConfig:
    """Complete configuration for reproducibility."""
    
    params: Dict             # All simulation parameters
    config_hash: str         # SHA256 of sorted params
    
    # Graph initialization
    n_nodes: int
    n_edges_initial: int
    init_w_range: tuple      # (min, max) for random weights
    
    # Evolution
    n_ticks: int
    dump_graph_every: int    # How often to save full graph
    
    def to_dict(self) -> Dict:
        """Convert to JSON-serializable dict."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'RunConfig':
        """Load from dict."""
        return cls(**data)


@dataclass
class ValidationReport:
    """Validation results (fail-closed)."""
    
    is_valid: bool
    validation_status: str   # "VALID", "INVALID_TECH", "INVALID_THEORY", "PARTIAL"
    reasons: list            # List of validation messages
    
    # Metrics checked
    threshold_check: Optional[Dict]   # wcluster/wdist/wbridge relations
    geometry_check: Optional[Dict]    # cluster count, density, etc.
    
    # Timestamp
    validated_at: str        # ISO 8601 UTC
    
    def to_dict(self) -> Dict:
        """Convert to JSON-serializable dict."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ValidationReport':
        """Load from dict."""
        return cls(**data)


@dataclass
class RunStatus:
    """Final completion status."""
    
    completed: bool          # Did run finish?
    success: bool            # Did it succeed without errors?
    error: Optional[str]     # Error message if failed
    
    # Outcomes
    final_tick: int          # Last tick reached
    final_n_edges: int       # Final edge count
    freeze_detected: bool    # Did system freeze?
    freeze_tick: Optional[int]  # When freeze occurred
    
    # Validation
    validated: bool          # Was validation run?
    validation_passed: bool  # Did validation pass?
    
    # Timestamp
    completed_at: str        # ISO 8601 UTC
    
    def to_dict(self) -> Dict:
        """Convert to JSON-serializable dict."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'RunStatus':
        """Load from dict."""
        return cls(**data)


def compute_config_hash(params: Dict) -> str:
    """
    Compute deterministic hash of parameters.
    
    Sorts keys to ensure reproducibility.
    """
    # Sort keys for determinism
    sorted_params = dict(sorted(params.items()))
    
    # Convert to JSON string
    json_str = json.dumps(sorted_params, sort_keys=True)
    
    # Hash
    return hashlib.sha256(json_str.encode()).hexdigest()


def get_git_info() -> tuple:
    """
    Get git commit info if available.
    
    Returns:
        (commit, branch, is_dirty)
    """
    try:
        import subprocess
        
        # Get commit
        commit = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        
        # Get branch
        branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        
        # Check if dirty
        status = subprocess.check_output(
            ['git', 'status', '--porcelain'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        is_dirty = len(status) > 0
        
        return commit, branch, is_dirty
        
    except Exception:
        return None, None, None


def create_run_metadata(
    seed: int,
    config_hash: str,
    experiment_name: str,
    sweep_param: Optional[str] = None,
    sweep_value: Optional[float] = None,
    notes: Optional[str] = None
) -> RunMetadata:
    """
    Create metadata for new run.
    
    Auto-fills: timestamps, git info, system info.
    """
    now = datetime.utcnow().isoformat() + 'Z'
    run_id = f"{now}_{config_hash[:8]}"
    
    git_commit, git_branch, git_dirty = get_git_info()
    
    return RunMetadata(
        run_id=run_id,
        seed=seed,
        config_hash=config_hash,
        start_time=now,
        end_time=None,
        duration_seconds=None,
        git_commit=git_commit,
        git_branch=git_branch,
        git_dirty=git_dirty,
        python_version=platform.python_version(),
        platform=platform.platform(),
        hostname=platform.node(),
        experiment_name=experiment_name,
        sweep_param=sweep_param,
        sweep_value=sweep_value,
        notes=notes
    )


def finalize_run_metadata(
    metadata: RunMetadata,
    duration_seconds: float
) -> RunMetadata:
    """
    Finalize metadata after run completes.
    
    Sets end_time and duration.
    """
    metadata.end_time = datetime.utcnow().isoformat() + 'Z'
    metadata.duration_seconds = duration_seconds
    return metadata


def save_metadata(metadata: RunMetadata, filepath: str):
    """Save metadata to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(metadata.to_dict(), f, indent=2)


def save_config(config: RunConfig, filepath: str):
    """Save config to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(config.to_dict(), f, indent=2)


def save_validation(report: ValidationReport, filepath: str):
    """Save validation report to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(report.to_dict(), f, indent=2)


def save_status(status: RunStatus, filepath: str):
    """Save run status to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(status.to_dict(), f, indent=2)


def load_metadata(filepath: str) -> RunMetadata:
    """Load metadata from JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return RunMetadata.from_dict(data)


def load_config(filepath: str) -> RunConfig:
    """Load config from JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return RunConfig.from_dict(data)


def load_validation(filepath: str) -> ValidationReport:
    """Load validation report from JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return ValidationReport.from_dict(data)


def load_status(filepath: str) -> RunStatus:
    """Load run status from JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return RunStatus.from_dict(data)


def is_run_complete(run_dir: str) -> tuple:
    """
    Check if run directory is complete (KROK 6 requirement).
    
    Returns:
        (is_complete, missing_files)
    """
    from pathlib import Path
    
    run_path = Path(run_dir)
    
    required_files = [
        'config.json',
        'metadata.json',
        'simulation.jsonl',
        'validation.json',
        'status.json'
    ]
    
    missing = []
    for filename in required_files:
        if not (run_path / filename).exists():
            missing.append(filename)
    
    return (len(missing) == 0), missing


def validate_run_for_analysis(run_dir: str) -> tuple:
    """
    Validate run for analysis (KROK 6 fail-closed).
    
    Checks:
    1. All required files present
    2. Status = completed + success
    3. Validation = passed
    4. Config has hash
    5. Metadata has seed
    
    Returns:
        (is_valid, reasons)
    """
    from pathlib import Path
    
    reasons = []
    run_path = Path(run_dir)
    
    # Check completeness
    is_complete, missing = is_run_complete(run_dir)
    if not is_complete:
        reasons.append(f"Missing files: {', '.join(missing)}")
        return False, reasons
    
    # Load files
    try:
        config = load_config(run_path / 'config.json')
        metadata = load_metadata(run_path / 'metadata.json')
        status = load_status(run_path / 'status.json')
        validation = load_validation(run_path / 'validation.json')
    except Exception as e:
        reasons.append(f"Failed to load files: {e}")
        return False, reasons
    
    # Check status
    if not status.completed:
        reasons.append("Run not completed")
    if not status.success:
        reasons.append(f"Run failed: {status.error}")
    
    # Check validation
    if not status.validated:
        reasons.append("Run not validated")
    if not status.validation_passed:
        reasons.append("Validation failed")
    
    # Check config
    if not config.config_hash:
        reasons.append("Config missing hash")
    
    # Check metadata
    if metadata.seed is None:
        reasons.append("Metadata missing seed")
    if not metadata.end_time:
        reasons.append("Metadata incomplete (no end_time)")
    
    return (len(reasons) == 0), reasons
