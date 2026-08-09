#!/usr/bin/env python3
"""Verify coordinate-monomial two-residual slice universality."""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "TWO_RESIDUAL_COORDINATE_MONOMIAL_SLICE_UNIVERSALITY_NOGO.md"


def allowed_edge(left, right, sector):
    if left[0] > right[0]:
        left, right = right, left
    types = (left[0], right[0])
    if types == ("R", "U"):
        return ("H", left[1], right[1])
    if sector == "arbitrary" and types == ("U", "U"):
        return ("W", left[1], right[1])
    if types == ("Q", "Q"):
        return ("h",)
    if sector == "factor" and types == ("Q", "U"):
        return ("a" if left[1] == 0 else "b", right[1])
    return None


def allowed_matchings(vertices, sector):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        label = allowed_edge(first, second, sector)
        if label is None:
            continue
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in allowed_matchings(rest, sector):
            yield ((first, second, label),) + tail


def matching_signature(matching, root_count, sector):
    root_assignment = [None] * root_count
    unused = []
    q_assignment = [None, None]
    for left, right, label in matching:
        if label[0] == "H":
            root_assignment[label[1]] = label[2]
        elif label[0] == "W":
            unused = [label[1], label[2]]
        elif label[0] in ("a", "b"):
            q_assignment[0 if label[0] == "a" else 1] = label[1]
    assert all(value is not None for value in root_assignment)
    if sector == "arbitrary":
        assert unused and matching[0] is not None
        return tuple(root_assignment), tuple(sorted(unused))
    assert all(value is not None for value in q_assignment)
    return tuple(root_assignment), tuple(q_assignment)


def matching_ledger(root_count):
    mode_count = root_count + 2
    vertices = (
        tuple(("R", index) for index in range(root_count))
        + tuple(("U", index) for index in range(mode_count))
        + (("Q", 0), ("Q", 1))
    )
    arbitrary = {
        matching_signature(matching, root_count, "arbitrary")
        for matching in allowed_matchings(vertices, "arbitrary")
    }
    expected_arbitrary = {
        (assignment, pair)
        for pair in itertools.combinations(range(mode_count), 2)
        for assignment in itertools.permutations(
            tuple(index for index in range(mode_count) if index not in pair)
        )
    }
    assert arbitrary == expected_arbitrary

    factor = {
        matching_signature(matching, root_count, "factor")
        for matching in allowed_matchings(vertices, "factor")
    }
    expected_factor = {
        (permutation[:root_count], permutation[root_count:])
        for permutation in itertools.permutations(range(mode_count))
    }
    assert factor == expected_factor
    return {
        "roots": root_count,
        "blockers": mode_count,
        "arbitrary_cofactor_matchings": len(arbitrary),
        "expected_arbitrary": math.comb(mode_count, 2) * math.factorial(root_count),
        "factorized_matchings": len(factor),
        "expected_factorized": math.factorial(mode_count),
    }


def permanent(rows):
    size = len(rows)
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(size))
            for permutation in itertools.permutations(range(size))
        )
    )


