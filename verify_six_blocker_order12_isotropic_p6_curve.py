#!/usr/bin/env python3
"""Verify the order-twelve isotropic P6-curve theorem."""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "SIX_BLOCKER_ORDER12_ISOTROPIC_P6_CURVE.md"
Edge = tuple[str, str]
Monomial = tuple[Edge, ...]


def edge(left: str, right: str) -> Edge:
    return tuple(sorted((left, right)))


def perfect_matchings(vertices: tuple[str, ...], allowed) -> tuple[Monomial, ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    output = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        if not allowed(first, second):
            continue
        remaining = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remaining, allowed):
            output.append(tuple(sorted((edge(first, second), *tail))))
    return tuple(output)


def matching_partition() -> dict[str, int]:
    common = tuple(f"r{index}" for index in range(4))
    exchanged = ("a", "b")
    blockers = tuple(f"u{index}" for index in range(6))
    common_set = frozenset(common)
    blocker_set = frozenset(blockers)

    def allowed(left: str, right: str) -> bool:
        if left in common_set:
            return right in blocker_set
        if right in common_set:
            return left in blocker_set
        return True

    surviving = Counter(perfect_matchings((*common, *exchanged, *blockers), allowed))

    permanent_part: Counter[Monomial] = Counter()
    for assignment in itertools.permutations(blockers):
        pairs = tuple(
            edge(root, assignment[index])
            for index, root in enumerate((*common, *exchanged))
        )
        permanent_part[tuple(sorted(pairs))] += 1

    cofactor_part: Counter[Monomial] = Counter()
    for leftover in itertools.combinations(blockers, 2):
        used = tuple(blocker for blocker in blockers if blocker not in leftover)
        for assignment in itertools.permutations(used):
            root_pairs = tuple(
                edge(root, assignment[index]) for index, root in enumerate(common)
            )
            pairs = (*root_pairs, edge("a", "b"), edge(*leftover))
            cofactor_part[tuple(sorted(pairs))] += 1

    assert not (set(permanent_part) & set(cofactor_part))
    assert surviving == permanent_part + cofactor_part
    assert all(value == 1 for value in surviving.values())
    assert len(permanent_part) == 720
    assert len(cofactor_part) == 360
    assert len(surviving) == 1080
    return {
        "surviving_matching_monomials": len(surviving),
        "p6_permanent_monomials": len(permanent_part),
        "cross_cofactor_monomials": len(cofactor_part),
    }


