#!/usr/bin/env python3
"""Independent finite-field audit of the transverse boundary classification."""

from __future__ import annotations

import itertools
import json

P = 5
VERTICES = tuple(range(5))
EDGES = tuple(itertools.combinations(VERTICES, 2))


def rank_mod(rows: list[list[int]]) -> int:
    matrix = [[value % P for value in row] for row in rows]
    rank = 0
    columns = len(matrix[0]) if matrix else 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, P)
        matrix[rank] = [(inverse * value) % P for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank:
                continue
            factor = matrix[row][column]
            if factor:
                matrix[row] = [
                    (left - factor * right) % P
                    for left, right in zip(matrix[row], matrix[rank], strict=True)
                ]
        rank += 1
    return rank


def regular_tournaments() -> list[dict[tuple[int, int], int]]:
    records = []
    for choices in itertools.product((0, 1), repeat=len(EDGES)):
        heads = {edge: edge[choice] for edge, choice in zip(EDGES, choices, strict=True)}
        if all(sum(head == vertex for head in heads.values()) == 2 for vertex in VERTICES):
            records.append(heads)
    assert len(records) == 24
    return records


def tournament_matrix(heads: dict[tuple[int, int], int]) -> list[list[int]]:
    incoming = {
        vertex: sorted(edge for edge, head in heads.items() if head == vertex)
        for vertex in VERTICES
    }
    rows = []
    for edge in EDGES:
        row = [0] * 10
        head = heads[edge]
        slot = incoming[head].index(edge)
        row[2 * head + slot] = 1
        rows.append(row)
    return rows


def normalized_projective_vectors() -> list[tuple[int, int, int]]:
    vectors = []
    for vector in itertools.product(range(P), repeat=3):
        if vector == (0, 0, 0):
            continue
        first = next(value for value in vector if value)
        inverse = pow(first, -1, P)
        normalized = tuple((inverse * value) % P for value in vector)
        if normalized not in vectors:
            vectors.append(normalized)
    assert len(vectors) == P * P + P + 1
    return vectors


def main() -> None:
    tournaments = regular_tournaments()
    for heads in tournaments:
        assert rank_mod(tournament_matrix(heads)) == 10

    # If all incident gradients at one mode lie on one line, the tangent
    # supported on the complementary local direction is an explicit kernel.
    rank_one_tests = 0
    base = tournament_matrix(tournaments[0])
    for vertex in VERTICES:
        rows = [row[:] for row in base]
        coefficient = 1
        for edge_index, edge in enumerate(EDGES):
            if vertex in edge:
                rows[edge_index][2 * vertex] = coefficient % P
                rows[edge_index][2 * vertex + 1] = 0
                coefficient += 1
        assert rank_mod(rows) <= 9
        assert all(row[2 * vertex + 1] == 0 for row in rows)
        rank_one_tests += 1

    projective = normalized_projective_vectors()
    membership_checks = 0
    for x in projective:
        annihilator = [
            list(a)
            for a in itertools.product(range(P), repeat=3)
            if sum(left * right for left, right in zip(a, x, strict=True)) % P == 0
        ]
        assert rank_mod(annihilator) == 2
        for colour in range(3):
            coordinate = [0, 0, 0]
            coordinate[colour] = 1
            membership = rank_mod(annihilator) == rank_mod(annihilator + [coordinate])
            assert membership == (x[colour] == 0)
            membership_checks += 1

    print(
        json.dumps(
            {
                "audited": True,
                "field": "F_5",
                "regular_tournaments": len(tournaments),
                "full_rank_tournament_jacobians": len(tournaments),
                "rank_one_local_span_tests": rank_one_tests,
                "projective_points": len(projective),
                "coordinate_membership_checks": membership_checks,
                "formula_audit_only": True,
                "coordinate_boundary_excluded": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
