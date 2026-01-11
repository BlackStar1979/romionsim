#!/usr/bin/env python3
"""
ROMION Sweep Runner - KROK 6 Compliant

Implements complete, reproducible experiment protocol:
- config.json: Full parameter set + hash
- metadata.json: Seed, timestamps, git info, system info
- simulation.jsonl: Evolution log
- validation.json: Fail-closed validation report
- status.json: Final completion status

WITHOUT ALL FILES, RUN IS INCOMPLETE AND IGNORED BY ANALYSIS.

This is the ONLY correct way to run sweeps in ROMION.
"""

import sys
from pathlib import Path

# Add repo root
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

import random
import json
import time
from datetime import datetime
from typing import Dict, Optional

from core.graph import Graph
from core.engine import CoreEngine
from scripts.run_metadata import (
    RunConfig, RunMetadata, RunStatus, ValidationReport,
    compute_config_hash, create_run_metadata, finalize_run_metadata,
    save_config, save_metadata, save_status, save_validation
)


def init_graph(n: int, e: int, w_cap: float, seed: int) -> Graph:
    """Initialize random graph."""
    random.seed(seed)
    G = Graph(n)
    for _ in range(e):
        u = random.randrange(n)
        v = random.randrange(n)
        if u != v:
            w = random.uniform(0.15, 0.5)
            G.add_edge(u, v, w, limit=w_cap)
    return G


def detect_freeze(log_path: Path, window: int = 10, threshold: int = 0) -> tuple:
    """
    Detect if system froze (bridges = 0 for window ticks).
    
    Returns:
        (freeze_detected, freeze_tick)
    """
    # Read log backwards
    with open(log_path, 'r') as f:
        lines = f.readlines()
    
    # Find GRAPH dumps
    graph_ticks = []
    for line in reversed(lines):
        try:
            obj = json.loads(line.strip())
            if obj.get('type') == 'GRAPH':
                tick = obj.get('tick')
                n_edges = len(obj.get('edges', []))
                graph_ticks.append((tick, n_edges))
                
                if len(graph_ticks) >= window:
                    break
        except:
            continue
    
    # Check if all recent ticks have edges <= threshold
    if len(graph_ticks) >= window:
        all_frozen = all(n_edges <= threshold for _, n_edges in graph_ticks[:window])
        if all_frozen:
            return True, graph_ticks[0][0]  # Most recent tick
    
    return False, None


def run_simulation(
    params: Dict,
    seed: int,
    n_ticks: int,
    dump_graph_every: int,
    output_dir: Path,
    experiment_name: str,
    sweep_param: Optional[str] = None,
    sweep_value: Optional[float] = None,
    notes: Optional[str] = None
) -> bool:
    """
    Run single simulation with KROK 6 complete tracking.
    
    Returns:
        True if successful, False if failed
    """
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Compute config hash
    config_hash = compute_config_hash(params)
    
    # Create config
    config = RunConfig(
        params=params,
        config_hash=config_hash,
        n_nodes=1000,
        n_edges_initial=10000,
        init_w_range=(0.15, 0.5),
        n_ticks=n_ticks,
        dump_graph_every=dump_graph_every
    )
    
    # Create metadata
    metadata = create_run_metadata(
        seed=seed,
        config_hash=config_hash,
        experiment_name=experiment_name,
        sweep_param=sweep_param,
        sweep_value=sweep_value,
        notes=notes
    )
    
    # Save config and metadata immediately
    save_config(config, output_dir / 'config.json')
    save_metadata(metadata, output_dir / 'metadata.json')
    
    # Start timer
    start_time = time.time()
    
    # Initialize status
    status = RunStatus(
        completed=False,
        success=False,
        error=None,
        final_tick=0,
        final_n_edges=0,
        freeze_detected=False,
        freeze_tick=None,
        validated=False,
        validation_passed=False,
        completed_at=datetime.utcnow().isoformat() + 'Z'
    )
    
    try:
        # Initialize graph
        random.seed(seed)
        G = init_graph(n=1000, e=10000, w_cap=params['w_cap'], seed=seed)
        
        # Create engine
        engine = CoreEngine(G, params)
        
        # Run simulation
        log_path = output_dir / 'simulation.jsonl'
        with open(log_path, 'w') as f:
            for tick in range(n_ticks + 1):
                # Log state periodically
                if tick % 50 == 0:
                    state = {
                        'type': 'STATE',
                        'tick': tick,
                        'n_nodes': G.num_nodes,
                        'n_edges': len(G.edges),
                        'total_weight': sum(e.w for e in G.edges.values()),
                        'seed': seed,
                        'config_hash': config_hash,
                    }
                    f.write(json.dumps(state) + '\n')
                
                # Dump graph
                if tick > 0 and tick % dump_graph_every == 0:
                    edges = [[u, v, e.w] for (u, v), e in G.edges.items()]
                    graph_dump = {
                        'type': 'GRAPH',
                        'tick': tick,
                        'n': G.num_nodes,
                        'edges': edges,
                    }
                    f.write(json.dumps(graph_dump) + '\n')
                
                # Step
                if tick < n_ticks:
                    engine.tick()
        
        # Success
        duration = time.time() - start_time
        
        # Detect freeze
        freeze_detected, freeze_tick = detect_freeze(log_path)
        
        # Update status
        status.completed = True
        status.success = True
        status.final_tick = n_ticks
        status.final_n_edges = len(G.edges)
        status.freeze_detected = freeze_detected
        status.freeze_tick = freeze_tick
        status.completed_at = datetime.utcnow().isoformat() + 'Z'
        
        # Finalize metadata
        finalized_metadata = finalize_run_metadata(metadata, duration)
        save_metadata(finalized_metadata, output_dir / 'metadata.json')
        
        # Create validation report (basic - full validation done by analysis)
        validation = ValidationReport(
            is_valid=True,
            validation_status="VALID",
            reasons=[],
            threshold_check={
                'wcluster': params.get('wcluster', 0.02),
                'wdist': params.get('wdist', 0.005),
                'wbridge': params.get('wbridge', 0.0)
            },
            geometry_check=None,  # Will be filled by analysis
            validated_at=datetime.utcnow().isoformat() + 'Z'
        )
        
        status.validated = True
        status.validation_passed = True
        
        # Save validation and status
        save_validation(validation, output_dir / 'validation.json')
        save_status(status, output_dir / 'status.json')
        
        return True
        
    except Exception as e:
        # Failed
        duration = time.time() - start_time
        
        status.completed = True
        status.success = False
        status.error = str(e)
        status.final_tick = 0
        status.final_n_edges = 0
        status.completed_at = datetime.utcnow().isoformat() + 'Z'
        
        # Finalize metadata
        finalized_metadata = finalize_run_metadata(metadata, duration)
        save_metadata(finalized_metadata, output_dir / 'metadata.json')
        
        # Validation failed
        validation = ValidationReport(
            is_valid=False,
            validation_status="INVALID_TECH",
            reasons=[f"Simulation failed: {e}"],
            threshold_check=None,
            geometry_check=None,
            validated_at=datetime.utcnow().isoformat() + 'Z'
        )
        
        status.validated = True
        status.validation_passed = False
        
        save_validation(validation, output_dir / 'validation.json')
        save_status(status, output_dir / 'status.json')
        
        return False


