#!/usr/bin/env python3
"""
ROMION Extended Runner with Graph Dumps and Phase Control

Extensions:
- --dump-graph-every N: Saves graph snapshot (type=GRAPH) every N ticks
- --shock-*: Second wave of criticality (temporary parameter changes)
- --enable-s2-tail: Long-range weak bridges (S2-tail mechanism)

Warning: GRAPH dumps increase simulation.jsonl size significantly.

Format: {"type":"GRAPH","tick":t,"edges":[[u,v,w], ...]}
"""

# Add repo root to path so we can import core/
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import random
import json
import time
import argparse

from core.graph import Graph
from core.engine import CoreEngine


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
    
    # S2-tail defaults (DISABLED by default)
    'enable_s2_tail': False,
}

SEED = 42  # Default, overridable with --seed


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


def dump_graph(f, tick: int, G: Graph):
    """
    Dump current graph state to JSONL.
    
    ✅ FIXED: Properly access Edge dataclass attributes
    ChatGPT error: used .get() on dataclass (doesn't exist)
    """
    edges = []
    for (u, v), edge in G.edges.items():
        # ✅ CORRECT: edge is Edge dataclass, access .w directly
        edges.append([int(u), int(v), float(edge.w)])
    
    f.write(json.dumps({
        "type": "GRAPH",
        "tick": tick,
        "edges": edges
    }) + "\n")


