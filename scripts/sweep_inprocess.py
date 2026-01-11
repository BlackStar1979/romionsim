#!/usr/bin/env python3
"""
In-process decay sweep - NO subprocess, NO import issues.
Runs simulations directly in Python process.
"""

import sys
from pathlib import Path

# Add repo root ONCE at start
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

import random
import json
import csv
from core.graph import Graph
from core.engine import CoreEngine

# Sweep config
DECAY_POINTS = [1.0, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.5]
SEEDS = [42, 123]
TICKS = 600
DUMP_EVERY = 100

BASE_PARAMS = {
    'spawn_threshold': 0.15,
    'spawn_samples': 1500,
    'spawn_damping': 0.55,
    'spawn_cap': 1500,
    'reinforce_factor': 0.05,
    'decay_kappa_discount': 0.9,
    'min_weight': 0.005,
    'W_max': 2.5,
    'w_cap': 2.5,
    'theta': 0.25,
    'beta_2hop': 0.25,
    'twohop_sample': 15,
    'time_alpha_scale': 1.0,
    'epsilon_spark': 0.0,
    'spark_w': 0.0,
    'enable_s2_tail': False,
}


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


def run_simulation(decay_scale: float, seed: int, output_dir: Path) -> bool:
    """Run one simulation point."""
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "simulation.jsonl"
    
    print(f"  Running decay={decay_scale}, seed={seed}")
    
    # Set seed
    random.seed(seed)
    
    # Init graph
    G = init_graph(n=1000, e=10000, w_cap=BASE_PARAMS['w_cap'], seed=seed)
    
    # Set decay parameter
    params = BASE_PARAMS.copy()
    params['decay'] = 0.008 * decay_scale
    
    # Create engine
    engine = CoreEngine(G, params)
    
    # Run simulation
    with open(log_path, 'w') as f:
        for tick in range(TICKS + 1):
            # Log state
            if tick % 50 == 0:
                state = {
                    'type': 'STATE',
                    'tick': tick,
                    'n_nodes': G.num_nodes,
                    'n_edges': len(G.edges),
                    'total_weight': sum(e.w for e in G.edges.values()),
                    'params': params,
                }
                f.write(json.dumps(state) + '\n')
            
            # Dump graph
            if tick > 0 and tick % DUMP_EVERY == 0:
                edges = [[u, v, e.w] for (u, v), e in G.edges.items()]
                graph_dump = {
                    'type': 'GRAPH',
                    'tick': tick,
                    'edges': edges,
                }
                f.write(json.dumps(graph_dump) + '\n')
            
            # Step
            if tick < TICKS:
                engine.tick()
    
    print(f"    OK Complete: {len(G.edges)} edges @ tick {TICKS}")
    return True


def main():
    results_dir = Path("tests/sweep_decay_inprocess/results")
    
    total = len(DECAY_POINTS) * len(SEEDS)
    completed = 0
    
    print("=" * 70)
    print(f"IN-PROCESS DECAY SWEEP: {total} runs")
    print("=" * 70)
    
    for i, decay in enumerate(DECAY_POINTS, 1):
        for j, seed in enumerate(SEEDS, 1):
            run_num = (i-1) * len(SEEDS) + j
            print(f"\n[{run_num}/{total}] decay={decay}, seed={seed}")
            
            output_dir = results_dir / f"d{decay}_s{seed}"
            
            try:
                if run_simulation(decay, seed, output_dir):
                    completed += 1
            except Exception as e:
                print(f"    X ERROR: {e}")
    
    print("\n" + "=" * 70)
    print(f"SWEEP COMPLETE: {completed}/{total} runs")
    print("=" * 70)
    
    if completed > 0:
        print("\nNext step: Analyze results with gravity_test.py")
        print("  python analysis/gravity_test.py --log <log> --tick 400 --channels --anisotropy")


if __name__ == "__main__":
    main()
