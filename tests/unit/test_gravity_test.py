"""
Unit tests for gravity_test package.

Tests basic functionality of modular components.
Run with: pytest tests/unit/test_gravity_test.py
Or: python -m pytest tests/unit/test_gravity_test.py
"""

import sys
from pathlib import Path

# Add analysis to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'analysis'))

from gravity_test import (
    infer_n,
    build_node_adj_threshold,
    find_components,
    assign_clusters,
    count_bridges,
    compute_hub,
    BridgeAgg
)


def test_infer_n():
    """Test node count inference from edges."""
    edges = [[0, 1, 1.0], [1, 2, 1.0], [2, 3, 1.0]]
    assert infer_n(edges) == 4
    
    edges = []
    assert infer_n(edges) == 0
    
    edges = [[5, 10, 1.0]]
    assert infer_n(edges) == 11  # Max node + 1


def test_build_adj_threshold():
    """Test adjacency list building with threshold."""
    edges = [
        [0, 1, 0.5],
        [1, 2, 0.3],
        [2, 3, 0.1],
    ]
    
    # High threshold - only strong edge
    adj = build_node_adj_threshold(edges, 0.4)
    assert 1 in adj[0] and 0 in adj[1]
    assert 2 not in adj.get(1, [])
    
    # Low threshold - all edges
    adj = build_node_adj_threshold(edges, 0.0)
    assert len(adj) == 4


def test_find_components():
    """Test component detection."""
    # Simple chain: 0-1-2
    adj = {0: [1], 1: [0, 2], 2: [1]}
    comps = find_components(3, adj)
    assert len(comps) == 1
    assert len(comps[0]) == 3
    
    # Two separate components
    adj = {0: [1], 1: [0], 2: [3], 3: [2]}
    comps = find_components(4, adj)
    assert len(comps) == 2


def test_assign_clusters():
    """Test cluster assignment."""
    comps = [[0, 1, 2], [3, 4], [5]]
    node2c = assign_clusters(comps)
    
    assert node2c[0] == node2c[1] == node2c[2]  # Same cluster
    assert node2c[3] == node2c[4]  # Same cluster
    assert node2c[0] != node2c[3]  # Different clusters
    assert node2c[3] != node2c[5]  # Different clusters


def test_count_bridges():
    """Test bridge counting between clusters."""
    # Two clusters: [0,1] and [2,3]
    node2c = [0, 0, 1, 1]
    edges = [
        [0, 1, 1.0],  # Intra-cluster
        [2, 3, 1.0],  # Intra-cluster
        [0, 2, 0.5],  # Bridge
        [1, 3, 0.3],  # Bridge
    ]
    
    bridges, unassigned = count_bridges(edges, node2c, 0.0)
    
    assert len(bridges) == 1  # One cluster pair
    assert (0, 1) in bridges
    assert bridges[(0, 1)].count == 2
    assert abs(bridges[(0, 1)].w_sum - 0.8) < 0.01


def test_compute_hub():
    """Test hub computation."""
    # Simple hub: cluster 0 connects to clusters 1,2,3
    bridges = {
        (0, 1): BridgeAgg(1.0, 1),
        (0, 2): BridgeAgg(1.0, 1),
        (0, 3): BridgeAgg(1.0, 1),
    }
    
    hub_id, hub_deg, hub_share, coverage = compute_hub(bridges, 4)
    
    assert hub_id == 0
    assert hub_deg == 3
    assert hub_share == 50.0  # 3 out of 6 connections
    assert coverage == 100.0  # All 4 clusters have bridges


def test_bridge_agg():
    """Test BridgeAgg dataclass."""
    agg = BridgeAgg()
    assert agg.w_sum == 0.0
    assert agg.count == 0
    
    agg = BridgeAgg(5.0, 10)
    assert agg.w_sum == 5.0
    assert agg.count == 10


def test_empty_graph():
    """Test edge cases with empty graphs."""
    # Empty edges
    edges = []
    assert infer_n(edges) == 0
    
    # Empty adjacency
    comps = find_components(5, {})
    assert len(comps) == 5  # All singletons
    
    # Empty clusters
    node2c = []
    bridges, _ = count_bridges([], node2c, 0.0)
    assert len(bridges) == 0


def test_unassigned_nodes():
    """Test handling of unassigned nodes (cluster -1)."""
    node2c = [0, 0, -1, 1, 1]  # Node 2 unassigned
    edges = [
        [0, 1, 1.0],  # Intra (cluster 0)
        [2, 3, 1.0],  # Has unassigned node
        [3, 4, 1.0],  # Intra (cluster 1)
    ]
    
    bridges, unassigned = count_bridges(edges, node2c, 0.0)
    
    # Should skip edge with unassigned node
    assert unassigned == 1, f"Expected 1 unassigned, got {unassigned}"
    assert len(bridges) == 0, f"Expected 0 bridges, got {len(bridges)}"  # No inter-cluster edges!


if __name__ == '__main__':
    # Run tests manually
    print("Running gravity_test unit tests...")
    
    tests = [
        test_infer_n,
        test_build_adj_threshold,
        test_find_components,
        test_assign_clusters,
        test_count_bridges,
        test_compute_hub,
        test_bridge_agg,
        test_empty_graph,
        test_unassigned_nodes,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print(f"  [OK] {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  [FAIL] {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  [ERROR] {test.__name__}: {e}")
            failed += 1
    
    print()
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed > 0:
        sys.exit(1)
