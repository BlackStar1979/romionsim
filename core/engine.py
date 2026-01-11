# romionsim/core/engine.py
"""
Main evolution engine for ROMION simulation.

Implements evolution operator U:
U = Normalize ∘ Propagate ∘ Spawn ∘ Metrics

Each tick represents one Planck step.
"""

from .metrics import compute_metrics
from .rules import rule_spawn, rule_propagate, rule_normalize, rule_field_tail


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
        
        Evolution sequence (Schema v2 compliant):
        1. Metrics PRE: Compute κ (decision state - Layer 1 CORE)
        2. Spawn: Create/reinforce shortcuts (S1)
        3. Field-tail: Long-range weak bridges (if enabled)
        4. Propagate: Decay weak edges
        5. Re-calculate pressure: Physics changed weights
        6. Normalize: Clamp pressure, extract tension
        6b. Metrics POST: Re-compute κ (observation state - Layer 1 CORE)
        7. Update observables: Tension and emergent time
        8. Projection: Compute visibility (Layer 2 FRACTURE)
        
        CRITICAL: Projection uses POST-evolution κ, NOT PRE-evolution κ.
        This enforces temporal separation (no backreaction).
        
        Returns:
            Dict with statistics:
                - tick: Current tick number
                - spawn_new: New edges created (L1)
                - spawn_reinf: Edges reinforced (L1)
                - field_tail_added: Weak long-range bridges (L1)
                - removed: Edges decayed (L1)
                - norm_ops: Normalization operations (L1)
                - tension_step: Tension this tick (L1)
                - max_acc_tension: Maximum accumulated tension (L1)
                - visible_edges: Edges with κ_post ≥ θ (L2)
                - visible_ratio: Fraction visible (L2)
                - total_edges: Total edges in CORE (L1)
                - mean_pressure: Average pressure (L1)
                - mean_kappa_pre: Average κ before evolution (L1)
                - mean_kappa_post: Average κ after evolution (L1)
        """
        self.n += 1
        
        # 1. FULL METRICS (once per tick - at start)
        # Compute κ which serves as decision info for this tick
        metrics = compute_metrics(self.G, self.params)
        
        # 2. PHYSICS (topology and weight changes)
        spawn_new, spawn_reinf = rule_spawn(self.G, self.params)
        
        # 3. FIELD-TAIL: Long-range weak bridges (FIELD proxy, not S2 Antipair)
        # Default: DISABLED. Enable via --enable-field-tail
        # This is MVP proxy for field, NOT S2 (Antipair) which is SPEC/unimplemented
        field_tail_added = rule_field_tail(self.G, self.params)
        
        # 4. DECAY
        removed = rule_propagate(self.G, self.params)
        
        # 5. LIGHT PRESSURE RE-CALCULATION
        # Physics changed weights, so pressure changed
        # Fast sum so Normalization sees current state
        current_pressure_map = {
            u: sum(e.w for e in self.G.adj[u].values())
            for u in range(self.G.num_nodes)
        }
        
        # 6. NORMALIZATION (Event Horizon)
        # If pressure exceeds W_max, cut weights
        norm_ops, step_tension = rule_normalize(
            self.G, current_pressure_map, self.params
        )
        
        # 6b. POST-EVOLUTION METRICS (CRITICAL: After all physics)
        # Re-compute κ after spawn/decay/normalize to get OBSERVATION state
        # This ensures projection uses current κ, not decision-time κ
        metrics_post = compute_metrics(self.G, self.params)
        
        # 7. TIME AND TENSION (Observables)
        global_tension_step = 0.0
        w_max = self.params.get('W_max', 2.5)  # Theory value (THEORY.md v2.0)
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

        # 8. PROJECTION (Layer 2: FRACTURE)
        theta = self.params.get('theta', 0.25)  # Theory value (THEORY.md v2.0)
        
        # CRITICAL: Visibility computed from POST-evolution κ (metrics_post)
        # NOT from decision-time κ (metrics_pre)
        # This enforces temporal separation: projection uses observable state
        visible_edges = sum(
            1 for e in self.G.all_edges() if e.kappa_cache >= theta
        )
        
        # 9. FINAL STATISTICS (for logs)
        
        final_total_p = sum(current_pressure_map.values())
        final_mean_p = final_total_p / max(1, self.G.num_nodes)
        
        max_acc_tension = (
            max(self.total_tension_map.values())
            if self.G.num_nodes > 0
            else 0.0
        )

        return {
            "tick": self.n,
            
            # Evolution events (L1-CORE)
            "spawn_new": spawn_new,
            "spawn_reinf": spawn_reinf,
            "field_tail_added": field_tail_added,
            "removed": removed,
            "norm_ops": norm_ops,
            
            # Observables (L1-CORE)
            "tension_step": global_tension_step,
            "max_acc_tension": max_acc_tension,
            
            # Projection (L2-FRACTURE)
            "visible_edges": visible_edges,
            "visible_ratio": visible_edges / max(1, len(self.G.edges)),
            
            # CORE state (L1)
            "total_edges": len(self.G.edges),
            "mean_pressure": final_mean_p,
            
            # Metrics (pre = decision, post = observation)
            "mean_kappa_pre": metrics["mean_kappa"],  # Decision-time κ
            "mean_kappa_post": metrics_post["mean_kappa"]  # Observation-time κ
        }
