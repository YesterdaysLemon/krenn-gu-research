#!/usr/bin/env python3
"""Verify the star- and path-support directed-triangle P4 components."""

from __future__ import annotations

import itertools
import json

import sympy as sp


WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
PAIRS = tuple(itertools.combinations(range(4), 2))


def permanent(rows) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def coefficients(planes) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: sp.factor(
            permanent(tuple(planes[mode].row(word[mode]) for mode in range(4)))
        )
        for word in WORDS
    }


def product(left, right) -> sp.Matrix:
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def pair_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(product(left.row(i), right.row(j)) for i in range(2) for j in range(2))
    )


def triple_covectors(planes) -> dict[tuple[int, ...], sp.Matrix]:
    identity = sp.eye(4)
    return {
        bits: sp.Matrix(
            [[
                permanent(
                    (
                        identity.row(coordinate),
                        planes[0].row(bits[0]),
                        planes[1].row(bits[1]),
                        planes[2].row(bits[2]),
                    )
                )
                for coordinate in range(4)
            ]]
        )
        for bits in itertools.product((0, 1), repeat=3)
    }


def raw_family(kind: str, u: sp.Expr, v: sp.Expr):
    a = sp.Matrix([[1, 0, 1, 0]])
    a_bar = sp.Matrix([[1, 0, -1, 0]])
    b = sp.Matrix([[0, 1, 1, 0]])
    b_bar = sp.Matrix([[0, 1, -1, 0]])
    c = sp.Matrix([[0, 0, 1, 1]])
    c_bar = sp.Matrix([[0, 0, 1, -1]])
    d = sp.Matrix([[1, 1, 0, 0]])
    d_bar = sp.Matrix([[1, -1, 0, 0]])

    if kind == "star":
        u_0 = sp.Matrix(((1 - u, 1, 0, u), (1 - v, 0, 1, v)))
        triangle = (
            sp.Matrix.vstack(b, c),
            sp.Matrix.vstack(a_bar, b_bar),
            sp.Matrix.vstack(c_bar, a),
        )
    elif kind == "path":
        u_0 = sp.Matrix(((-1 - u, 1, 0, u), (1 - v, 0, 1, v)))
        triangle = (
            sp.Matrix.vstack(d, c),
            sp.Matrix.vstack(a_bar, d_bar),
            sp.Matrix.vstack(c_bar, a),
        )
    else:
        raise ValueError(kind)
    return (u_0, *triangle)


PIVOTS = {
    "star": ((0, 1), (1, 2), (0, 1), (0, 2)),
    "path": ((0, 1), (0, 2), (0, 1), (0, 2)),
}


def reduce_in_charts(planes, pivots):
    return tuple(sp.simplify(plane[:, pivot].inv() * plane) for plane, pivot in zip(planes, pivots, strict=True))


def chart_coordinates(planes, pivots):
    result = []
    for plane, pivot in zip(planes, pivots, strict=True):
        nonpivots = tuple(index for index in range(4) if index not in pivot)
        result.extend(
            plane[row, column]
            for row in range(2)
            for column in nonpivots
        )
    return tuple(result)


def chart_planes(variables, pivots):
    result = []
    for mode, pivot in enumerate(pivots):
        nonpivots = tuple(index for index in range(4) if index not in pivot)
        plane = sp.zeros(2, 4)
        plane[0, pivot[0]] = 1
        plane[1, pivot[1]] = 1
        entries = variables[4 * mode : 4 * mode + 4]
        for row in range(2):
            for offset, column in enumerate(nonpivots):
                plane[row, column] = entries[2 * row + offset]
        result.append(plane)
    return tuple(result)


def support_degrees(labels):
    degrees = [0, 0, 0, 0]
    for left, right in labels:
        degrees[left] += 1
        degrees[right] += 1
    return tuple(sorted(degrees, reverse=True))


