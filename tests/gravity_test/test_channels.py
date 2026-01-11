"""Tests for channel capacity metrics."""

from __future__ import annotations

import pytest


def test_path_capacity_cut_weight(meta_graph_simple):
    from analysis.gravity_test.channels import path_capacity

    # Choose regions manually
    L = {0, 1}
    R = {2, 3}
    cap, meta = path_capacity(meta_graph_simple, L, R, mode="cut_weight")

    # Crossing edges are: (1,2)=2.0 and (0,3)=4.0 => sum = 6.0
    assert cap == pytest.approx(6.0)
    assert meta["cut_edges"] == 2
    assert meta["mode"] == "cut_weight"


def test_path_capacity_zero_when_no_cross_edges():
    from analysis.gravity_test.channels import path_capacity

    g = {(0, 1): 1.0, (2, 3): 2.0}
    cap, meta = path_capacity(g, {0, 1}, {2, 3}, mode="cut_weight")
    assert cap == pytest.approx(0.0)
    assert meta["cut_edges"] == 0


def test_path_capacity_unknown_mode(meta_graph_simple):
    from analysis.gravity_test.channels import path_capacity

    with pytest.raises(ValueError):
        path_capacity(meta_graph_simple, {0}, {1, 2, 3}, mode="paths")
