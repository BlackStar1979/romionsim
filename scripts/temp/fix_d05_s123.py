#!/usr/bin/env python3
"""
Re-run single incomplete simulation: d0.5_s123
"""

import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

import random
import json
from core.graph import Graph
from core.engine import CoreEngine

# Parameters for d0.5_s123
DECAY_SCALE = 0.5
SEED = 123
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

def main():
    output_dir = Path("tests/sweep_decay_inprocess/results/d0.5_s123")
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "simulation.jsonl"
    
    print(f"Re-running decay={DECAY_SCALE}, seed={SEED}")
    print(f"Output: {log_path}")
    
    # Set seed
    random.seed(SEED)
    
    # Init graph
    G = init_graph(n=1000, e=10000, w_cap=BASE_PARAMS['w_cap'], seed=SEED)
    
    # Set decay parameter
    params = BASE_PARAMS.copy()
    params['decay'] = 0.008 * DECAY_SCALE
    
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
                f.flush()  # Force write
                
                if tick % 100 == 0:
                    print(f"  tick {tick}: {len(G.edges)} edges")
            
            # Dump graph
            if tick > 0 and tick % DUMP_EVERY == 0:
                edges = [[u, v, e.w] for (u, v), e in G.edges.items()]
                graph_dump = {
                    'type': 'GRAPH',
                    'tick': tick,
                    'edges': edges,
                }
                f.write(json.dumps(graph_dump) + '\n')
                f.flush()
            
            # Step
            if tick < TICKS:
                engine.tick()
    
    print(f"Complete: {len(G.edges)} edges @ tick {TICKS}")
    print(f"Log written: {log_path}")

if __name__ == "__main__":
    main()
