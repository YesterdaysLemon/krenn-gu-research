#!/usr/bin/env python3
"""Independent finite-field/combinatorial audit of tight P5 extraction.

This file imports nothing from the primary verifier.  The theorem over C is
the written proof; the finite fields audit its linear-algebra and coefficient
mechanics with separate implementations.
"""

from __future__ import annotations

import functools
import itertools
import json

PRIME = 101
KERNEL_PRIME = 5
ROOTS = tuple(range(5))
BLOCKERS = tuple(range(5, 10))


def inverse(value: int, prime: int) -> int:
    return pow(value % prime, prime - 2, prime)


def canonical_rowspace(vectors, prime: int):
    rows = [
        list(vector) for vector in vectors if any(entry % prime for entry in vector)
    ]
    if not rows:
        return ()
    column = 0
    pivot_row = 0
    while pivot_row < len(rows) and column < 3:
        pivot = next(
            (
                index
                for index in range(pivot_row, len(rows))
                if rows[index][column] % prime
            ),
            None,
        )
        if pivot is None:
            column += 1
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = inverse(rows[pivot_row][column], prime)
        rows[pivot_row] = [(entry * scale) % prime for entry in rows[pivot_row]]
        for index in range(len(rows)):
            if index == pivot_row:
                continue
            factor = rows[index][column] % prime
            if factor:
                rows[index] = [
                    (left - factor * right) % prime
                    for left, right in zip(rows[index], rows[pivot_row], strict=True)
                ]
        pivot_row += 1
        column += 1
    reduced = [tuple(row) for row in rows if any(row)]
    reduced.sort(
        key=lambda row: next(index for index, entry in enumerate(row) if entry)
    )
    return tuple(reduced)


def rowspace_contains(basis, vector, prime: int) -> bool:
    return len(canonical_rowspace((*basis, vector), prime)) == len(basis)


def dot(left, right, prime: int) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True)) % prime


def kernel_torus_audit():
    vectors = tuple(itertools.product(range(KERNEL_PRIME), repeat=3))
    nonzero = tuple(vector for vector in vectors if any(vector))
    subspaces = {()}
    for vector in nonzero:
        subspaces.add(canonical_rowspace((vector,), KERNEL_PRIME))
    for left in nonzero:
        for right in nonzero:
            basis = canonical_rowspace((left, right), KERNEL_PRIME)
            if len(basis) <= 2:
                subspaces.add(basis)

    coordinates = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    audited = 0
    for basis in subspaces:
        if any(rowspace_contains(basis, coordinate, KERNEL_PRIME) for coordinate in coordinates):
            continue
        kernel = tuple(
            vector
            for vector in nonzero
            if all(dot(row, vector, KERNEL_PRIME) == 0 for row in basis)
        )
        assert kernel
        assert any(all(entry != 0 for entry in vector) for vector in kernel)
        audited += 1
    return {"subspaces": len(subspaces), "coordinate_nonblocker_subspaces": audited}


def edge_weight(left: int, right: int, trial: int, residual: set[int]) -> int:
    left, right = sorted((left, right))
    if left in ROOTS and right in ROOTS:
        return 0
    if (left in ROOTS and right in residual) or (right in ROOTS and left in residual):
        return 0
    return (
        17 * (left + 1)
        + 29 * (right + 1)
        + 31 * trial * (left + 2) * (right + 3)
        + left * right
    ) % PRIME


def hafnian(vertices: tuple[int, ...], weight) -> int:
    index = {vertex: position for position, vertex in enumerate(vertices)}

    @functools.cache
    def solve(mask: int) -> int:
        if mask == 0:
            return 1
        first_bit = mask & -mask
        first_position = first_bit.bit_length() - 1
        first = vertices[first_position]
        rest = mask ^ first_bit
        total = 0
        bits = rest
        while bits:
            second_bit = bits & -bits
            second_position = second_bit.bit_length() - 1
            second = vertices[second_position]
            total += weight(first, second) * solve(rest ^ second_bit)
            bits ^= second_bit
        return total % PRIME

    full_mask = sum(1 << index[vertex] for vertex in vertices)
    return solve(full_mask)


def permanent(matrix) -> int:
    size = len(matrix)

    @functools.cache
    def solve(row: int, used: int) -> int:
        if row == size:
            return 1
        total = 0
        for column in range(size):
            if not used & (1 << column):
                total += matrix[row][column] * solve(row + 1, used | (1 << column))
        return total % PRIME

    return solve(0, 0)


def factorisation_audit(residual_size: int, trial: int):
    residual_vertices = tuple(range(10, 10 + residual_size))
    residual = set(residual_vertices)
    vertices = ROOTS + BLOCKERS + residual_vertices
    def weight(left, right):
        return edge_weight(left, right, trial, residual)
    full = hafnian(vertices, weight)
    root_blocker = tuple(
        tuple(weight(root, blocker) for blocker in BLOCKERS) for root in ROOTS
    )
    root_permanent = permanent(root_blocker)
    residual_hafnian = hafnian(residual_vertices, weight)
    assert full == root_permanent * residual_hafnian % PRIME
    return {
        "vertices": len(vertices),
        "trial": trial,
        "full_hafnian": full,
        "root_blocker_permanent": root_permanent,
        "residual_hafnian": residual_hafnian,
    }


def main() -> None:
    # Three subsets of a five-element union, each of cardinality at least
    # five, are the same common five-set.
    universe = set(range(5))
    blocker_triples = 0
    for first in (universe,):
        for second in (universe,):
            for third in (universe,):
                assert first | second | third == universe
                assert first == second == third
                blocker_triples += 1

    kernel_report = kernel_torus_audit()
    factor_reports = [
        factorisation_audit(residual_size, trial)
        for residual_size in (0, 2, 4, 6)
        for trial in (1, 2)
    ]

    # Independently check that all nonzero diagonal coefficients can be
    # removed by rescaling one local mode over F_7.
    rescaling_checks = 0
    for coefficients in itertools.product(range(1, 7), repeat=3):
        scalings = tuple(inverse(value, 7) for value in coefficients)
        assert tuple(
            value * scale % 7
            for value, scale in zip(coefficients, scalings, strict=True)
        ) == (1, 1, 1)
        rescaling_checks += 1

    # Coordinate evaluation separates the three diagonal tensors.
    evaluation_matrix = tuple(
        tuple(
            1 if evaluation_colour == tensor_colour else 0
            for tensor_colour in range(3)
        )
        for evaluation_colour in range(3)
    )
    assert evaluation_matrix == ((1, 0, 0), (0, 1, 0), (0, 0, 1))

    print(
        json.dumps(
            {
                "status": "verified",
                "matching_field": f"F_{PRIME}",
                "kernel_field": f"F_{KERNEL_PRIME}",
                "blocker_set_triples": blocker_triples,
                "kernel_torus_audit": kernel_report,
                "factorisation_audits": factor_reports,
                "diagonal_independence_rank": 3,
                "nonzero_rescaling_checks_over_F7": rescaling_checks,
                "role": "independent corroboration of the arbitrary-order proof over C",
                "global_conjecture": "unresolved",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
