"""
Gravity Test - Bridge Analysis for ROMION

Modular version split into:
- io: File loading and parsing
- clustering: Component detection and cluster assignment
- metrics: Bridge counting and hub analysis
- distances: All-pairs distances and distance tables
- regions: Deterministic region splitting (for channels)
- channels: Channel capacity and anisotropy metrics
- validate: Fail-closed validation layer
- main: CLI and reporting

Backward compatible with original gravity_test.py usage.
"""

__version__ = "2.1.0"

# Re-export main functions for backward compatibility
from .io import load_graph_snapshot, parse_tick_range
from .clustering import (
    infer_n,
    build_node_adj_threshold,
    build_node_adj_topk,
    find_components,
    assign_clusters
)
from .metrics import (
    BridgeAgg,
    count_bridges,
    build_cluster_graph_from_edges,
    compute_hub,
    correlations,
    spearmanr
)
from .distances import (
    all_pairs_cluster_distances,
    distance_table,
    is_connectivity_only,
    build_background_cluster_graph
)

# New modules for channels/anisotropy (SPEC-ready metrics)
from .regions import split_regions
from .channels import path_capacity, anisotropy_index
from .validate import validate_metrics, format_invalid_report

__all__ = [
    # IO
    'load_graph_snapshot',
    'parse_tick_range',
    
    # Clustering
    'infer_n',
    'build_node_adj_threshold',
    'build_node_adj_topk',
    'find_components',
    'assign_clusters',
    
    # Metrics
    'BridgeAgg',
    'count_bridges',
    'build_cluster_graph_from_edges',
    'compute_hub',
    'correlations',
    'spearmanr',
    
    # Distances
    'all_pairs_cluster_distances',
    'distance_table',
    'is_connectivity_only',
    'build_background_cluster_graph',
    
    # Regions / Channels (SPEC-ready metrics on background geometry)
    'split_regions',
    'path_capacity',
    'anisotropy_index',
    
    # Validation (fail-closed)
    'validate_metrics',
    'format_invalid_report',
]
