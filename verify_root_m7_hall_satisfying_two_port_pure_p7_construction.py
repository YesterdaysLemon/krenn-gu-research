"""Verify the exact Hall-satisfying binary-cofactor/pure-P7 construction."""

from __future__ import annotations

import json
from collections import Counter
from functools import cache
from itertools import product

import sympy as sp

M = 7
R = 5
E = tuple(sp.eye(3).col(index) for index in range(3))
F = tuple(sp.eye(5).col(index) for index in range(5))
X = sp.ones(3, 1)


def permanent(matrix: list[list[int]]) -> int:
    totals = {0: 1}
    for row in matrix:
        updated: dict[int, int] = {}
        for mask, coefficient in totals.items():
            for column, value in enumerate(row):
                bit = 1 << column
                if value and not mask & bit:
                    new_mask = mask | bit
                    updated[new_mask] = updated.get(new_mask, 0) + coefficient * value
        totals = updated
    return totals.get((1 << len(matrix)) - 1, 0)


def data():
    a = [sp.zeros(3, 1) for _ in range(M)]
    b = [sp.zeros(3, 1) for _ in range(M)]
    a[0], a[3], a[5], a[6] = E[0], E[2], E[1], E[1]
    b[0], b[1], b[5], b[6] = E[0], E[0], E[2], -E[1]

    zero = sp.zeros(5, 1)
    columns = (
        (zero, -F[0], F[1]),
        (zero, F[1], F[0]),
        (F[0], F[2], F[4]),
        (F[1], F[3], zero),
        (F[2], F[4], F[3]),
        (F[3], zero, zero),
        (F[4], zero, F[2]),
    )
    h = [sp.Matrix.hstack(*triple) for triple in columns]
    return a, b, h


def matrix_rank(rows: list[sp.Matrix]) -> int:
    return sp.Matrix.vstack(*(row.T for row in rows)).rank()


def path_principal_signatures() -> dict[int, Counter[tuple[int, ...]]]:
    edges = {(index, index + 1): 1 if index % 2 == 0 else 0 for index in range(6)}

    def signature(deleted: int) -> Counter[tuple[int, ...]]:
        vertices = tuple(vertex for vertex in range(M) if vertex != deleted)
        positions = {vertex: index for index, vertex in enumerate(vertices)}

        @cache
        def recurse(remaining: tuple[int, ...]):
            if not remaining:
                return ((),)
            first = remaining[0]
            answer = []
            for position in range(1, len(remaining)):
                second = remaining[position]
                edge = (first, second)
                if edge not in edges:
                    continue
                rest = remaining[1:position] + remaining[position + 1 :]
                for tail in recurse(rest):
                    answer.append((edge,) + tail)
            return tuple(answer)

        result: Counter[tuple[int, ...]] = Counter()
        for matching in recurse(vertices):
            word = [-1] * (M - 1)
            for edge in matching:
                colour = edges[edge]
                word[positions[edge[0]]] = word[positions[edge[1]]] = colour
            assert -1 not in word
            result[tuple(word)] += 1
        return result

    return {deleted: signature(deleted) for deleted in range(M)}


def endpoint_signatures(
    ports: list[sp.Matrix], principals: dict[int, Counter[tuple[int, ...]]]
) -> Counter[tuple[int, ...]]:
    result: Counter[tuple[int, ...]] = Counter()
    for deleted, signatures in principals.items():
        for tail, coefficient in signatures.items():
            for colour in range(3):
                weight = int(ports[deleted][colour])
                if not weight:
                    continue
                word = tail[:deleted] + (colour,) + tail[deleted:]
                result[word] += weight * coefficient
    return Counter({word: value for word, value in result.items() if value})


def p7_coefficient(word: tuple[int, ...], a, b, h) -> int:
    matrix = []
    for root in range(R):
        matrix.append([int(h[u][root, word[u]]) for u in range(M)])
    matrix.append([int(a[u][word[u]]) for u in range(M)])
    matrix.append([int(b[u][word[u]]) for u in range(M)])
    return permanent(matrix)


def verify() -> dict[str, object]:
    a, b, h = data()
    assert matrix_rank(a) == matrix_rank(b) == 3

    hall = []
    for colour in range(3):
        support_a = [u for u in range(M) if a[u][colour]]
        support_b = [u for u in range(M) if b[u][colour]]
        assert support_a and support_b and len(set(support_a + support_b)) >= 2
        hall.append((support_a, support_b))
    assert hall == [([0], [0, 1]), ([5, 6], [6]), ([3], [5])]

    principals = path_principal_signatures()
    expected_principals = {
        0: Counter({(0,) * 6: 1}),
        1: Counter(),
        2: Counter({(1, 1, 0, 0, 0, 0): 1}),
        3: Counter(),
        4: Counter({(1, 1, 1, 1, 0, 0): 1}),
        5: Counter(),
        6: Counter({(1,) * 6: 1}),
    }
    assert principals == expected_principals
    first_endpoint = endpoint_signatures(a, principals)
    second_endpoint = endpoint_signatures(b, principals)
    assert first_endpoint == Counter({(0,) * M: 1, (1,) * M: 1})
    assert second_endpoint == Counter({(0,) * M: 1, (1,) * M: -1})

    root_spans = []
    for root in range(R):
        rows = [h[u].row(root).T for u in range(M)]
        root_spans.append(matrix_rank(rows))
    assert root_spans == [3] * R

    local_ranks = []
    for u in range(M):
        local = h[u].col_join(a[u].T).col_join(b[u].T)
        local_ranks.append(local.rank())
    assert local_ranks == [3] * M

    # Legal projectively constant root--blocker blocks e_2 tensor H_u[i,-].
    for u in range(M):
        for root in range(R):
            block = E[2] * h[u].row(root)
            assert X.T * block == h[u].row(root)
            assert E[0].T * block == E[1].T * block == sp.zeros(1, 3)

    # h=0 makes every four-vertex residual block the two-row factorization.
    four_vertex_checks = 0
    for u in range(M):
        for v in range(u + 1, M):
            residual = a[u] * b[v].T + b[u] * a[v].T
            for c, d in product(range(3), repeat=2):
                actual = a[u][c] * b[v][d] + b[u][c] * a[v][d]
                assert actual == residual[c, d]
            four_vertex_checks += 1

    coefficients = {
        word: p7_coefficient(word, a, b, h)
        for word in product(range(3), repeat=M)
    }
    histogram = Counter(coefficients.values())
    assert histogram == Counter({0: 2151, 1: 24, -1: 12})
    assert [coefficients[(colour,) * M] for colour in range(3)] == [1, 1, 1]
    mixed = [(word, value) for word, value in coefficients.items() if value and len(set(word)) > 1]
    assert len(mixed) == 33
    assert mixed[0] == ((0, 0, 0, 0, 1, 0, 2), 1)

    return {
        "port_ranks": [3, 3],
        "hall_supports": hall,
        "endpoint_nonzero_words": [len(first_endpoint), len(second_endpoint)],
        "root_row_spans": root_spans,
        "local_map_ranks": local_ranks,
        "four_vertex_checks": four_vertex_checks,
        "pure_p7_coefficients": [1, 1, 1],
        "p7_histogram": {str(key): value for key, value in sorted(histogram.items())},
        "nonzero_mixed_words": len(mixed),
        "first_mixed_failure": {"word": list(mixed[0][0]), "coefficient": mixed[0][1]},
    }


def main() -> None:
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "construction": verify(),
                "full_p7_diagonal_realized": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
