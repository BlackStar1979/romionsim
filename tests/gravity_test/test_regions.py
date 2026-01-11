"""Tests for region splitting."""

from __future__ import annotations

import pytest


def test_split_regions_basic(meta_graph_simple):
    from analysis.gravity_test.regions import split_regions

    n_clusters = 4
    L, R, meta = split_regions(meta_graph_simple, n_clusters, method="bfs_seed")

    assert isinstance(L, set) and isinstance(R, set)
    assert L and R  # Both non-empty
    assert L.isdisjoint(R)
    assert len(L) + len(R) == n_clusters
    assert meta["n_clusters"] == n_clusters
    assert meta["method"] == "bfs_seed"


def test_split_regions_deterministic(meta_graph_simple):
    from analysis.gravity_test.regions import split_regions

    n_clusters = 4
    L1, R1, _ = split_regions(meta_graph_simple, n_clusters, method="bfs_seed")
    L2, R2, _ = split_regions(meta_graph_simple, n_clusters, method="bfs_seed")
    assert L1 == L2
    assert R1 == R2


def test_split_regions_requires_two_clusters(meta_graph_simple):
    from analysis.gravity_test.regions import split_regions

    with pytest.raises(ValueError):
        split_regions(meta_graph_simple, 1)


def test_split_regions_unknown_method(meta_graph_simple):
    from analysis.gravity_test.regions import split_regions

    with pytest.raises(ValueError):
        split_regions(meta_graph_simple, 4, method="unknown")


def test_split_regions_handles_disconnected_graph():
    from analysis.gravity_test.regions import split_regions

    # Two disconnected components: (0-1) and (2-3)
    g = {(0, 1): 1.0, (2, 3): 1.0}
    L, R, meta = split_regions(g, 4, method="bfs_seed")
    assert len(L) + len(R) == 4
    assert meta["disconnected_clusters"] >= 0
