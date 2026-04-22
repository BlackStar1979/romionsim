"""
ROMION CORE RNG (deterministic random source)

This module provides a deterministic RNG wrapper for CORE.
It enforces explicit seeding and avoids hidden randomness.

Rules:
- CORE must not depend on numpy or external RNG libraries.
- All randomness must be derived from an explicit seed.
- The engine must log the seed as part of explicit parameters.

Applies to ontology: THEORY_V3.9
Documentation status: v1-prerelease
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Optional, Sequence, TypeVar


T = TypeVar("T")


@dataclass
class CoreRng:
    """
    Deterministic random generator for CORE.

    This is a thin wrapper around random.Random,
    used to make it explicit and testable.
    """

    seed: int

    def __post_init__(self) -> None:
        self._rng = random.Random(int(self.seed))

    def rand_float(self) -> float:
        """
        Return a float in [0.0, 1.0).
        """
        return self._rng.random()

    def rand_uniform(self, a: float, b: float) -> float:
        """
        Return a float in [a, b].
        """
        return self._rng.uniform(a, b)

    def rand_int(self, a: int, b: int) -> int:
        """
        Return an int in [a, b] inclusive.
        """
        return self._rng.randint(a, b)

    def choice(self, items: Sequence[T]) -> T:
        """
        Choose one element from a non-empty sequence.
        """
        if not items:
            raise ValueError("choice() requires a non-empty sequence")
        return self._rng.choice(list(items))

    def shuffle(self, items: List[T]) -> None:
        """
        Shuffle a list in place.
        """
        self._rng.shuffle(items)

    def sample(self, items: Sequence[T], k: int) -> List[T]:
        """
        Sample k unique elements from a sequence.
        """
        if k < 0:
            raise ValueError("k must be >= 0")
        if k == 0:
            return []
        if k > len(items):
            raise ValueError("k must be <= len(items)")
        return self._rng.sample(list(items), k)

    def maybe(self, p: float) -> bool:
        """
        Return True with probability p.

        p must be in [0, 1].
        """
        if p < 0.0 or p > 1.0:
            raise ValueError("p must be in [0, 1]")
        return self.rand_float() < p

    def rand_weight(self, w_min: float, w_max: float) -> float:
        """
        Convenience: draw a non-negative weight in [w_min, w_max].

        Intended for CORE relation weight initialization.
        """
        if w_min < 0.0 or w_max < 0.0:
            raise ValueError("w_min and w_max must be >= 0")
        if w_max < w_min:
            raise ValueError("w_max must be >= w_min")
        return self.rand_uniform(w_min, w_max)