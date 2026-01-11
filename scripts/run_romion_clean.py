#!/usr/bin/env python3
"""
ROMION Clean Simulation Runner

Theory-driven implementation with:
- Explicit parameter control
- Quantum Spark DISABLED by default
- Phase control via spawn/decay scales
- Clean output structure

Usage:
    python run_romion_clean.py                          # baseline
    python run_romion_clean.py --ticks 2000             # longer run
    python run_romion_clean.py --spawn-scale 1.2        # phase control
    python run_romion_clean.py --enable-spark --epsilon-spark 0.002  # WARNING: needs S2 derivation!
"""

import random
import json
import time
import argparse
import os
from pathlib import Path

from core.graph import Graph
from core.engine import CoreEngine


# =====================
# BASE PARAMETERS
# =====================
# These values need theoretical justification (see IMPLEMENTATION_AUDIT.md)
BASE_PARAMS = {
    # S1 (Closure) parameters
    'spawn_threshold': 0.15,      # Min κ for spawning (= θ projection threshold?)
    'spawn_samples': 1500,        # Sample size (pragmatic optimization)
    'spawn_damping': 0.55,        # α₁ from S1 - TODO: derive from theory
    'spawn_cap': 1500,            # Max new edges per tick (safety)
    'reinforce_factor': 0.05,     # Resonance boost - TODO: justify
    
    # Propagate parameters
    'decay': 0.008,               # Base decay rate - TODO: relate to exp(-λ·Frust)
    'decay_kappa_discount': 0.9,  # κ protection factor
    'min_weight': 0.005,          # Vacuum threshold
    
    # Normalize parameters
    'W_max': 2.5,                 # Event horizon pressure - TODO: derive
    'w_cap': 2.5,                 # Hard weight limit (same as W_max for consistency)
    
    # Metrics parameters
    'theta': 0.25,                # FRACTURE projection threshold (theoretical)
    'beta_2hop': 0.25,            # 2-hop path weight - TODO: justify
    'twohop_sample': 15,          # 2-hop sample limit (pragmatic)
    'time_alpha_scale': 1.0,      # Emergent time scale factor
    
    # Quantum Spark - DISABLED BY DEFAULT
    # Requires derivation from S2 (Antipair): ε = P(w'(e†) > w_min | Frust >> 1)
    'epsilon_spark': 0.0,         # Spark probability (OFF)
    'spark_w': 0.0,               # Spark strength (OFF)
}

SEED = 42


def init_graph(n: int = 2000, e: int = 6000, params: dict = None) -> Graph:
    """
    Initialize graph with random edges (cold start).
    
    Args:
        n: Number of nodes
        e: Initial number of edges
        params: Parameter dict for w_cap
        
    Returns:
        Initialized Graph
    """
    if params is None:
        params = BASE_PARAMS
        
    G = Graph(n)
    w_cap = params.get("W_max", 2.5)
    
    for _ in range(e):
        u = random.randrange(n)
        v = random.randrange(n)
        if u != v:
            w = random.uniform(0.15, 0.5)
            G.add_edge(u, v, w, limit=w_cap)
            
    return G


