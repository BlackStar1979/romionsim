#!/usr/bin/env python3
"""
ROMION Runner with Frustration Logging

Enables frustration data collection for Quantum Spark verification.

Usage:
    python run_with_frustration.py --ticks 1000 --frust-every 100

Output:
    simulation.jsonl with {"type":"FRUST","tick":t,"frust":[[u,v,f], ...]}
    
Then analyze:
    python analysis/verify_spark.py --log simulation.jsonl
"""

import random
import json
import time
import argparse
from pathlib import Path

from core.graph import Graph
from core.engine import CoreEngine
from core.metrics import compute_frustration


BASE_PARAMS = {
    'spawn_threshold': 0.15,
    'spawn_samples': 1500,
    'spawn_damping': 0.55,
    'spawn_cap': 1500,
    'reinforce_factor': 0.05,
    'decay': 0.008,
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
}

SEED = 42


def init_graph(n: int, e: int, w_cap: float) -> Graph:
    """Initialize random graph."""
    G = Graph(n)
    for _ in range(e):
        u = random.randrange(n)
        v = random.randrange(n)
        if u != v:
            w = random.uniform(0.15, 0.5)
            G.add_edge(u, v, w, limit=w_cap)
    return G


def dump_frustration(f, tick: int, G: Graph, pressure_map: dict, params: dict):
    """Dump frustration data for all edges."""
    frust_data = compute_frustration(G, pressure_map, params)
    frust_list = [
        [u, v, frust]
        for (u, v), frust in frust_data["frustration_map"].items()
    ]
    
    f.write(json.dumps({
        "type": "FRUST",
        "tick": tick,
        "frust": frust_list,
        "mean": frust_data["mean_frust"],
        "max": frust_data["max_frust"]
    }) + "\n")


def main():
    ap = argparse.ArgumentParser(
        description='ROMION with Frustration Logging',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    ap.add_argument('--ticks', type=int, default=1000)
    ap.add_argument('--nodes', type=int, default=2000)
    ap.add_argument('--init-edges', type=int, default=6000)
    ap.add_argument('--out', default='.')
    ap.add_argument('--log-interval', type=int, default=50)
    
    ap.add_argument('--frust-every', type=int, default=0,
                    help='Log frustration every N ticks (0=disabled)')
    
    ap.add_argument('--spawn-scale', type=float, default=1.0)
    ap.add_argument('--decay-scale', type=float, default=1.0)
    
    ap.add_argument('--enable-spark', action='store_true')
    ap.add_argument('--epsilon-spark', type=float, default=0.002)
    
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    random.seed(SEED)

    params = dict(BASE_PARAMS)
    params['spawn_damping'] *= args.spawn_scale
    params['reinforce_factor'] *= args.spawn_scale
    params['decay'] *= args.decay_scale

    if args.enable_spark:
        print("WARNING: Quantum Spark ENABLED for verification")
        params['epsilon_spark'] = args.epsilon_spark
        params['spark_w'] = 0.08

    G = init_graph(args.nodes, args.init_edges, params['w_cap'])
    engine = CoreEngine(G, params)

    log_path = out_dir / "simulation.jsonl"
    print(f"Logging to: {log_path}")
    
    if args.frust_every:
        print(f"Frustration logging every {args.frust_every} ticks")
        print("Use: python analysis/verify_spark.py --log simulation.jsonl")

    print(f"{'TICK':<6} | {'EDGES':<7} | {'VIS%':<6} | {'κ':<6} | {'P':<6} | {'FRUST':<8}")
    print("-" * 70)

    start = time.time()

    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps({"type": "PARAMS", "seed": SEED, "data": params}) + "\n")

        for t in range(1, args.ticks + 1):
            stats = engine.tick()
            f.write(json.dumps({"type": "STATS", "data": stats}) + "\n")

            # Frustration dump
            if args.frust_every and (t % args.frust_every == 0):
                # Re-compute pressure for frustration calculation
                pressure_map = {
                    u: sum(e.w for e in engine.G.adj[u].values())
                    for u in range(engine.G.num_nodes)
                }
                dump_frustration(f, t, engine.G, pressure_map, params)

            # Progress
            if t % args.log_interval == 0:
                vis_pct = stats['visible_ratio'] * 100
                frust_str = ""
                if args.frust_every and (t % args.frust_every == 0):
                    frust_str = "LOGGED"
                
                print(
                    f"{stats['tick']:<6} | {stats['total_edges']:<7} | "
                    f"{vis_pct:5.1f}% | {stats['mean_kappa']:5.3f} | "
                    f"{stats['mean_pressure']:5.2f} | {frust_str:<8}"
                )

    dur = time.time() - start
    print("-" * 70)
    print(f"Simulation complete in {dur:.2f}s")
    
    if args.frust_every:
        print()
        print("Next step:")
        print(f"  python analysis/verify_spark.py --log {log_path}")


if __name__ == "__main__":
    main()
