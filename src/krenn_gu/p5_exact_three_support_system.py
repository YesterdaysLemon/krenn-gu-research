"""Exact-three-partial specialization of the shared P5 support core."""

from __future__ import annotations

from krenn_gu.p5_support_system import generate as generate_support_system


def generate(
    supports: tuple[tuple[int, ...], ...],
    signature_indices: tuple[int, ...],
) -> tuple[str, dict]:
    return generate_support_system(
        supports,
        signature_indices,
        expected_partial_cells=3,
    )


__all__ = ["generate"]
