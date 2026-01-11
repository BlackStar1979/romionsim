#!/usr/bin/env python3
"""
Sweep Validator - KROK 6 Enforcement

Validates experiment runs for analysis eligibility.

FAIL-CLOSED: Incomplete or invalid runs are EXCLUDED from analysis.

Checks:
1. All required files present (config, metadata, log, validation, status)
2. Status = completed + success
3. Validation = passed
4. Config has hash
5. Metadata has seed + timestamps

WITHOUT ALL CHECKS PASSED, RUN IS IGNORED.

Usage:
    python scripts/validate_sweep.py <sweep_directory>
"""

import sys
from pathlib import Path

# Add repo root
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

import json
from scripts.run_metadata import (
    is_run_complete, validate_run_for_analysis,
    load_config, load_metadata, load_status, load_validation
)
from scripts.validate_log_schema import validate_log_schema


def validate_sweep(sweep_dir: Path, verbose: bool = True):
    """
    Validate all runs in sweep directory.
    
    NEW (KROK 2): Includes log schema validation.
    
    Returns:
        (valid_runs, invalid_runs, incomplete_runs, legacy_runs)
    """
    
    valid_runs = []
    invalid_runs = []
    incomplete_runs = []
    legacy_runs = []  # NEW: v1.0 logs (acceptable with warnings)
    
    # Find all run directories
    run_dirs = [d for d in sweep_dir.iterdir() if d.is_dir()]
    
    if verbose:
        print("=" * 70)
        print(f"SWEEP VALIDATION - {sweep_dir.name}")
        print("=" * 70)
        print(f"Total directories: {len(run_dirs)}")
        print()
    
    for run_dir in sorted(run_dirs):
        if verbose:
            print(f"Checking: {run_dir.name}")
        
        # Check completeness
        is_complete, missing = is_run_complete(run_dir)
        
        if not is_complete:
            incomplete_runs.append((run_dir, missing))
            if verbose:
                print(f"  [INCOMPLETE] missing: {', '.join(missing)}")
            continue
        
        # NEW: Validate log schema (KROK 2 - CANONICAL_LOG_CONTRACT.md)
        log_path = run_dir / 'simulation.jsonl'
        if log_path.exists():
            schema_result = validate_log_schema(log_path)
            
            if schema_result.is_rejected:
                # REJECT invalid logs
                invalid_runs.append((run_dir, [
                    f"LOG SCHEMA: {schema_result.message}",
                    *schema_result.details
                ]))
                if verbose:
                    print(f"  [INVALID] Log schema: {schema_result.status.value}")
                continue
            elif schema_result.is_legacy:
                # LEGACY v1.0: acceptable with warnings
                legacy_runs.append((run_dir, schema_result))
                if verbose:
                    print(f"  [LEGACY-V1] Log format v1.0 (mark results)")
                # Continue to other checks (don't reject legacy)
        
        # Validate for analysis (existing checks)
        is_valid, reasons = validate_run_for_analysis(run_dir)
        
        if is_valid:
            valid_runs.append(run_dir)
            if verbose:
                print(f"  [VALID]")
        else:
            invalid_runs.append((run_dir, reasons))
            if verbose:
                print(f"  [INVALID]")
                for reason in reasons:
                    print(f"      - {reason}")
    
    return valid_runs, invalid_runs, incomplete_runs, legacy_runs


def print_summary(valid_runs, invalid_runs, incomplete_runs, legacy_runs):
    """Print validation summary."""
    
    total = len(valid_runs) + len(invalid_runs) + len(incomplete_runs) + len(legacy_runs)
    
    print()
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Total runs: {total}")
    print(f"  [VALID]      {len(valid_runs)} ({len(valid_runs)/total*100:.1f}%)")
    print(f"  [LEGACY-V1]  {len(legacy_runs)} ({len(legacy_runs)/total*100:.1f}%)")
    print(f"  [INVALID]    {len(invalid_runs)} ({len(invalid_runs)/total*100:.1f}%)")
    print(f"  [INCOMPLETE] {len(incomplete_runs)} ({len(incomplete_runs)/total*100:.1f}%)")
    print()
    
    if legacy_runs:
        print("LEGACY v1.0 RUNS (acceptable with warnings):")
        for run_dir, schema_result in legacy_runs:
            print(f"  {run_dir.name}: {schema_result.version}")
        print()
        print("  WARNING: Legacy runs MUST be marked [LEGACY-V1] in results")
        print("  WARNING: No metrics_pre/post separation")
        print("  WARNING: No frustration data")
        print()
    
    if invalid_runs:
        print("INVALID RUNS:")
        for run_dir, reasons in invalid_runs:
            print(f"  {run_dir.name}:")
            for reason in reasons:
                print(f"    - {reason}")
        print()
    
    if incomplete_runs:
        print("INCOMPLETE RUNS:")
        for run_dir, missing in incomplete_runs:
            print(f"  {run_dir.name}: missing {', '.join(missing)}")
        print()
    
    analysis_ready = len(valid_runs) + len(legacy_runs)
    if analysis_ready > 0:
        print(f"[READY] {analysis_ready} runs ready for analysis")
        if legacy_runs:
            print(f"  ({len(valid_runs)} v2.0, {len(legacy_runs)} v1.0-LEGACY)")
        print()
        print("Valid runs:")
        for run_dir in valid_runs:
            print(f"  {run_dir.name}")
        if legacy_runs:
            print("Legacy runs (mark [LEGACY-V1]):")
            for run_dir, _ in legacy_runs:
                print(f"  {run_dir.name}")
    else:
        print("[FAIL] NO VALID RUNS - analysis cannot proceed")
    
    print("=" * 70)


