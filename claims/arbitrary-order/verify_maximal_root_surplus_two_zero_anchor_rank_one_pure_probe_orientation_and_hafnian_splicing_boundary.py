"""Focused exact checks for the GLS60 orientation/splicing boundary.

The written proof carries the characteristic-zero theorem.  This verifier
checks its polynomial identities, matching expansions, sharp controls, and
the permanent-versus-hafnian arity boundary with exact arithmetic.
"""

from __future__ import annotations

import itertools
import json
from functools import lru_cache

import sympy as sp


COLORS = range(3)
LABELS = tuple(range(6))
KAPPA = (0, 0, 1, 1, 2, 2)
PAIRS = tuple(itertools.combinations(LABELS, 2))
E = tuple(tuple(1 if i == j else 0 for j in COLORS) for i in COLORS)


@lru_cache(maxsize=None)
def matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    out = []
    for pos in range(1, len(vertices)):
        second = vertices[pos]
        tail = vertices[1:pos] + vertices[pos + 1 :]
        for rest in matchings(tail):
            out.append(((first, second),) + rest)
    return tuple(out)


def outer(u: tuple[int, ...], v: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(a * b for b in v) for a in u)


def add_matrix(*matrices: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(sum(matrix[i][j] for matrix in matrices) for j in COLORS)
        for i in COLORS
    )


def dense_edge(i: int, j: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple((i + 2) * (j + 3) + (c + 1) * (d + 2) + i * d - j * c for d in COLORS)
        for c in COLORS
    )


def dense_direction(i: int, j: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple((i + 1) * (c + 2) - (j + 2) * (d + 1) + c * d + 1 for d in COLORS)
        for c in COLORS
    )


def hafnian_coefficient(
    edges: dict[tuple[int, int], tuple[tuple[int, ...], ...]],
    vertices: tuple[int, ...],
    word: tuple[int, ...],
) -> int:
    total = 0
    for matching in matchings(vertices):
        term = 1
        for i, j in matching:
            term *= edges[(i, j)][word[i]][word[j]]
        total += term
    return total


def first_variation_coefficient(
    w_edges: dict[tuple[int, int], tuple[tuple[int, ...], ...]],
    theta_edges: dict[tuple[int, int], tuple[tuple[int, ...], ...]],
    word: tuple[int, ...],
) -> int:
    total = 0
    for i, j in PAIRS:
        complement = tuple(v for v in LABELS if v not in (i, j))
        total += theta_edges[(i, j)][word[i]][word[j]] * hafnian_coefficient(
            w_edges, complement, word
        )
    return total