def main():
    ap = argparse.ArgumentParser(
        description='ROMION Extended Simulation with Dumps',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Basic simulation
    ap.add_argument('--ticks', type=int, default=1000)
    ap.add_argument('--nodes', type=int, default=2000)
    ap.add_argument('--init-edges', type=int, default=6000)
    ap.add_argument('--out', default='.')
    ap.add_argument('--log-interval', type=int, default=50)
    ap.add_argument('--seed', type=int, default=42, help='Random seed')

    # Phase control
    ap.add_argument('--spawn-scale', type=float, default=1.0,
                    help='Scale spawn parameters')
    ap.add_argument('--decay-scale', type=float, default=1.0,
                    help='Scale decay rate')
    ap.add_argument('--tension-scale', type=float, default=1.0,
                    help='Scale tension parameters (theta, beta)')

    # Quantum Spark
    ap.add_argument('--enable-spark', action='store_true')
    ap.add_argument('--epsilon-spark', type=float, default=0.002)
    ap.add_argument('--spark-w', type=float, default=0.08)

    # Graph dumps
    ap.add_argument('--dump-graph-every', type=int, default=0,
                    help='Dump graph every N ticks (0=disabled)')

    # Shock parameters (second wave)
    ap.add_argument('--shock-tick', type=int, default=None,
                    help='Start shock at this tick')
    ap.add_argument('--shock-len', type=int, default=0,
                    help='Shock duration in ticks')
    ap.add_argument('--shock-spawn', type=float, default=1.0,
                    help='Spawn multiplier during shock')
    ap.add_argument('--shock-decay', type=float, default=1.0,
                    help='Decay multiplier during shock')
    
    # S2-tail parameters (long-range field)
    ap.add_argument('--enable-s2-tail', action='store_true',
                    help='Enable S2-tail (weak long-range bridges)')
    ap.add_argument('--tail-samples', type=int, default=200,
                    help='Candidate pairs per tick for S2-tail')
    ap.add_argument('--tail-base-rate', type=float, default=0.01,
                    help='Base acceptance probability for S2-tail')
    ap.add_argument('--lambda-dist', type=float, default=0.5,
                    help='Distance decay factor for S2-tail')
    ap.add_argument('--tail-w', type=float, default=0.008,
                    help='Bridge weight for S2-tail (must be < wcluster)')
    ap.add_argument('--frust-x0', type=float, default=0.5,
                    help='Frustration threshold for S2-tail')
    ap.add_argument('--wcluster', type=float, default=0.02,
                    help='Cluster threshold (for S2-tail and gravity_test)')
    ap.add_argument('--wdist', type=float, default=0.005,
                    help='Background graph threshold (for S2-tail distance)')
    
    args = ap.parse_args()

    # Setup
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Use seed from args
    seed = args.seed
    random.seed(seed)

    # Build parameters
    params = dict(BASE_PARAMS)
    
    # Apply base scales
    params['spawn_damping'] *= args.spawn_scale
    params['reinforce_factor'] *= args.spawn_scale
    params['decay'] *= args.decay_scale
    params['theta'] *= args.tension_scale
    params['beta_2hop'] *= args.tension_scale

    # Quantum Spark (optional)
    if args.enable_spark:
        print("WARNING: Quantum Spark ENABLED")
        params['epsilon_spark'] = args.epsilon_spark
        params['spark_w'] = args.spark_w

    # S2-tail (optional)
    if args.enable_s2_tail:
        print("WARNING: S2-tail ENABLED (long-range weak bridges)")
        params['enable_s2_tail'] = True
        params['tail_samples'] = args.tail_samples
        params['tail_base_rate'] = args.tail_base_rate
        params['lambda_dist'] = args.lambda_dist
        params['tail_w'] = args.tail_w
        params['frust_x0'] = args.frust_x0
        params['wcluster'] = args.wcluster
        params['wdist'] = args.wdist

    # Initialize
    G = init_graph(args.nodes, args.init_edges, params['w_cap'])
    engine = CoreEngine(G, params)

    # ✅ FIXED: Store original values ONCE for shock calculation
    # ChatGPT error: modified params in-place causing cumulative effect
    orig_spawn_damp = params['spawn_damping']
    orig_reinforce = params['reinforce_factor']
    orig_decay = params['decay']

    # Output
    log_path = out_dir / "simulation.jsonl"
    print(f"Logging to: {log_path}")
    
    if args.dump_graph_every:
        print(f"Graph dumps every {args.dump_graph_every} ticks")
        print("WARNING: This increases file size significantly")
    
    if args.shock_tick is not None:
        print(f"Shock wave: tick {args.shock_tick}, duration {args.shock_len}")
        print(f"  spawn_mul={args.shock_spawn}, decay_mul={args.shock_decay}")
    
    if args.enable_s2_tail:
        print(f"S2-tail: samples={args.tail_samples}, base_rate={args.tail_base_rate}, lambda={args.lambda_dist}")

    # Header
    print(f"{'TICK':<6} | {'EDGES':<7} | {'VIS%':<6} | {'kappa':<6} | {'P':<6} | {'NEW':<5} | {'REF':<5} | {'S2':<4} | {'RMV':<4}")
    print("-" * 85)

    start = time.time()

    with open(log_path, 'w', encoding='utf-8') as f:
        # Write parameters
        f.write(json.dumps({
            "type": "PARAMS",
            "seed": seed,
            "data": params
        }) + "\n")

        # Evolution loop
        for t in range(1, args.ticks + 1):
            # ✅ FIXED: Calculate multipliers from original values
            # Not from already-modified params
            spawn_mul = 1.0
            decay_mul = 1.0
            
            if args.shock_tick is not None and args.shock_len > 0:
                if args.shock_tick <= t < (args.shock_tick + args.shock_len):
                    spawn_mul = args.shock_spawn
                    decay_mul = args.shock_decay

            # Apply multipliers (from original, not cumulative)
            engine.params['spawn_damping'] = orig_spawn_damp * spawn_mul
            engine.params['reinforce_factor'] = orig_reinforce * spawn_mul
            engine.params['decay'] = orig_decay * decay_mul

            # Tick
            stats = engine.tick()
            f.write(json.dumps({"type": "STATS", "data": stats}) + "\n")

            # Graph dump (if enabled)
            if args.dump_graph_every and (t % args.dump_graph_every == 0):
                dump_graph(f, t, engine.G)

            # Progress
            if t % args.log_interval == 0:
                vis_pct = stats['visible_ratio'] * 100
                print(
                    f"{stats['tick']:<6} | {stats['total_edges']:<7} | "
                    f"{vis_pct:5.1f}% | {stats['mean_kappa']:5.3f} | "
                    f"{stats['mean_pressure']:5.2f} | {stats['spawn_new']:<5} | "
                    f"{stats['spawn_reinf']:<5} | {stats.get('s2_tail_added', 0):<4} | {stats['removed']:<4}"
                )

    dur = time.time() - start
    print("-" * 85)
    print(f"Simulation complete in {dur:.2f}s")


if __name__ == "__main__":
    main()