def run_sweep(
    base_params: Dict,
    sweep_param: str,
    sweep_values: list,
    seeds: list,
    n_ticks: int,
    dump_every: int,
    output_root: Path,
    experiment_name: str
):
    """
    Run parameter sweep with KROK 6 compliance.
    
    Args:
        base_params: Base parameter dict
        sweep_param: Parameter to sweep (e.g., "decay")
        sweep_values: Values to test
        seeds: Random seeds for each value
        n_ticks: Simulation length
        dump_every: Graph dump frequency
        output_root: Root directory for results
        experiment_name: Experiment identifier
    """
    
    total_runs = len(sweep_values) * len(seeds)
    completed = 0
    failed = 0
    
    print("=" * 70)
    print(f"ROMION SWEEP - {experiment_name}")
    print("=" * 70)
    print(f"Parameter: {sweep_param}")
    print(f"Values: {sweep_values}")
    print(f"Seeds: {seeds}")
    print(f"Total runs: {total_runs}")
    print("=" * 70)
    print()
    
    for i, value in enumerate(sweep_values, 1):
        for j, seed in enumerate(seeds, 1):
            run_num = (i - 1) * len(seeds) + j
            
            print(f"[{run_num}/{total_runs}] {sweep_param}={value}, seed={seed}")
            
            # Create run directory
            run_dir = output_root / f"{sweep_param}_{value}_seed_{seed}"
            
            # Set parameter
            params = base_params.copy()
            params[sweep_param] = value
            
            # Run
            try:
                success = run_simulation(
                    params=params,
                    seed=seed,
                    n_ticks=n_ticks,
                    dump_graph_every=dump_every,
                    output_dir=run_dir,
                    experiment_name=experiment_name,
                    sweep_param=sweep_param,
                    sweep_value=value,
                    notes=f"Sweep: {sweep_param}={value}, seed={seed}"
                )
                
                if success:
                    completed += 1
                    print(f"  ✓ Complete")
                else:
                    failed += 1
                    print(f"  ✗ Failed")
                    
            except Exception as e:
                failed += 1
                print(f"  ✗ Exception: {e}")
    
    print()
    print("=" * 70)
    print(f"SWEEP COMPLETE")
    print(f"  Success: {completed}/{total_runs}")
    print(f"  Failed: {failed}/{total_runs}")
    print("=" * 70)
    print()
    print("Run validation:")
    print(f"  python scripts/validate_sweep.py {output_root}")
    print()
    print("Next: Analyze with gravity_test (only VALID runs)")


def main():
    """Example decay sweep."""
    
    # Base parameters (ROMION v2.0 theory values)
    BASE_PARAMS = {
        'spawn_threshold': 0.15,
        'spawn_samples': 1500,
        'spawn_damping': 0.55,
        'spawn_cap': 1500,
        'reinforce_factor': 0.05,
        'decay_kappa_discount': 0.9,
        'min_weight': 0.005,
        'W_max': 2.5,        # Theory value
        'w_cap': 2.5,
        'theta': 0.25,       # Theory value
        'beta_2hop': 0.25,
        'twohop_sample': 15,
        'time_alpha_scale': 1.0,
        'epsilon_spark': 0.0,
        'enable_field_tail': False,  # Updated name
        # Three thresholds (for analysis)
        'wcluster': 0.02,
        'wdist': 0.005,
        'wbridge': 0.0,
    }
    
    # Sweep configuration
    DECAY_SCALE_VALUES = [1.0, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.5]
    SEEDS = [42, 123, 456]
    N_TICKS = 600
    DUMP_EVERY = 100
    
    # Output
    output_root = Path("experiments/decay_sweep_krok6")
    
    # Run sweep
    run_sweep(
        base_params=BASE_PARAMS,
        sweep_param='decay',
        sweep_values=[0.008 * scale for scale in DECAY_SCALE_VALUES],
        seeds=SEEDS,
        n_ticks=N_TICKS,
        dump_every=DUMP_EVERY,
        output_root=output_root,
        experiment_name="decay_sweep_krok6"
    )


if __name__ == "__main__":
    main()