def poly_mul(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return out


def deformed_linear_coefficient(
    w_edges: dict[tuple[int, int], tuple[tuple[int, ...], ...]],
    theta_edges: dict[tuple[int, int], tuple[tuple[int, ...], ...]],
    word: tuple[int, ...],
) -> int:
    total = 0
    for matching in matchings(LABELS):
        polynomial = [1]
        for i, j in matching:
            polynomial = poly_mul(
                polynomial,
                [w_edges[(i, j)][word[i]][word[j]], theta_edges[(i, j)][word[i]][word[j]]],
            )
        total += polynomial[1]
    return total


def verify_cauchy_binet_orientation() -> dict[str, int]:
    x = sp.Matrix(3, 2, sp.symbols("x0:6"))
    y = sp.Matrix(3, 2, sp.symbols("y0:6"))
    swap = sp.Matrix([[0, 1], [1, 0]])
    product = x * swap * y.T
    checks = 0
    for rows in itertools.combinations(range(3), 2):
        for cols in itertools.combinations(range(3), 2):
            lhs = product.extract(rows, cols).det()
            rhs = -x.extract(rows, range(2)).det() * y.extract(cols, range(2)).det()
            assert sp.expand(lhs - rhs) == 0
            checks += 1

    a, b, alpha, beta, r1, r2 = sp.symbols("a b alpha beta r1 r2")
    e0 = sp.Matrix([1, 0, 0])
    transverse = sp.Matrix([0, r1, r2])
    xs = a * e0
    xt = b * e0
    ys = alpha * e0 + a * transverse
    yt = beta * e0 - b * transverse
    normal = xs * yt.T + xt * ys.T
    assert normal == (a * beta + b * alpha) * (e0 * e0.T)

    # The alternatives are sharp: neither shore is forced to be the pure one.
    e1 = sp.Matrix([0, 1, 0])
    x_only = e0 * (e0 - e1).T + e0 * e1.T
    y_only = (e0 - e1) * e0.T + e1 * e0.T
    assert x_only == e0 * e0.T
    assert y_only == e0 * e0.T
    assert sp.Matrix.hstack(e0, e0).rank() == 1
    assert sp.Matrix.hstack(e1, e0 - e1).rank() == 2
    assert sp.Matrix.hstack(e1, e0 - e1).rank() == 2
    assert sp.Matrix.hstack(e0, e0).rank() == 1
    return {"cauchy_binet_minors": checks, "normal_forms": 3}


def companion_fixture() -> tuple[
    dict[tuple[int, int], tuple[tuple[int, ...], ...]], dict[str, int]
]:
    x = (
        (1, 0, 0),
        (1, 0, 0),
        (0, 1, 0),
        (0, 1, 0),
        (0, 0, 0),
        (0, 0, 1),
    )
    y = (
        (0, 0, 0),
        (1, 0, 0),
        (0, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (0, 0, 1),
    )
    for i in LABELS:
        assert any(x[i]) or any(y[i])
    for c, (s, t) in enumerate(((0, 1), (2, 3), (4, 5))):
        target = tuple(tuple(1 if (i, j) == (c, c) else 0 for j in COLORS) for i in COLORS)
        assert add_matrix(outer(x[s], y[t]), outer(x[t], y[s])) == target

    z0 = z1 = (1, 1, 1)
    x_eval = tuple(sum(u * v for u, v in zip(row, z0)) for row in x)
    y_eval = tuple(sum(u * v for u, v in zip(row, z1)) for row in y)
    theta_edges = {}
    for i, j in PAIRS:
        scalar = x_eval[i] * y_eval[j] + x_eval[j] * y_eval[i]
        theta_edges[(i, j)] = tuple(
            tuple(
                scalar if (c, d) == (KAPPA[i], KAPPA[j]) else 0
                for d in COLORS
            )
            for c in COLORS
        )

    support = {}
    for word in itertools.product(COLORS, repeat=6):
        value = hafnian_coefficient(theta_edges, LABELS, word)
        if value:
            support[word] = value
    assert support == {KAPPA: 18}
    companion_flattening = sp.zeros(3, 3**5)
    target_flattening = sp.zeros(3, 3**5)
    for word, value in support.items():
        column = sum(word[pos] * 3 ** (5 - pos) for pos in range(1, 6))
        companion_flattening[word[0], column] = value
    for c in COLORS:
        target_flattening[c, sum(c * 3 ** (5 - pos) for pos in range(1, 6))] = 1
    assert companion_flattening.rank() == 1
    assert target_flattening.rank() == 3
    return theta_edges, {
        "companion_graph_support_words": len(support),
        "companion_graph_mixed_coefficient": support[KAPPA],
        "companion_graph_flattening_rank": companion_flattening.rank(),
        "three_colour_target_flattening_rank": target_flattening.rank(),
    }


def verify_first_variation_and_gauge() -> dict[str, int]:
    w_edges = {(i, j): dense_edge(i, j) for i, j in PAIRS}
    theta_edges = {(i, j): dense_direction(i, j) for i, j in PAIRS}
    coefficient_checks = 0
    for word in itertools.product(COLORS, repeat=6):
        assert first_variation_coefficient(w_edges, theta_edges, word) == deformed_linear_coefficient(
            w_edges, theta_edges, word
        )
        coefficient_checks += 1

    gauge_checks = 0
    for weights in ((-2, -1, 0, 1, 3, 4), (-2, -1, 0, 1, 3, -1)):
        gauge = {
            (i, j): tuple(
                tuple((weights[i] + weights[j]) * w_edges[(i, j)][c][d] for d in COLORS)
                for c in COLORS
            )
            for i, j in PAIRS
        }
        trace = sum(weights)
        for word in itertools.product(COLORS, repeat=6):
            lhs = first_variation_coefficient(w_edges, gauge, word)
            rhs = trace * hafnian_coefficient(w_edges, LABELS, word)
            assert lhs == rhs
            gauge_checks += 1
    return {"first_variation_coefficients": coefficient_checks, "gauge_coefficients": gauge_checks}


def verify_matching_and_tensor_type_censuses() -> dict[str, int]:
    matchings_six = len(matchings(tuple(range(6))))
    matchings_eight = len(matchings(tuple(range(8))))
    zero_anchor_root_edge = len(matchings(tuple(range(6))))
    surviving_eight = matchings_eight - zero_anchor_root_edge
    pointed_six = len(PAIRS) * len(matchings(tuple(range(4))))
    assert (matchings_six, matchings_eight, zero_anchor_root_edge, surviving_eight, pointed_six) == (
        15,
        105,
        15,
        90,
        45,
    )
    assert surviving_eight == 2 * pointed_six
    permanent_monomials = sum(1 for _ in itertools.permutations(range(6)))
    assert permanent_monomials == 720
    return {
        "six_vertex_hafnian_monomials": matchings_six,
        "eight_vertex_matchings": matchings_eight,
        "zero_anchor_survivors": surviving_eight,
        "pointed_six_matchings": pointed_six,
        "p6_permanent_monomials": permanent_monomials,
    }


def main() -> None:
    report = {
        "verified": True,
        "orientation": verify_cauchy_binet_orientation(),
        "first_variation": verify_first_variation_and_gauge(),
        "censuses": verify_matching_and_tensor_type_censuses(),
    }
    _, fixture_report = companion_fixture()
    report["companion_graph"] = fixture_report
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
