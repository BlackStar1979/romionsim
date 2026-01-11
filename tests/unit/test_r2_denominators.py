"""
Unit test for ROMION bridge distance distribution.

Tests canonical P(dist | bridge) computation.
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from analysis.gravity_test.distances import distance_table
from collections import namedtuple


# Mock bridge aggregate
BridgeAgg = namedtuple('BridgeAgg', ['count', 'w_sum'])


def test_romion_p_dist_given_bridge():
    """Test ROMION PRIMARY metric: P(dist | bridge)."""
    
    # Mock data: 4 clusters
    dists = {
        (0, 1): 1,  # dist=1: 3 background pairs
        (0, 2): 1,
        (1, 2): 1,
        (0, 3): 2,  # dist=2: 3 background pairs
        (1, 3): 2,
        (2, 3): 2,
    }
    
    # Bridges: only 2 pairs at dist=1
    bridges = {
        (0, 1): BridgeAgg(count=5, w_sum=1.5),
        (1, 2): BridgeAgg(count=3, w_sum=0.9),
    }
    
    rows = distance_table(bridges, dists)
    
    # ROMION: total_bridged_pairs = 2
    total_bridged = sum(r['bridged_pairs'] for r in rows)
    assert total_bridged == 2, f"Expected 2 total bridged pairs, got {total_bridged}"
    
    # Check PRIMARY metric: P(dist | bridge)
    d1 = [r for r in rows if r['dist'] == 1][0]
    assert d1['bridged_pairs'] == 2, f"dist=1: expected 2 bridged pairs"
    assert abs(d1['p_dist_given_bridge'] - 1.0) < 0.01, f"dist=1: P(d|br)=1.0, got {d1['p_dist_given_bridge']}"
    
    d2 = [r for r in rows if r['dist'] == 2][0]
    assert d2['bridged_pairs'] == 0, f"dist=2: expected 0 bridged pairs"
    assert d2['p_dist_given_bridge'] == 0.0, f"dist=2: P(d|br)=0, got {d2['p_dist_given_bridge']}"
    
    # Check distribution sums to 1.0
    total_p = sum(r['p_dist_given_bridge'] for r in rows)
    assert abs(total_p - 1.0) < 1e-6, f"ΣP(dist|bridge) should be 1.0, got {total_p}"
    
    print("[PASS] test_romion_p_dist_given_bridge")


def test_romion_diagnostic_metric():
    """Test DIAGNOSTIC metric: P(bridge | dist) for reference."""
    
    dists = {
        (0, 1): 1,
        (0, 2): 1,
    }
    
    bridges = {
        (0, 1): BridgeAgg(count=10, w_sum=2.0),
        # (0, 2) has NO bridge
    }
    
    rows = distance_table(bridges, dists)
    
    d1 = [r for r in rows if r['dist'] == 1][0]
    
    # PRIMARY: P(dist|bridge) = 1.0 (all bridges at d=1)
    assert abs(d1['p_dist_given_bridge'] - 1.0) < 0.01
    
    # DIAGNOSTIC: P(bridge|dist) = 1/2 (1 out of 2 pairs at d=1 has bridge)
    assert d1['background_pairs'] == 2, "Expected 2 background pairs at d=1"
    assert d1['bridged_pairs'] == 1, "Expected 1 bridged pair at d=1"
    assert abs(d1['p_bridge_given_dist'] - 0.5) < 0.01, f"P(br|d=1)=0.5, got {d1['p_bridge_given_dist']}"
    
    print("[PASS] test_romion_diagnostic_metric")


def test_romion_finite_range():
    """Test finite-range field (all bridges at d=1 only)."""
    
    dists = {
        (0, 1): 1,
        (0, 2): 2,
        (1, 2): 3,
    }
    
    bridges = {
        (0, 1): BridgeAgg(count=5, w_sum=1.0),
    }
    
    rows = distance_table(bridges, dists)
    
    # Find d_max (maximum distance with bridges)
    bridged_dists = [r['dist'] for r in rows if r['bridged_pairs'] > 0]
    d_max = max(bridged_dists) if bridged_dists else 0
    
    assert d_max == 1, f"Expected d_max=1 (finite range), got {d_max}"
    
    # All probability mass at d=1
    d1 = [r for r in rows if r['dist'] == 1][0]
    assert d1['p_dist_given_bridge'] == 1.0, "All bridges should be at d=1"
    
    print("[PASS] test_romion_finite_range")


def test_romion_empty():
    """Test empty case (no bridges)."""
    
    dists = {}
    bridges = {}
    
    rows = distance_table(bridges, dists)
    
    assert len(rows) == 0, "Empty input should give empty output"
    
    # Check that sum is well-defined (0.0 for empty)
    total_p = sum(r['p_dist_given_bridge'] for r in rows)
    assert total_p == 0.0, "Empty distribution should sum to 0"
    
    print("[PASS] test_romion_empty")


if __name__ == '__main__':
    test_romion_p_dist_given_bridge()
    test_romion_diagnostic_metric()
    test_romion_finite_range()
    test_romion_empty()
    print("\n[PASS] ALL ROMION TESTS PASSED")