def component_certificate(kind: str):
    u, v, t_0, t_1, t_2 = sp.symbols(f"u_{kind} v_{kind} t0_{kind} t1_{kind} t2_{kind}")
    parameters = (u, v, t_0, t_1, t_2)
    source_scale = sp.diag(t_0, t_1, t_2, 1)
    planes = tuple(plane * source_scale for plane in raw_family(kind, u, v))
    pivots = PIVOTS[kind]
    reduced = reduce_in_charts(planes, pivots)
    coordinates = chart_coordinates(reduced, pivots)
    sample = {u: 2, v: 3, t_0: 1, t_1: 1, t_2: 1}

    family_jacobian = sp.Matrix(coordinates).jacobian(parameters).subs(sample)
    family_rows = {
        "star": (0, 1, 2, 3, 5),
        "path": (0, 1, 2, 3, 4),
    }[kind]
    family_determinant = sp.factor(
        family_jacobian.extract(family_rows, range(5)).det()
    )
    expected_family_determinant = {
        "star": sp.Rational(1, 16),
        "path": sp.Rational(1, 8),
    }[kind]
    assert family_determinant == expected_family_determinant

    variables = tuple(sp.symbols(f"x_{kind}_0:16"))
    universal_planes = chart_planes(variables, pivots)
    tensor = coefficients(universal_planes)
    point = dict(
        zip(
            variables,
            (sp.factor(coordinate.subs(sample)) for coordinate in coordinates),
            strict=True,
        )
    )
    values = {word: sp.factor(value.subs(point)) for word, value in tensor.items()}
    anchor = {
        "star": (0, 0, 1, 0),
        "path": (0, 1, 1, 0),
    }[kind]
    assert values[anchor] != 0
    ratios = []
    for mode in range(4):
        flipped = list(anchor)
        flipped[mode] = 1 - flipped[mode]
        ratios.append(sp.factor(values[tuple(flipped)] / values[anchor]))
    expected_ratios = {
        "star": (1, -1, 0, 0),
        "path": (5, 0, 0, 0),
    }[kind]
    assert tuple(ratios) == expected_ratios

    z = tuple(sp.symbols(f"z_{kind}_0:4"))
    equations = []
    for word in WORDS:
        if word == anchor:
            continue
        target = sp.prod(z[mode] for mode in range(4) if word[mode] != anchor[mode])
        equations.append(sp.expand(tensor[word] - tensor[anchor] * target))
    incidence_point = point | dict(zip(z, ratios, strict=True))
    incidence_jacobian = sp.Matrix(equations).jacobian((*variables, *z)).subs(incidence_point)
    incidence_columns = {
        "star": (0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 18, 19),
        "path": (0, 1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 14, 17, 18, 19),
    }[kind]
    incidence_determinant = sp.factor(incidence_jacobian[:, incidence_columns].det())
    expected_incidence_determinant = {"star": -192, "path": 28800}[kind]
    assert incidence_determinant == expected_incidence_determinant

    return {
        "family_minor": str(family_determinant),
        "incidence_minor": str(incidence_determinant),
        "incidence_rank": incidence_jacobian.rank(),
        "local_dimension": 20 - incidence_jacobian.rank(),
    }


def main() -> None:
    u, v = sp.symbols("u v")
    expected_covectors = {
        "star": {
            (0, 0, 0): sp.Matrix([[1, -1, -1, 1]]),
            (1, 1, 1): sp.Matrix([[1, -1, 1, 1]]),
        },
        "path": {
            (0, 0, 0): sp.Matrix([[1, 1, -1, 1]]),
            (1, 1, 1): sp.Matrix([[-1, 1, -1, -1]]),
        },
    }
    expected_tensors = {
        "star": {(1, 1, 1, 1): 2},
        "path": {(0, 1, 1, 1): 2, (1, 1, 1, 1): -2},
    }
    expected_pair_minors = {
        "star": (
            2 * (u - 1) * (u - v),
            2 * u * v,
            2 * (v - 1),
        ),
        "path": (
            2 * u * (u + v + 1),
            2 * v * (u + v),
            2 * (v - 1),
        ),
    }
    pair_minor_rows = {
        "star": ((0, 1, 3, 5), (0, 1, 3, 4), (0, 1, 2, 3)),
        "path": ((0, 1, 3, 5), (0, 1, 2, 3), (0, 1, 2, 3)),
    }
    relation_vectors = (
        sp.Matrix([0, 1, 0, 0]),
        sp.Matrix([0, 0, 1, 0]),
        sp.Matrix([0, 1, 0, 0]),
    )

    results = {}
    for kind in ("star", "path"):
        planes = raw_family(kind, u, v)
        covectors = triple_covectors(planes[1:])
        for bits, covector in covectors.items():
            assert sp.simplify(
                covector - expected_covectors[kind].get(bits, sp.zeros(1, 4))
            ) == sp.zeros(1, 4)

        tensor = coefficients(planes)
        for word, value in tensor.items():
            assert sp.factor(value - expected_tensors[kind].get(word, 0)) == 0

        for offset, other_mode in enumerate((1, 2, 3)):
            matrix = pair_matrix(planes[0], planes[other_mode])
            rows = pair_minor_rows[kind][offset]
            determinant = sp.factor(matrix.extract(rows, range(4)).det())
            assert sp.factor(determinant - expected_pair_minors[kind][offset]) == 0

        for offset, (left, right) in enumerate(((1, 2), (1, 3), (2, 3))):
            matrix = pair_matrix(planes[left], planes[right])
            relation = relation_vectors[offset]
            assert matrix * relation == sp.zeros(6, 1)
            assert sp.Matrix(2, 2, tuple(relation)).rank() == 1
            assert matrix.rank() == 3

        sample = tuple(plane.subs({u: 2, v: 3}) for plane in planes)
        profile = tuple(
            pair_matrix(sample[left], sample[right]).rank() for left, right in PAIRS
        )
        assert profile == (4, 4, 4, 3, 3, 3)
        results[kind] = {
            "pair_profile": profile,
            **component_certificate(kind),
        }

    star_labels = ((1, 2), (2, 3), (0, 2))
    path_labels = ((0, 1), (2, 3), (0, 2))
    assert support_degrees(star_labels) == (3, 1, 1, 1)
    assert support_degrees(path_labels) == (2, 2, 1, 1)

    print(
        json.dumps(
            {
                "status": "pass",
                "components": results,
                "support_degree_sequences": {
                    "star": support_degrees(star_labels),
                    "path": support_degrees(path_labels),
                },
                "certified_component_lower_bound": 17,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
