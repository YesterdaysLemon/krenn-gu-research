"""Numerically test the full two-vertex quotient obstruction.

Fix vertices p,q and local contractions x,y with

    x^T W_(p,q) y = 0.

At every remaining vertex r, let K_r be the simultaneous kernel of
W_(p,r)^T x and W_(q,r)^T y. Every perfect-matching contribution vanishes
on x tensor y tensor product_r K_r. A genuine GHZ realization must
therefore satisfy

    sum_c x_c y_c tensor_r (e_c restricted to K_r) = 0.

The cross-product test represents K_r by one vector and loses all
information when the two defining covectors are dependent. This script
keeps a complete numerical basis of K_r, so it remains informative on
rank-deficient strata such as the triangular-prism degeneration.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from prism_boundary import prism_weights
from search_witness import EquationSystem, load_candidate


def oriented_block(
    system: EquationSystem, weights: np.ndarray, centre: int, leaf: int
) -> np.ndarray:
    """Return the block with centre as its row endpoint."""

    blocks = system.edge_array(weights)
    if centre < leaf:
        return blocks[system.edge_index[(centre, leaf)]]
    return blocks[system.edge_index[(leaf, centre)]].T


def simultaneous_kernel_basis(
    first_covector: np.ndarray,
    second_covector: np.ndarray,
    relative_tolerance: float = 1e-10,
) -> np.ndarray:
    """Return orthonormal columns spanning both bilinear kernels."""

    constraints = np.vstack((first_covector, second_covector))
    _, singular_values, right_vectors_h = np.linalg.svd(
        constraints, full_matrices=True
    )
    scale = max(
        1.0, float(singular_values[0]) if singular_values.size else 0.0
    )
    rank = int(np.sum(singular_values > relative_tolerance * scale))
    return right_vectors_h[rank:].conj().T


def sample_on_bilinear_zero(
    block: np.ndarray, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray] | None:
    """Sample normalized x,y satisfying x^T block y = 0."""

    x = rng.standard_normal(3) + 1j * rng.standard_normal(3)
    x /= np.linalg.norm(x)
    row = x @ block
    pivot = int(np.argmax(np.abs(row)))
    if abs(row[pivot]) < 1e-12:
        y = rng.standard_normal(3) + 1j * rng.standard_normal(3)
        y /= np.linalg.norm(y)
        return x, y
    y = rng.standard_normal(3) + 1j * rng.standard_normal(3)
    y[pivot] = 0
    y[pivot] = -(row @ y) / row[pivot]
    norm = np.linalg.norm(y)
    if norm < 1e-12:
        return None
    y /= norm
    return x, y


def quotient_tensor(
    system: EquationSystem,
    weights: np.ndarray,
    p: int,
    q: int,
    x: np.ndarray,
    y: np.ndarray,
) -> tuple[np.ndarray, list[int]]:
    """Build the restricted diagonal tensor and its local dimensions."""

    bases: list[np.ndarray] = []
    for leaf in range(system.n):
        if leaf in (p, q):
            continue
        first_covector = oriented_block(system, weights, p, leaf).T @ x
        second_covector = oriented_block(system, weights, q, leaf).T @ y
        bases.append(
            simultaneous_kernel_basis(first_covector, second_covector)
        )

    dimensions = [basis.shape[1] for basis in bases]
    tensor = np.zeros(dimensions, dtype=np.complex128)
    for colour in range(3):
        term: np.ndarray | np.complex128 = np.complex128(
            x[colour] * y[colour]
        )
        for basis in bases:
            term = np.multiply.outer(term, basis[colour, :])
        tensor += term
    return tensor, dimensions


def audit_pair(
    system: EquationSystem,
    weights: np.ndarray,
    p: int,
    q: int,
    samples: int,
    rng: np.random.Generator,
) -> dict[str, float | int | list[int]]:
    """Return the largest sampled quotient residual for one vertex pair."""

    block = oriented_block(system, weights, p, q)
    maximum = 0.0
    maximum_dimensions: list[int] = []
    completed = 0
    bilinear_error = 0.0
    for _ in range(samples):
        sampled = sample_on_bilinear_zero(block, rng)
        if sampled is None:
            continue
        x, y = sampled
        bilinear_error = max(bilinear_error, float(abs(x @ block @ y)))
        tensor, dimensions = quotient_tensor(system, weights, p, q, x, y)
        norm = float(np.linalg.norm(tensor))
        if norm > maximum:
            maximum = norm
            maximum_dimensions = dimensions
        completed += 1
    return {
        "samples": completed,
        "max_quotient_residual": maximum,
        "max_bilinear_error": bilinear_error,
        "dimensions_at_max": maximum_dimensions,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--candidate", type=Path)
    source.add_argument("--prism-x", type=float)
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    system = EquationSystem(6, 3)
    if args.candidate is not None:
        weights = load_candidate(args.candidate, system)
    else:
        system, weights = prism_weights(complex(args.prism_x))

    rng = np.random.default_rng(args.seed)
    overall = 0.0
    for p in range(system.n):
        for q in range(p + 1, system.n):
            result = audit_pair(
                system, weights, p, q, args.samples, rng
            )
            overall = max(
                overall, float(result["max_quotient_residual"])
            )
            print(f"pair=({p},{q}) {result}")
    print(f"overall_max_quotient_residual={overall:.12e}")


if __name__ == "__main__":
    main()
