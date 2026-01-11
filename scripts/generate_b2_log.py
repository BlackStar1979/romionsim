#!/usr/bin/env python3
"""
Generate schema v2.0 log for Phase B.2 testing.
"""

import sys
sys.path.insert(0, 'C:\\Work\\romionsim')

from core.graph import Graph
from core.engine import CoreEngine
from core.log import JSONLogger

# Parameters (decay=0.7, active regime from Phase B Exp 3)
params = {
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
    'enable_field_tail': False,
    'decay': 0.0056  # decay_scale=0.7 → decay=0.008*0.7=0.0056
}

# Initialize
n_nodes = 1000
n_edges_init = 3000
seed = 42

G = Graph(n_nodes, n_edges_init, seed=seed)
engine = CoreEngine(G, params)
logger = JSONLogger('C:\\Work\\romionsim\\results\\phase_b2_v2\\simulation.jsonl', schema_version='2.0')

# Metadata
logger.log_metadata(params, seed=seed, n_nodes=n_nodes, n_edges_init=n_edges_init)

# Run 500 ticks
for i in range(500):
    stats = engine.tick()
    
    # STATE every 50 ticks + final
    if i % 50 == 0 or i == 499:
        logger.log_state(
            tick=stats['tick'],
            stats=stats,
            engine=engine,
            params=params
        )
    
    # GRAPH at tick 400
    if i == 399:
        logger.log_graph(tick=stats['tick'], graph=G)
    
    if i % 100 == 0:
        print(f"Tick {i}")

logger.close()
print("DONE: results/phase_b2_v2/simulation.jsonl")