def run_simulation(args):
    """Execute simulation with given arguments."""
    # Setup output directory
    out_dir = Path(args.out)
    out_dir.mkdir(exist_ok=True, parents=True)
    
    # Random seed
    random.seed(SEED)
    
    # Build parameters
    params = dict(BASE_PARAMS)
    
    # Phase control (theory-driven parameter scaling)
    if hasattr(args, 'spawn_scale') and args.spawn_scale != 1.0:
        params['spawn_damping'] *= args.spawn_scale
        params['reinforce_factor'] *= args.spawn_scale
        print(f"Phase control: spawn_scale = {args.spawn_scale}")
        
    if hasattr(args, 'decay_scale') and args.decay_scale != 1.0:
        params['decay'] *= args.decay_scale
        print(f"Phase control: decay_scale = {args.decay_scale}")
    
    # Quantum Spark control (DISABLED unless explicitly enabled)
    if args.enable_spark:
        print("WARNING: Quantum Spark ENABLED")
        print("This feature requires theoretical derivation from S2!")
        print("See IMPLEMENTATION_AUDIT.md for details")
        params['epsilon_spark'] = args.epsilon_spark
        params['spark_w'] = 0.08
    
    # Initialize
    print(f"Initializing graph (N={args.nodes}, E={args.init_edges})...")
    G = init_graph(args.nodes, args.init_edges, params)
    engine = CoreEngine(G, params)
    
    # Output file
    log_path = out_dir / "simulation.jsonl"
    print(f"Logging to: {log_path}")
    
    # Header
    print(f"{'TICK':<6} | {'EDGES':<7} | {'VIS%':<6} | {'κ':<6} | {'P':<6} | {'NEW':<5} | {'REF':<5} | {'RMV':<4}")
    print("-" * 75)
    
    start_time = time.time()
    
    with open(log_path, 'w') as f:
        # Write parameters
        meta = {"type": "PARAMS", "seed": SEED, "data": params}
        f.write(json.dumps(meta) + "\n")
        
        # Evolution loop
        for t in range(1, args.ticks + 1):
            stats = engine.tick()
            f.write(json.dumps({"type": "STATS", "data": stats}) + "\n")
            
            # Progress output
            if t % args.log_interval == 0:
                vis_pct = stats['visible_ratio'] * 100
                print(
                    f"{stats['tick']:<6} | {stats['total_edges']:<7} | "
                    f"{vis_pct:5.1f}% | {stats['mean_kappa']:5.3f} | "
                    f"{stats['mean_pressure']:5.2f} | {stats['spawn_new']:<5} | "
                    f"{stats['spawn_reinf']:<5} | {stats['removed']:<4}"
                )
    
    duration = time.time() - start_time
    print("-" * 75)
    print(f"Simulation complete in {duration:.2f}s")
    print(f"Final state: {stats['total_edges']} edges, {stats['visible_edges']} visible")


def main():
    parser = argparse.ArgumentParser(
        description='ROMION Clean Simulation',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Simulation parameters
    parser.add_argument('--ticks', type=int, default=1000,
                        help='Number of simulation ticks')
    parser.add_argument('--nodes', type=int, default=2000,
                        help='Number of nodes')
    parser.add_argument('--init-edges', type=int, default=6000,
                        help='Initial number of edges')
    
    # Output control
    parser.add_argument('--out', default='.',
                        help='Output directory')
    parser.add_argument('--log-interval', type=int, default=50,
                        help='Print stats every N ticks')
    
    # Phase control (theory-driven parameter scaling)
    parser.add_argument('--spawn-scale', type=float, default=1.0,
                        help='Scale spawn parameters (>1 = more creation)')
    parser.add_argument('--decay-scale', type=float, default=1.0,
                        help='Scale decay rate (>1 = faster decay)')
    
    # Quantum Spark control (DISABLED by default)
    parser.add_argument('--enable-spark', action='store_true',
                        help='Enable Quantum Spark (WARNING: requires S2 derivation!)')
    parser.add_argument('--epsilon-spark', type=float, default=0.002,
                        help='Spark probability (only if --enable-spark)')
    
    args = parser.parse_args()
    
    # Validation
    if args.enable_spark:
        print()
        print("=" * 75)
        print("WARNING: You are enabling Quantum Spark")
        print("This feature is currently a MAGIC FEATURE")
        print("It must be theoretically derived from S2 (Antipair rule)")
        print("See: C:\\Work\\romion\\IMPLEMENTATION_AUDIT.md")
        print("=" * 75)
        print()
        response = input("Continue anyway? [y/N]: ")
        if response.lower() != 'y':
            print("Aborting. Good choice!")
            return
    
    run_simulation(args)


if __name__ == "__main__":
    main()
