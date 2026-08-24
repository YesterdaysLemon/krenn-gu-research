"""Focused exact checks for GLS59.

The written proof carries the characteristic-zero theorem.  This verifier
checks the covector alternative, the complete-matching probe-exchange kill,
the five-label overlap classification, and exact full eight-to-six-vertex
controls for the binary and monocolour descent endpoints.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import cache
from itertools import permutations, product

import sympy as sp

Vector = tuple[Fraction, Fraction, Fraction]
Matrix = tuple[tuple[Fraction, Fraction, Fraction], ...]
Matching = tuple[tuple[int, int], ...]

ZERO_VECTOR: Vector = (Fraction(0), Fraction(0), Fraction(0))
ZERO_MATRIX: Matrix = (ZERO_VECTOR, ZERO_VECTOR, ZERO_VECTOR)


def basis(colour: int) -> Vector:
    return tuple(Fraction(int(index == colour)) for index in range(3))  # type: ignore[return-value]


def unit(row: int, column: int, value: int = 1) -> Matrix:
    return tuple(
        tuple(Fraction(value if (i, j) == (row, column) else 0) for j in range(3))
        for i in range(3)
    )


def transpose(matrix: Matrix) -> Matrix:
    return tuple(
        tuple(matrix[row][column] for row in range(3))
        for column in range(3)
    )


def matrix_add(*matrices: Matrix) -> Matrix:
    return tuple(
        tuple(sum(matrix[row][column] for matrix in matrices) for column in range(3))
        for row in range(3)
    )


def matrix_scale(value: Fraction, matrix: Matrix) -> Matrix:
    return tuple(tuple(value * entry for entry in row) for row in matrix)


def outer(left: Vector, right: Vector) -> Matrix:
    return tuple(tuple(x * y for y in right) for x in left)


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(3))
        for row in range(3)
    )  # type: ignore[return-value]


def left_contract(vector: Vector, matrix: Matrix) -> Vector:
    return tuple(
        sum(vector[row] * matrix[row][column] for row in range(3))
        for column in range(3)
    )  # type: ignore[return-value]


def bilinear(left: Vector, matrix: Matrix, right: Vector) -> Fraction:
    return sum(x * y for x, y in zip(left, matvec(matrix, right), strict=True))


def edge_matrix(
    edges: dict[tuple[int, int], Matrix], left: int, right: int
) -> Matrix:
    if left < right:
        return edges.get((left, right), ZERO_MATRIX)
    return transpose(edges.get((right, left), ZERO_MATRIX))


@cache
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    result: list[Matching] = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            result.append(((first, second),) + tail)
    return tuple(result)


def matching_coefficient(
    vertices: tuple[int, ...],
    local_vectors: dict[int, Vector],
    edges: dict[tuple[int, int], Matrix],
) -> Fraction:
    total = Fraction(0)
    for matching in perfect_matchings(vertices):
        value = Fraction(1)
        for left, right in matching:
            value *= bilinear(
                local_vectors[left], edge_matrix(edges, left, right), local_vectors[right]
            )
        total += value
    return total


def sparse_matching_tensor(
    vertices: tuple[int, ...], edges: dict[tuple[int, int], Matrix]
) -> Counter[tuple[int, ...]]:
    coefficients: Counter[tuple[int, ...]] = Counter()
    position = {vertex: index for index, vertex in enumerate(vertices)}
    for matching in perfect_matchings(vertices):
        entries_by_edge: list[tuple[tuple[int, int, Fraction], ...]] = []
        for left, right in matching:
            matrix = edge_matrix(edges, left, right)
            entries = tuple(
                (row, column, matrix[row][column])
                for row in range(3)
                for column in range(3)
                if matrix[row][column]
            )
            if not entries:
                break
            entries_by_edge.append(entries)
        else:
            for choices in product(*entries_by_edge):
                word = [-1] * len(vertices)
                value = Fraction(1)
                for (left, right), (row, column, entry) in zip(
                    matching, choices, strict=True
                ):
                    word[position[left]] = row
                    word[position[right]] = column
                    value *= entry
                coefficients[tuple(word)] += value
    return +coefficients


def matrix_rank(rows: tuple[Vector, ...]) -> int:
    return int(sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in row] for row in rows]).rank())


def joint_rank(edges: dict[tuple[int, int], Matrix], label: int) -> int:
    rows = edge_matrix(edges, 0, label) + edge_matrix(edges, 1, label)
    return matrix_rank(rows)


def image_axis(matrix: Matrix) -> int | None:
    columns = {
        column
        for row in range(3)
        for column in range(3)
        if matrix[row][column]
    }
    if len(columns) == 1:
        return next(iter(columns))
    return None


def vector_axis(vector: Vector) -> int | None:
    support = [index for index, value in enumerate(vector) if value]
    if len(support) == 1:
        return support[0]
    return None


def audit_covector_alternative() -> dict[str, int]:
    prime = 5
    vectors = tuple(product(range(prime), repeat=3))
    cases = 0
    pure_obstructions = 0
    witnesses = 0
    for colour in range(3):
        for covector in vectors:
            cases += 1
            surviving = [
                vector
                for vector in vectors
                if sum(covector[index] * vector[index] for index in range(3)) % prime == 0
                and vector[colour]
            ]
            pure = (
                covector[colour] != 0
                and all(covector[index] == 0 for index in range(3) if index != colour)
            )
            assert bool(surviving) != pure
            pure_obstructions += int(pure)
            witnesses += len(surviving)
    assert cases == 375
    assert pure_obstructions == 12
    assert witnesses == 7500
    return {
        "F5_covector_colour_cases": cases,
        "F5_nonzero_pure_obstructions": pure_obstructions,
        "F5_kernel_coordinate_witnesses": witnesses,
    }


def audit_probe_exchange_matching_kill() -> dict[str, int]:
    # Vertices: old probes 0,1; silent auxiliary n=2; five other auxiliaries.
    matchings = perfect_matchings(tuple(range(8)))
    partner_counts: Counter[str] = Counter()
    per_other: Counter[int] = Counter()
    for matching in matchings:
        edge = next(edge for edge in matching if 0 in edge)
        partner = edge[0] if edge[1] == 0 else edge[1]
        if partner == 1:
            partner_counts["zero_anchor"] += 1
        elif partner == 2:
            partner_counts["joint_kernel"] += 1
        else:
            partner_counts["chosen_edge_kernel"] += 1
            per_other[partner] += 1
    assert len(matchings) == 105
    assert partner_counts == Counter(
        zero_anchor=15, joint_kernel=15, chosen_edge_kernel=75
    )
    assert per_other == Counter({3: 15, 4: 15, 5: 15, 6: 15, 7: 15})
    return {
        "eight_vertex_matchings": len(matchings),
        "anchor_killed": partner_counts["zero_anchor"],
        "joint_kernel_killed": partner_counts["joint_kernel"],
        "chosen_edge_kernel_killed": partner_counts["chosen_edge_kernel"],
    }


def audit_five_label_probe_star_overlap() -> dict[str, int]:
    labels = tuple(range(5))
    stars = tuple(permutations(labels, 3))
    cases = 0
    same_colour_overlaps = 0
    cross_colour_overlaps = 0
    minimum_overlap = 5
    for left in stars:
        for right in stars:
            cases += 1
            overlap = set(left) & set(right)
            minimum_overlap = min(minimum_overlap, len(overlap))
            assert overlap
            for label in overlap:
                left_colour = left.index(label)
                right_colour = right.index(label)
                if left_colour == right_colour:
                    same_colour_overlaps += 1
                    rows = (basis(left_colour), basis(right_colour))
                    assert matrix_rank(rows) == 1
                else:
                    cross_colour_overlaps += 1
                    rows = (basis(left_colour), basis(right_colour))
                    assert matrix_rank(rows) == 2
    assert len(stars) == 60
    assert cases == 3600
    assert minimum_overlap == 1
    assert same_colour_overlaps + cross_colour_overlaps == 6480
    return {
        "ordered_probe_star_pairs": cases,
        "minimum_label_overlap": minimum_overlap,
        "same_colour_overlap_occurrences": same_colour_overlaps,
        "cross_colour_overlap_occurrences": cross_colour_overlaps,
    }


def make_control(kind: str) -> tuple[dict[tuple[int, int], Matrix], Vector, Vector, set[int]]:
    # Vertices: probes 0,1; unique nonrigid n=2; overlap t=3; ports 4..7.
    edges: dict[tuple[int, int], Matrix] = {(0, 1): ZERO_MATRIX}
    k = (Fraction(1), Fraction(1), Fraction(1))
    if kind == "same":
        ell = (Fraction(0), Fraction(1), Fraction(1))
        edges.update(
            {
                (0, 3): unit(0, 0),
                (1, 3): unit(0, 0),
                (0, 4): unit(1, 1),
                (1, 5): unit(1, 1),
                (1, 6): unit(2, 2),
                (0, 7): unit(2, 2),
                (2, 3): unit(0, 0),
                (2, 4): unit(0, 2),
                (2, 6): unit(0, 1),
                (3, 5): unit(1, 2),
                (3, 7): unit(1, 1),
            }
        )
        target_colours = {1, 2}
    elif kind == "cross":
        ell = basis(2)
        edges.update(
            {
                (0, 3): unit(0, 0),
                (1, 3): unit(1, 1),
                (0, 4): unit(1, 1),
                (0, 5): unit(2, 2),
                (1, 6): unit(0, 0),
                (1, 7): unit(2, 2),
                (2, 3): unit(0, 0),
                (2, 4): unit(0, 2),
                (2, 6): unit(0, 1),
                (3, 6): unit(2, 2),
            }
        )
        target_colours = {2}
    else:
        raise ValueError(kind)
    return edges, k, ell, target_colours


def effective_six_vertex_edges(
    edges: dict[tuple[int, int], Matrix], k: Vector, ell: Vector
) -> dict[tuple[int, int], Matrix]:
    ports = (4, 5, 6, 7)
    effective: dict[tuple[int, int], Matrix] = {(0, 1): ZERO_MATRIX}
    for probe in (0, 1):
        for port in ports:
            effective[(probe, port)] = edge_matrix(edges, probe, port)
    h = bilinear(k, edge_matrix(edges, 2, 3), ell)
    shores_n = {port: left_contract(k, edge_matrix(edges, 2, port)) for port in ports}
    shores_t = {port: left_contract(ell, edge_matrix(edges, 3, port)) for port in ports}
    for index, left in enumerate(ports):
        for right in ports[index + 1 :]:
            effective[(left, right)] = matrix_add(
                matrix_scale(h, edge_matrix(edges, left, right)),
                outer(shores_n[left], shores_t[right]),
                outer(shores_t[left], shores_n[right]),
            )
    return effective


def audit_control(kind: str) -> dict[str, int]:
    edges, k, ell, target_colours = make_control(kind)
    assert matvec(edge_matrix(edges, 0, 2), k) == ZERO_VECTOR
    assert matvec(edge_matrix(edges, 1, 2), k) == ZERO_VECTOR
    assert matvec(edge_matrix(edges, 0, 3), ell) == ZERO_VECTOR
    assert matvec(edge_matrix(edges, 1, 3), ell) == ZERO_VECTOR

    ranks = {label: joint_rank(edges, label) for label in range(2, 8)}
    expected_t_rank = 1 if kind == "same" else 2
    assert ranks[2] == 0
    assert ranks[3] == expected_t_rank
    assert all(ranks[label] == 1 for label in range(4, 8))

    root_zero_star = {
        image_axis(edge_matrix(edges, 0, label)): label
        for label in range(3, 8)
        if image_axis(edge_matrix(edges, 0, label)) is not None
    }
    root_one_star = {
        image_axis(edge_matrix(edges, 1, label)): label
        for label in range(3, 8)
        if image_axis(edge_matrix(edges, 1, label)) is not None
    }
    assert set(root_zero_star) == {0, 1, 2}
    assert set(root_one_star) == {0, 1, 2}
    assert root_zero_star[0] == 3
    assert root_one_star[0 if kind == "same" else 1] == 3

    n_star = {
        vector_axis(left_contract(k, edge_matrix(edges, 2, label))): label
        for label in range(3, 8)
        if vector_axis(left_contract(k, edge_matrix(edges, 2, label))) is not None
    }
    assert set(n_star) == {0, 1, 2}

    effective = effective_six_vertex_edges(edges, k, ell)
    open_vertices = (0, 1, 4, 5, 6, 7)
    dense_checks = 0
    for word in product(range(3), repeat=6):
        local_vectors = {vertex: basis(colour) for vertex, colour in zip(open_vertices, word, strict=True)}
        full_vectors = dict(local_vectors)
        full_vectors[2] = k
        full_vectors[3] = ell
        full_value = matching_coefficient(tuple(range(8)), full_vectors, edges)
        effective_value = matching_coefficient(open_vertices, local_vectors, effective)
        assert full_value == effective_value
        expected = Fraction(1) if len(set(word)) == 1 and word[0] in target_colours else Fraction(0)
        assert effective_value == expected
        dense_checks += 1

    tensor = sparse_matching_tensor(open_vertices, effective)
    expected_tensor = Counter({(colour,) * 6: Fraction(1) for colour in target_colours})
    assert tensor == expected_tensor
    return {
        f"{kind}_joint_rank_n": ranks[2],
        f"{kind}_joint_rank_t": ranks[3],
        f"{kind}_rigid_other_labels": sum(ranks[label] > 0 for label in range(3, 8)),
        f"{kind}_dense_eight_to_six_checks": dense_checks,
        f"{kind}_target_colours": len(target_colours),
        f"{kind}_supported_words": len(tensor),
    }


def audit_low_activity_shortage() -> dict[str, int]:
    labels = set(range(5))
    star_triples = tuple(permutations(labels, 3))
    cases = 0
    for natural_star in star_triples:
        silent = set(natural_star)
        available = labels - silent
        assert len(available) == 2
        # Three distinct nonzero pure probe neighbours cannot avoid the three
        # labels whose evaluated probe shores have been forced to zero.
        assert not any(set(candidate) <= available for candidate in star_triples)
        cases += 1
    assert cases == 60
    return {
        "natural_star_labelings": cases,
        "remaining_labels_after_diagonal_silence": 2,
    }


def main() -> None:
    results: dict[str, int] = {}
    for audit in (
        audit_covector_alternative,
        audit_probe_exchange_matching_kill,
        audit_five_label_probe_star_overlap,
        audit_low_activity_shortage,
    ):
        results.update(audit())
    results.update(audit_control("same"))
    results.update(audit_control("cross"))
    for key in sorted(results):
        print(f"{key}={results[key]}")
    print("GLS59 focused exact verifier: PASS")


if __name__ == "__main__":
    main()