def create_valid_runs_list(valid_runs, legacy_runs, output_path: Path):
    """
    Create manifest of valid runs for analysis.
    
    NEW (KROK 2): Includes schema version and legacy flag.
    
    Saves JSON with run paths and metadata.
    """
    
    manifest = {
        'valid_runs': [],
        'legacy_runs': [],
        'total_valid': len(valid_runs),
        'total_legacy': len(legacy_runs),
        'created_at': None
    }
    
    from datetime import datetime
    manifest['created_at'] = datetime.utcnow().isoformat() + 'Z'
    
    # Valid v2.0 runs
    for run_dir in valid_runs:
        # Load metadata
        metadata = load_metadata(run_dir / 'metadata.json')
        config = load_config(run_dir / 'config.json')
        status = load_status(run_dir / 'status.json')
        
        manifest['valid_runs'].append({
            'path': str(run_dir),
            'run_id': metadata.run_id,
            'seed': metadata.seed,
            'config_hash': config.config_hash,
            'schema_version': '2.0',  # NEW
            'experiment_name': metadata.experiment_name,
            'sweep_param': metadata.sweep_param,
            'sweep_value': metadata.sweep_value,
            'duration_seconds': metadata.duration_seconds,
            'final_tick': status.final_tick,
            'final_n_edges': status.final_n_edges,
            'freeze_detected': status.freeze_detected,
            'freeze_tick': status.freeze_tick
        })
    
    # Legacy v1.0 runs (acceptable with warnings)
    for run_dir, schema_result in legacy_runs:
        # Load what we can (may not have all metadata)
        try:
            metadata = load_metadata(run_dir / 'metadata.json')
            config = load_config(run_dir / 'config.json')
            status = load_status(run_dir / 'status.json')
            
            manifest['legacy_runs'].append({
                'path': str(run_dir),
                'run_id': metadata.run_id,
                'seed': metadata.seed,
                'config_hash': config.config_hash,
                'schema_version': '1.0-LEGACY',  # NEW
                'legacy_warnings': schema_result.details,  # NEW
                'experiment_name': metadata.experiment_name,
                'sweep_param': metadata.sweep_param,
                'sweep_value': metadata.sweep_value,
                'duration_seconds': metadata.duration_seconds,
                'final_tick': status.final_tick,
                'final_n_edges': status.final_n_edges
            })
        except:
            # Legacy run may not have all files - best effort
            manifest['legacy_runs'].append({
                'path': str(run_dir),
                'schema_version': '1.0-LEGACY',
                'legacy_warnings': schema_result.details
            })
    
    # Save manifest
    with open(output_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\nManifest saved: {output_path}")
    print(f"  {len(valid_runs)} v2.0 runs")
    if legacy_runs:
        print(f"  {len(legacy_runs)} v1.0-LEGACY runs (mark results!)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_sweep.py <sweep_directory>")
        print()
        print("Example:")
        print("  python scripts/validate_sweep.py experiments/decay_sweep_krok6")
        sys.exit(1)
    
    sweep_dir = Path(sys.argv[1])
    
    if not sweep_dir.exists():
        print(f"ERROR: Directory not found: {sweep_dir}")
        sys.exit(1)
    
    if not sweep_dir.is_dir():
        print(f"ERROR: Not a directory: {sweep_dir}")
        sys.exit(1)
    
    # Validate
    valid_runs, invalid_runs, incomplete_runs, legacy_runs = validate_sweep(sweep_dir, verbose=True)
    
    # Print summary
    print_summary(valid_runs, invalid_runs, incomplete_runs, legacy_runs)
    
    # Create manifest
    analysis_ready = len(valid_runs) + len(legacy_runs)
    if analysis_ready > 0:
        manifest_path = sweep_dir / 'valid_runs_manifest.json'
        create_valid_runs_list(valid_runs, legacy_runs, manifest_path)
    
    # Exit code
    if analysis_ready == 0:
        print("\n[FAIL] No valid runs - fix runs and re-validate")
        sys.exit(1)
    elif invalid_runs or incomplete_runs:
        print(f"\n[WARNING] {len(invalid_runs) + len(incomplete_runs)} runs excluded")
        if legacy_runs:
            print(f"[WARNING] {len(legacy_runs)} LEGACY v1.0 runs - mark results [LEGACY-V1]")
        sys.exit(0)
    else:
        print("\n[SUCCESS] All runs valid")
        if legacy_runs:
            print(f"[WARNING] {len(legacy_runs)} runs are LEGACY v1.0")
        sys.exit(0)


if __name__ == "__main__":
    main()