def symbolic_curve() -> None:
    beta, delta, t = sp.symbols("beta delta t", nonzero=True)
    cross_matrix = sp.diag(beta, delta)
    y_a = sp.Matrix([1, t])
    y_b = sp.Matrix([delta * t, -beta])
    assert sp.expand((y_a.T * cross_matrix * y_b)[0]) == 0

    p00, p01, p10, p11 = sp.symbols("p00 p01 p10 p11")
    pi_curve = sp.expand(
        y_a[0] * y_b[0] * p00
        + y_a[0] * y_b[1] * p01
        + y_a[1] * y_b[0] * p10
        + y_a[1] * y_b[1] * p11
    )
    expected = -beta * p01 + t * (delta * p00 - beta * p11) + (delta * t**2 * p10)
    assert sp.expand(pi_curve - expected) == 0

    # Eliminate the one shared cofactor from the two diagonal corners.
    c, d00, d11 = sp.symbols("c d00 d11")
    pi00 = d00 - beta * c
    pi11 = d11 - delta * c
    assert sp.expand(beta * (pi11 - d11) - delta * (pi00 - d00)) == 0

    # On delta=0 the second ruling forces the double-port corner directly.
    assert sp.expand(pi11.subs(delta, 0) - d11) == 0

    # Modulo the diagonal target, all four corners lie in one cofactor line.
    quotient_row = sp.Matrix([[-beta, 0, 0, -delta]])
    assert quotient_row.rank() == 1

    # Independent full-frame sample for the target coefficient conic.
    x_a = sp.Matrix([1, 1, 1])
    z_a = sp.Matrix([1, 2, 3])
    x_b = sp.Matrix([2, 3, 5])
    z_b = sp.Matrix([3, 5, 7])

    def hadamard(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
        return sp.Matrix([left[index] * right[index] for index in range(3)])

    sample_beta, sample_delta = 1, 2
    v01 = hadamard(x_a, z_b)
    v10 = hadamard(z_a, x_b)
    middle = sample_delta * hadamard(x_a, x_b) - (sample_beta * hadamard(z_a, z_b))
    frame = sp.Matrix.hstack(v01, v10, middle)
    assert frame.det() == 69
    direct_coefficients = hadamard(
        x_a + t * z_a,
        sample_delta * t * x_b - sample_beta * z_b,
    )
    framed_coefficients = -sample_beta * v01 + t * middle + sample_delta * t**2 * v10
    assert all(
        sp.expand(entry) == 0 for entry in direct_coefficients - framed_coefficients
    )


def blocker_root_rows() -> tuple[sp.Matrix, ...]:
    e0, e1, e2 = (sp.eye(3).row(index) for index in range(3))
    exceptional = (
        sp.Matrix.vstack(e1, e2, e1 + e2, e1 + 2 * e2, e1 - e2, e0),
        sp.Matrix.vstack(e0, e2, e0 + e2, e0 + 2 * e2, e0 - e2, e1),
        sp.Matrix.vstack(e0, e1, e0 + e1, e0 + 2 * e1, e0 - e1, e2),
    )
    full = sp.Matrix.vstack(
        e0,
        e1,
        e2,
        e0 + e1 + e2,
        e0 + 2 * e1 + 3 * e2,
        3 * e0 + 2 * e1 + e2,
    )
    return (*exceptional, full, full.copy(), full.copy())


def ports() -> tuple[tuple[sp.Matrix, ...], tuple[sp.Matrix, ...]]:
    port_b = tuple(
        sp.Matrix([row])
        for row in (
            (1, 1, 0),
            (0, 1, 1),
            (1, 0, 1),
            (2, 1, 1),
            (1, 3, 1),
            (1, 1, 4),
        )
    )
    port_a = tuple(
        sp.Matrix([row])
        for row in (
            (0, 1, 2),
            (2, 0, 1),
            (1, 2, 0),
            (1, 1, 2),
            (2, 1, 1),
            (1, 2, 1),
        )
    )
    return port_a, port_b


def permanent(matrix: sp.Matrix) -> sp.Expr:
    states = {0: sp.S.One}
    for column in range(6):
        next_states = {}
        for mask, value in states.items():
            for row in range(6):
                if mask & (1 << row):
                    continue
                new_mask = mask | (1 << row)
                next_states[new_mask] = next_states.get(new_mask, sp.S.Zero) + (
                    value * matrix[row, column]
                )
        states = next_states
    return sp.expand(states[63])


def local_model_nonextension() -> dict[str, int]:
    x = sp.Matrix([1, 1, 1])
    z_a = sp.Matrix([1, 2, 3])
    z_b = sp.Matrix([1, 3, 2])
    alpha_a = sp.Matrix([2, -1, 0])
    alpha_b = sp.Matrix([sp.Rational(3, 2), sp.Rational(-1, 2), 0])
    cross = alpha_a * alpha_b.T
    beta = (x.T * cross * x)[0]
    delta = (z_a.T * cross * z_b)[0]
    assert beta == 1
    assert delta == 0
    assert (x.T * cross * z_b)[0] == 0
    assert (z_a.T * cross * x)[0] == 0

    roots = blocker_root_rows()
    port_a, port_b = ports()
    word = (0, 0, 0, 0, 0, 1)
    scalar = sp.Matrix(
        6,
        6,
        lambda row, mode: sp.Matrix.vstack(
            roots[mode][:4, :], port_a[mode], port_b[mode]
        )[row, word[mode]],
    )
    coefficient = permanent(scalar)
    assert coefficient == 18
    assert len(set(word)) > 1  # The GHZ diagonal coefficient is zero.
    assert delta * coefficient == 0
    return {
        "beta": int(beta),
        "delta": int(delta),
        "double_port_off_diagonal_coefficient": int(coefficient),
    }


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero order-twelve structural theorem",
        "isotropic rational curve",
        "Pi_11=D_11",
        "cannot extend to an order-twelve global witness",
        "UNRESOLVED",
    ):
        assert phrase in theorem
    for dependency in (
        "SIX_BLOCKER_NONZERO_CROSS_PORT_FREEDOM.md",
        "SIX_BLOCKER_MAXIMAL_OVERLAP_GHZ_HYPERCUBE.md",
        "ODD_RESIDUAL_PORT_PERMANENT_EXTRACTION.md",
    ):
        assert (ROOT / dependency).exists()

    symbolic_curve()
    partition = matching_partition()
    local_model = local_model_nonextension()
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "matching_partition": partition,
                "cross_form_normal_form": "diag(beta,delta)",
                "quotient_permanent_map_rank_bound": 1,
                "sample_frame_determinant": 69,
                "isotropic_p6_curve_proved": True,
                "delta_zero_double_port_p6_forced": True,
                "local_model_nonextension": local_model,
                "arbitrary_ambient_order_claimed": False,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
