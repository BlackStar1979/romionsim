# romionsim/core/__init__.py
"""
ROMION Core Simulation Engine

Clean, theory-driven implementation based on:
- S1 (Closure): Topological shortcuts [MVP - IMPLEMENTED]
- S2 (Antipair): Quasi-unitarity [SPEC - UNIMPLEMENTED]
- S3 (Triadic): Type composition [SPEC - UNIMPLEMENTED]

Field-tail: MVP proxy for long-range field [MVP - OPTIONAL]
  - NOT S2 (Antipair) - experimental mechanism only
  - Enable via --enable-field-tail flag
  - Phenomenological parameters (not theory-derived)

Quantum Spark: DEPRECATED (no theoretical derivation)
  - Was: Speculative S2-related feature
  - Status: DISABLED by default, will be REMOVED
"""

from .graph import Graph, Edge
from .rules import rule_spawn, rule_propagate, rule_normalize
from .metrics import compute_metrics
from .engine import CoreEngine

__all__ = [
    'Graph',
    'Edge', 
    'rule_spawn',
    'rule_propagate',
    'rule_normalize',
    'compute_metrics',
    'CoreEngine'
]

__version__ = '1.0.0-clean'