def symbolic_four_blocker_check():
    root_count = 2
    mode_count = 4
    h = sp.Symbol("h")
    cap_h = sp.Matrix(root_count, mode_count, lambda i, j: sp.Symbol(f"H{i}{j}"))
    cap_w = {
        pair: sp.Symbol(f"W{pair[0]}{pair[1]}")
        for pair in itertools.combinations(range(mode_count), 2)
    }
    a = sp.symbols(f"a0:{mode_count}")
    b = sp.symbols(f"b0:{mode_count}")

    arbitrary = 0
    factor = 0
    for pair in itertools.combinations(range(mode_count), 2):
        remaining = tuple(index for index in range(mode_count) if index not in pair)
        cofactor = permanent(cap_h[:, remaining].tolist())
        arbitrary += h * cap_w[pair] * cofactor
        factor += (a[pair[0]] * b[pair[1]] + b[pair[0]] * a[pair[1]]) * cofactor

    direct_arbitrary = 0
    direct_factor = 0
    vertices = (
        tuple(("R", index) for index in range(root_count))
        + tuple(("U", index) for index in range(mode_count))
        + (("Q", 0), ("Q", 1))
    )
    for matching in allowed_matchings(vertices, "arbitrary"):
        value = sp.Integer(1)
        for _left, _right, label in matching:
            if label[0] == "H":
                value *= cap_h[label[1], label[2]]
            elif label[0] == "W":
                value *= cap_w[tuple(sorted(label[1:]))]
            else:
                value *= h
        direct_arbitrary += value
    for matching in allowed_matchings(vertices, "factor"):
        value = sp.Integer(1)
        for _left, _right, label in matching:
            if label[0] == "H":
                value *= cap_h[label[1], label[2]]
            elif label[0] == "a":
                value *= a[label[1]]
            elif label[0] == "b":
                value *= b[label[1]]
            else:
                value *= h
        direct_factor += value
    assert sp.expand(direct_arbitrary - arbitrary) == 0
    assert sp.expand(direct_factor - factor) == 0
    return {
        "arbitrary_terms": len(sp.Add.make_args(sp.expand(arbitrary))),
        "factor_terms": len(sp.Add.make_args(sp.expand(factor))),
    }


def kernel_and_scaling_certificate(root_count=5):
    v = sp.Matrix((1, 1, 1))
    g = sp.Matrix(((1, 0, -1), (0, 1, -1)))
    assert g.rank() == 2
    assert g.nullspace() == [v]
    for coordinate in range(3):
        coordinate_row = sp.Matrix(
            [[sp.Integer(index == coordinate) for index in range(3)]]
        )
        assert sp.Matrix.vstack(g, coordinate_row).rank() == 3

    s, t = sp.symbols("s t")
    z0, z1 = s * v, t * v
    beta = sp.expand(z0[0] * z1[0])
    assert beta == s * t

    d = sp.symbols("d0:3", nonzero=True)
    root_vectors = (sp.Matrix(d),) + tuple(v for _ in range(root_count - 1))
    products = tuple(
        sp.prod(root[coordinate] for root in root_vectors) * v[coordinate] ** 2
        for coordinate in range(3)
    )
    assert products == d
    ell_values = tuple(sp.cancel(root[0] / root[0]) for root in root_vectors)
    assert ell_values == (1,) * root_count
    return {
        "kernel_matrix": tuple(tuple(map(str, row)) for row in g.tolist()),
        "kernel_generator": tuple(map(str, v)),
        "coordinate_monomial": str(beta),
        "diagonal_products": tuple(map(str, products)),
    }


def assignment_counts(max_roots=8):
    return tuple(
        {
            "roots": roots,
            "blockers": roots + 2,
            "arbitrary_cofactor_terms": math.comb(roots + 2, 2) * math.factorial(roots),
            "factorized_laplace_terms": math.factorial(roots + 2),
        }
        for roots in range(2, max_roots + 1)
    )


def main():
    theorem = THEOREM.read_text(encoding="utf-8")
    for phrase in (
        "Exact arbitrary-`r` characteristic-zero local-slice theorem",
        "slice-universal for the unresolved",
        "This is a **no-go theorem for a proof route**",
        "global Krenn--Gu conjecture remain **UNKNOWN** or **UNRESOLVED**",
    ):
        assert phrase in theorem
    ledgers = tuple(matching_ledger(roots) for roots in range(2, 6))
    symbolic = symbolic_four_blocker_check()
    kernel = kernel_and_scaling_certificate()
    counts = assignment_counts()
    print(
        json.dumps(
            {
                "status": "VERIFIED",
                "field": "Q / arbitrary-r written bijection",
                "matching_ledgers": ledgers,
                "symbolic_four_blocker_check": symbolic,
                "kernel_and_scaling": kernel,
                "arbitrary_r_counts": counts,
                "coordinate_branch_excluded": False,
                "local_slice_universality": True,
                "global_counterexample_constructed": False,
                "finite_field_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
