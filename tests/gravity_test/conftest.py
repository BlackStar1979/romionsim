"""Pytest configuration and fixtures for gravity_test tests."""

from __future__ import annotations

import sys
from pathlib import Path
import pytest


# Ensure repo root is importable when running pytest from root
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def meta_graph_simple():
    """4 clusters with controlled cut weights."""
    return {
        (0, 1): 1.0,
        (1, 2): 2.0,
        (2, 3): 3.0,
        (0, 3): 4.0,
    }


@pytest.fixture
def meta_graph_symmetric():
    """Complete graph on 5 clusters, equal weights. Anisotropy should be ~0."""
    g = {}
    n = 5
    for i in range(n):
        for j in range(i + 1, n):
            g[(i, j)] = 1.0
    return g, n


@pytest.fixture
def meta_graph_corridor():
    """
    Corridor-like structure on 6 clusters:
    Strong edges along chain 0-1-2-3-4-5, plus weak cross edges.
    Should yield anisotropy > 0.
    """
    g = {
        (0, 1): 10.0,
        (1, 2): 10.0,
        (2, 3): 10.0,
        (3, 4): 10.0,
        (4, 5): 10.0,
        # weak shortcuts
        (0, 2): 0.5,
        (1, 3): 0.5,
        (2, 4): 0.5,
        (3, 5): 0.5,
    }
    return g, 6
