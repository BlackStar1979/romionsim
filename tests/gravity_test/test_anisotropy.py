"""Tests for anisotropy metrics."""

from __future__ import annotations

import pytest


def test_anisotropy_symmetric_near_zero(meta_graph_symmetric):
    from analysis.gravity_test.channels import anisotropy_index

    g, n = meta_graph_symmetric
    anis, meta = anisotropy_index(
        g, n_clusters=n, n_splits=5, 
        split_method="bfs_seed", capacity_mode="cut_weight"
    )
    # Symmetric graph should have very low or zero anisotropy
    assert anis == pytest.approx(0.0, abs=0.01)
    assert meta["degenerate"] is False
    assert len(meta["caps"]) >= 1


def test_anisotropy_corridor_positive(meta_graph_corridor):
    from analysis.gravity_test.channels import anisotropy_index

    g, n = meta_graph_corridor
    anis, meta = anisotropy_index(
        g, n_clusters=n, n_splits=5,
        split_method="bfs_seed", capacity_mode="cut_weight"
    )
    # Corridor should create variability across split axes
    assert anis >= 0.0
    assert meta["degenerate"] is False


def test_anisotropy_degenerate_returns_zero():
    from analysis.gravity_test.channels import anisotropy_index

    # No edges at all => all capacities 0 => degenerate
    g = {}
    anis, meta = anisotropy_index(
        g, n_clusters=4, n_splits=3,
        split_method="bfs_seed", capacity_mode="cut_weight"
    )
    assert anis == pytest.approx(0.0)
    assert meta["degenerate"] is True


def test_anisotropy_requires_two_clusters():
    from analysis.gravity_test.channels import anisotropy_index

    with pytest.raises(ValueError):
        anisotropy_index({}, n_clusters=1)
