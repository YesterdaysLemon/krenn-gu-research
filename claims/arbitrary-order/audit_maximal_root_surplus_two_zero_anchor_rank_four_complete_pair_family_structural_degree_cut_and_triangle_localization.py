"""Independent standard-library audit for GLS46.

This script imports no repository module or third-party package.  It uses a
finite-field linear-factor solver, exhaustive labelled zero products, an
independent cut-subspace backtracker, and custom rational elimination.
The written proof, not the finite audits, carries the arbitrary-dimensional
characteristic-zero theorem.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product


def rank_mod(rows: list[list[int]], prime: int) -> int:
    """Return exact row rank over a prime field."""

    work = [[entry % prime for entry in row] for row in rows]
    rank = 0
    columns = len(work[0]) if work else 0
    for column in range(columns):
        pivot = next(
            (index for index in range(rank, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, prime)
        work[rank] = [(entry * inverse) % prime for entry in work[rank]]
        for index, row in enumerate(work):
            if index == rank or row[column] == 0:
                continue
            multiple = row[column]
            work[index] = [
                (left - multiple * right) % prime
                for left, right in zip(row, work[rank], strict=True)
            ]
        rank += 1
    return rank


def consistent_mod(matrix: list[list[int]], target: list[int], prime: int) -> bool:
    """Decide exact consistency by comparing coefficient and augmented ranks."""

    augmented = [
        [*row, value] for row, value in zip(matrix, target, strict=True)
    ]
    return rank_mod(matrix, prime) == rank_mod(augmented, prime)


def projective_vectors(length: int, prime: int) -> tuple[tuple[int, ...], ...]:
    """Normalize nonzero projective vectors by the first nonzero coordinate."""

    representatives = []
    for vector in product(range(prime), repeat=length):
        first = next((entry for entry in vector if entry), None)
        if first is None:
            continue
        inverse = pow(first, -1, prime)
        normalized = tuple((entry * inverse) % prime for entry in vector)
        if normalized == vector:
            representatives.append(vector)
    return tuple(representatives)


def monomials(variables: int, degree: int) -> tuple[tuple[int, ...], ...]:
    """Enumerate exponent vectors of one total degree."""

    return tuple(
        exponent
        for exponent in product(range(degree + 1), repeat=variables)
        if sum(exponent) == degree
    )


def reducibility_census() -> dict[str, int]:
    """Independently solve for every linear factor of every F3 excess cubic."""

    prime = 3
    linear_forms = projective_vectors(4, prime)
    quadratic_monomials = monomials(4, 2)
    cubic_monomials = monomials(4, 3)
    cubic_index = {monomial: index for index, monomial in enumerate(cubic_monomials)}
    multiplication_matrices: dict[tuple[int, ...], list[list[int]]] = {}
    for linear in linear_forms:
        matrix = [[0] * len(quadratic_monomials) for _ in cubic_monomials]
        for linear_index, linear_coefficient in enumerate(linear):
            if linear_coefficient == 0:
                continue
            unit = tuple(1 if index == linear_index else 0 for index in range(4))
            for column, quadratic in enumerate(quadratic_monomials):
                cubic = tuple(
                    left + right for left, right in zip(unit, quadratic, strict=True)
                )
                matrix[cubic_index[cubic]][column] = linear_coefficient
        multiplication_matrices[linear] = matrix

    excess_lines = projective_vectors(6, prime)
    reducible = 0
    for f01, f02, f10, f12, f20, f21 in excess_lines:
        alpha = f12 * f21 % prime
        beta = f02 * f20 % prime
        gamma = f01 * f10 % prime
        tau = (f01 * f12 * f20 + f02 * f10 * f21) % prime
        coefficients = [0] * len(cubic_monomials)
        coefficients[cubic_index[(1, 1, 1, 0)]] = 1
        coefficients[cubic_index[(1, 0, 0, 2)]] = -alpha % prime
        coefficients[cubic_index[(0, 1, 0, 2)]] = -beta % prime
        coefficients[cubic_index[(0, 0, 1, 2)]] = -gamma % prime
        coefficients[cubic_index[(0, 0, 0, 3)]] = tau
        has_linear_factor = any(
            consistent_mod(matrix, coefficients, prime)
            for matrix in multiplication_matrices.values()
        )
        predicted = (
            (beta == gamma == tau == 0)
            or (alpha == gamma == tau == 0)
            or (alpha == beta == tau == 0)
        )
        assert has_linear_factor == predicted
        reducible += int(has_linear_factor)
    assert len(excess_lines) == 364
    return {
        "excess_lines": len(excess_lines),
        "linear_forms": len(linear_forms),
        "reducible_cubics": reducible,
    }


def support(vector: tuple[int, ...]) -> frozenset[int]:
    return frozenset(index for index, entry in enumerate(vector) if entry)


def zero_product_census() -> dict[str, int]:
    """Exhaust the three-label scalar shadow of the labelled product lemma."""

    prime = 3
    vectors = tuple(product(range(prime), repeat=3))
    compatible = 0
    for alpha, beta in product(vectors, repeat=2):
        if not any(alpha) or not any(beta):
            continue
        condition = all(
            (alpha[left] * beta[right] + beta[left] * alpha[right]) % prime == 0
            for left in range(3)
            for right in range(left + 1, 3)
        )
        if not condition:
            continue
        compatible += 1
        assert support(alpha) == support(beta)
        assert len(support(alpha)) <= 2
    assert compatible > 0
    return {"nonzero_pairs": (len(vectors) - 1) ** 2, "compatible": compatible}


def vector_span_mask(vectors: int) -> int:
    """Return the F2 subspace generated by the set-bit vectors."""

    generators = [value for value in range(1, 8) if vectors & (1 << value)]
    values = {0}
    for generator in generators:
        values |= {value ^ generator for value in tuple(values)}
    return sum(1 << value for value in values)


def subspace_rank(mask: int) -> int:
    size = mask.bit_count()
    return {1: 0, 2: 1, 4: 2, 8: 3}[size]


def cut_subspace_census() -> dict[str, int]:
    """Exhaust all K4 edge-subspace assignments satisfying the cut bound."""

    subspaces = tuple(
        mask
        for mask in range(1 << 8)
        if mask & 1 and vector_span_mask(mask) == mask
    )
    assert len(subspaces) == 16
    edges = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
    cuts = tuple(
        tuple(
            index
            for index, edge in enumerate(edges)
            if ((edge[0] in side) != (edge[1] in side))
        )
        for side in (
            {0},
            {1},
            {2},
            {3},
            {0, 1},
            {0, 2},
            {0, 3},
        )
    )
    edge_cuts = tuple(
        tuple(index for index, cut in enumerate(cuts) if edge in cut)
        for edge in range(len(edges))
    )
    examined = 0
    rank_three = 0

    def recurse(
        edge_index: int,
        assignment: list[int],
        cut_spans: list[int],
        total_span: int,
    ) -> None:
        nonlocal examined, rank_three
        if edge_index == len(edges):
            examined += 1
            if subspace_rank(total_span) != 3:
                return
            rank_three += 1
            witnesses = []
            for vertices in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)):
                triangle_indices = tuple(
                    index
                    for index, edge in enumerate(edges)
                    if edge[0] in vertices and edge[1] in vertices
                )
                if any(subspace_rank(assignment[index]) != 1 for index in triangle_indices):
                    continue
                triangle_span = 1
                for index in triangle_indices:
                    triangle_span = vector_span_mask(triangle_span | assignment[index])
                if subspace_rank(triangle_span) != 3:
                    continue
                outside = set(range(len(edges))) - set(triangle_indices)
                if all(subspace_rank(assignment[index]) == 0 for index in outside):
                    witnesses.append(vertices)
            assert witnesses
            return

        for subspace in subspaces:
            updated_cuts = cut_spans.copy()
            valid = True
            for cut_index in edge_cuts[edge_index]:
                updated = vector_span_mask(updated_cuts[cut_index] | subspace)
                if subspace_rank(updated) > 2:
                    valid = False
                    break
                updated_cuts[cut_index] = updated
            if not valid:
                continue
            recurse(
                edge_index + 1,
                [*assignment, subspace],
                updated_cuts,
                vector_span_mask(total_span | subspace),
            )

    recurse(0, [], [1] * len(cuts), 1)
    assert rank_three > 0
    return {"cut_admissible_assignments": examined, "rank_three": rank_three}


def rank_fraction(rows: list[list[int | Fraction]]) -> int:
    """Exact Gaussian rank over Q, independent of the primary implementation."""

    work = [[Fraction(entry) for entry in row] for row in rows]
    rank = 0
    columns = len(work[0]) if work else 0
    for column in range(columns):
        pivot = next(
            (index for index in range(rank, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [entry / pivot_value for entry in work[rank]]
        for index, row in enumerate(work):
            if index == rank or row[column] == 0:
                continue
            multiple = row[column]
            work[index] = [
                left - multiple * right
                for left, right in zip(row, work[rank], strict=True)
            ]
        rank += 1
    return rank


def compatibility_rows(labels: tuple[tuple[int, int, int], ...]) -> list[list[int]]:
    """Build the sharpness-triangle system without symbolic algebra."""

    rows = []
    for label_index, label in enumerate(labels):
        for row in range(3):
            for column in range(3):
                if row == column:
                    continue
                equation = [0] * (6 + len(labels))
                equation[row] = label[column]
                equation[3 + column] = label[row]
                equation[6 + label_index] = -1
                rows.append(equation)
    return rows


def locked_triangle_audit() -> dict[str, int]:
    labels = ((0, 1, 1), (1, 0, 1), (1, 1, 0))
    two_mate_ranks = []
    for omitted in range(3):
        mates = tuple(label for index, label in enumerate(labels) if index != omitted)
        rank = rank_fraction(compatibility_rows(mates))
        assert rank == 7
        two_mate_ranks.append(rank)
    full_rank = rank_fraction(compatibility_rows(labels))
    assert full_rank == 9
    return {"two_mate_rank_sum": sum(two_mate_ranks), "three_mate_rank": full_rank}


def main() -> None:
    factors = reducibility_census()
    zero_products = zero_product_census()
    cuts = cut_subspace_census()
    tangent = locked_triangle_audit()
    print("GLS46 independent no-import structural audit: PASS")
    print("  F3 determinant-cubic linear factors:", factors)
    print("  F3 labelled zero products:", zero_products)
    print("  F2 cut-subspace assignments:", cuts)
    print("  custom-Q tangent ranks:", tangent)
    print("  finite audits are not the characteristic-zero proof")
    print("  rank-four full-swallow and global Krenn-Gu: UNRESOLVED")


if __name__ == "__main__":
    main()
