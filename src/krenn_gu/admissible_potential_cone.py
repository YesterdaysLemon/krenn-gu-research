"""Shared immutable rays for the admissible-potential cone."""

from __future__ import annotations

EXTREME_RAYS: tuple[tuple[int, ...], ...] = (
    (-4, 1, 1, 1, 6, -4),
    (-4, 1, 6, 1, 1, -4),
    (1, -4, 1, 1, -4, 6),
    (1, -4, 1, 6, -4, 1),
    (1, 6, -4, -4, 1, 1),
    (6, 1, -4, -4, 1, 1),
)

__all__ = ["EXTREME_RAYS"]
