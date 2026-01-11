# romionsim/core/engine.py
"""
Main evolution engine for ROMION simulation.

Implements evolution operator U:
U = Normalize ∘ Propagate ∘ Spawn ∘ Metrics

Each tick represents one Planck step.
"""

from .metrics import compute_metrics
from .rules import rule_spawn, rule_propagate, rule_normalize


class CoreEngine:
    """
    ROMION evolution engine.
    
    Manages:
    - Graph evolution via spawn/propagate/normalize rules
    - Observable computation (tension, emergent time)
    - State tracking across ticks
    """
    
    def __init__(self, graph, params: dict):
        """
        Initialize engine.
        
        Args:
            graph: Graph instance to evolve
            params: Configuration dict (see rules.py for details)
        """
        self.G = graph
        self.params = params
        self.n = 0  # Current tick
        
        # Accumulated observables
        self.total_tension_map = {i: 0.0 for i in range(graph.num_nodes)}
        self.emergent_time = {i: 0.0 for i in range(graph.num_nodes)}

    def tick(self) -> dict:
        """
        Execute one Planck step.
        
        Evolution sequence:
        1. Metrics: Compute κ (decision-making info for this tick)
        2. Spawn: Create/reinforce shortcuts (S1)
        3. Propagate: Decay weak edges
        4. Re-calculate pressure: Physics changed weights
        5. Normalize: Clamp pressure, extract tension
        6. Update observables: Tension and emergent time
        
        Returns:
            Dict with statistics:
                - tick: Current tick number
                - spawn_new: New edges created
                - spawn_reinf: Edges reinforced
                - removed: Edges decayed
                - norm_ops: Normalization operations
                - tension_step: Tension this tick
                - max_acc_tension: Maximum accumulated tension
                - visible_edges: Edges with κ ≥ θ
                - visible_ratio: Fraction visible
                - total_edges: Total edges in CORE
                - mean_pressure: Average pressure
                - mean_kappa: Average κ
        """
        self.n += 1
        
        # 1. FULL METRICS (once per tick - at start)
        # Compute κ which serves as decision info for this tick
        metrics = compute_metrics(self.G, self.params)
        
        # 2. PHYSICS (topology and weight changes)
        spawn_new, spawn_reinf = rule_spawn(self.G, self.params)
        removed = rule_propagate(self.G, self.params)
        
        # 3. LIGHT PRESSURE RE-CALCULATION
        # Physics changed weights, so pressure changed
        # Fast sum so Normalization sees current state
        current_pressure_map = {
            u: sum(e.w for e in self.G.adj[u].values())
            for u in range(self.G.num_nodes)
        }
        
        # 4. NORMALIZATION (Event Horizon)
        # If pressure exceeds W_max, cut weights
        norm_ops, step_tension = rule_normalize(
            self.G, current_pressure_map, self.params
        )
        
        # 5. TIME AND TENSION (Observables)
        global_tension_step = 0.0
        w_max = self.params.get('W_max', 5.0)
        time_alpha = self.params.get('time_alpha_scale', 1.0) / w_max
        
        for u in range(self.G.num_nodes):
            # Tension accumulation (candidate for mass)
            t_val = step_tension.get(u, 0.0)
            if t_val > 0:
                self.total_tension_map[u] += t_val
                global_tension_step += t_val
            
            # Emergent Time: Lags with pressure increase (Gravity)
            p = current_pressure_map[u]
            dt = 1.0 / (1.0 + time_alpha * p)
            self.emergent_time[u] += dt

        # 6. FINAL STATISTICS (for logs)
        theta = self.params.get('theta', 0.5)
        
        # Visibility based on κ from start of tick (decision-making)
        visible_edges = sum(
            1 for e in self.G.all_edges() if e.kappa_cache >= theta
        )
        
        final_total_p = sum(current_pressure_map.values())
        final_mean_p = final_total_p / max(1, self.G.num_nodes)
        
        max_acc_tension = (
            max(self.total_tension_map.values())
            if self.G.num_nodes > 0
            else 0.0
        )

        return {
            "tick": self.n,
            "spawn_new": spawn_new,
            "spawn_reinf": spawn_reinf,
            "removed": removed,
            "norm_ops": norm_ops,
            "tension_step": global_tension_step,
            "max_acc_tension": max_acc_tension,
            "visible_edges": visible_edges,
            "visible_ratio": visible_edges / max(1, len(self.G.edges)),
            "total_edges": len(self.G.edges),
            "mean_pressure": final_mean_p,
            "mean_kappa": metrics["mean_kappa"]
        }
