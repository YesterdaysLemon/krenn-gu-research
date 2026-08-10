#!/usr/bin/env python3
"""Verify component 25's k=0 generic projective-D23 obstruction exactly."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
from verify_p5_h31_marked_basis_open_branch import one_marked_map, permanent



import itertools
import json
import time

import sympy as sp


WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]


def add(*rows):
    return tuple(sp.expand(sum(row[j] for row in rows)) for j in range(4))


def scale(c, row):
    return tuple(sp.expand(c * value) for value in row)


def boundary_basis(s, sign):
    """The a=1,g=0,k=0 basis on the es=sign sheet."""
    cap_a = (1, 1, 0, 0)
    cap_c = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    cap_d = (0, 0, 1, -1)
    e = sp.Rational(sign, 1) / s
    alpha = (
        add(cap_a, scale(-e, cap_b)),
        add(cap_a, scale(-e, cap_b), scale(-sign, cap_c)),
        cap_c,
        cap_d,
    )
    beta = (
        cap_a,
        cap_a,
        add(cap_a, scale(e, cap_b)),
        add(cap_b, scale(-s, cap_c)),
    )
    return alpha, beta


def marked(alpha, beta, shifts):
    return tuple(add(beta[i], scale(shifts[i], alpha[i])) for i in range(4))


def project(row, extension, direction, slope):
    if direction == "D23":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    raise ValueError(direction)


def tensor(alpha, beta, extensions, direction, slope):
    alpha_p = tuple(
        project(alpha[i], extensions[i], direction, slope) for i in range(4)
    )
    beta_p = tuple(
        project(beta[i], extensions[4 + i], direction, slope) for i in range(4)
    )
    values = {
        word: sp.factor(
            permanent(
                tuple(beta_p[i] if word[i] else alpha_p[i] for i in range(4))
            )
        )
        for word in WORDS
    }
    return alpha_p, beta_p, values


def fixed_vertex_equations(values):
    empty = values[WORDS[0]]
    singletons = tuple(
        values[tuple(int(i == mode) for i in range(4))] for mode in range(4)
    )
    equations = [empty - 1]
    for word in WORDS:
        weight = sum(word)
        if 2 <= weight <= 3:
            equations.append(
                values[word] * empty ** (weight - 1)
                - sp.prod(singletons[i] for i in range(4) if word[i])
            )
    return tuple(equations), singletons


def determinant(matrix, rows, columns=None):
    if columns is None:
        columns = range(matrix.cols)
    return sp.factor(matrix[list(rows), list(columns)].det(method="domain-ge"))


def main():
    started = time.perf_counter()
    s, slope, parameter = sp.symbols("s lambda t")
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("z0:8")
    alpha, beta = boundary_basis(s, 1)

    # The pure tensor and pair-rank profile locate this divisor.  Its multiset
    # differs from component 23's closed t=0 profile, so no mode permutation
    # can identify the two P4 configurations.
    pure = {
        word: sp.factor(
            permanent(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))
        )
        for word in WORDS
    }
    assert pure[WORDS[-1]] == 4 / s
    assert all(pure[word] == 0 for word in WORDS[:-1])
    pair_profile = tuple(
        sp.Matrix([alpha[i], beta[i], alpha[j], beta[j]]).rank()
        for i, j in itertools.combinations(range(4), 2)
    )
    assert pair_profile == (3, 3, 4, 3, 4, 4)
    assert sorted(pair_profile) != sorted((3, 3, 3, 3, 4, 4))

    # Recheck the exact sign-sheet covariance after specializing k=0.
    alpha_minus, beta_minus = boundary_basis(s, -1)
    alpha_plus_transfer, beta_plus_transfer = boundary_basis(-s, 1)
    row_signs = (1, 1, -1, -1)
    plus_shifts = tuple(row_signs[i] * shifts[i] for i in range(4))
    plus_extensions = tuple(
        row_signs[i] * extensions[i] for i in range(4)
    ) + extensions[4:]
    _, _, minus_values = tensor(
        alpha_minus,
        marked(alpha_minus, beta_minus, shifts),
        extensions,
        "D23",
        slope,
    )
    _, _, plus_values = tensor(
        alpha_plus_transfer,
        marked(alpha_plus_transfer, beta_plus_transfer, plus_shifts),
        plus_extensions,
        "D23",
        1 / slope,
    )
    for word in WORDS:
        source_scale = sp.prod(
            row_signs[i] for i in range(4) if word[i] == 0
        )
        assert sp.factor(
            sp.cancel(source_scale * minus_values[word] - slope * plus_values[word])
        ) == 0

    # Compute the complete normalized D23 fixed-vertex incidence from scratch.
    _, _, canonical = tensor(alpha, beta, extensions, "D23", slope)
    equations, singletons = fixed_vertex_equations(canonical)
    numerators = tuple(sp.together(value).as_numer_denom()[0] for value in equations)
    field = sp.QQ.frac_field(s, slope)
    actual = sp.groebner(numerators, *extensions, domain=field, order="grevlex")

    x = s + 2 * (1 - slope) * parameter
    q = extensions[4]
    expected_equations = (
        q * (2 * (slope - 1) * q - 1),
        2 * s * (slope - 1) * (extensions[0] + q)
        + 2 * (slope - 1) * extensions[7]
        - s,
        2 * s * (slope - 1) * (extensions[1] + q)
        + 2 * (slope - 1) * extensions[7]
        - s,
        2 * (slope - 1) * (extensions[2] + q) - 1,
        2 * (slope + 1) * extensions[3]
        + 4 * s * (slope - 1) * q
        + 2 * (slope - 1) * extensions[7]
        - s,
        extensions[5],
        s * extensions[6] - extensions[7],
    )
    expected = sp.groebner(
        expected_equations, *extensions, domain=field, order="grevlex"
    )
    assert all(actual.reduce(value)[1] == 0 for value in expected_equations)
    assert all(
        expected.reduce(polynomial.as_expr())[1] == 0 for polynomial in actual.polys
    )
    assert len(actual) == len(expected) == 7
    # The quadratic is square-free on the ordinary-weight chart, so this ideal
    # is the reduced disjoint union of the following two affine lines.
    branches = {}
    for name, q_value in (
        ("inherited", sp.Integer(0)),
        ("specialization", 1 / (2 * (slope - 1))),
    ):
        branches[name] = {
            extensions[0]: x / (2 * s * (slope - 1)) - q_value,
            extensions[1]: x / (2 * s * (slope - 1)) - q_value,
            extensions[2]: 1 / (2 * (slope - 1)) - q_value,
            extensions[3]: x / (2 * (slope + 1))
            - 2 * s * (slope - 1) * q_value / (slope + 1),
            extensions[4]: q_value,
            extensions[5]: 0,
            extensions[6]: parameter / s,
            extensions[7]: parameter,
        }
    assert all(
        sp.factor(sp.cancel(value.subs(line))) == 0
        for line in branches.values()
        for value in equations
    )

    branch_markings = {}
    branch_maps = {}
    expected_markings = {
        "inherited": (-1, -1, -1, -(slope + 1) / (slope - 1)),
        "specialization": (-1, 0, -1, 0),
    }
    expected_opposites = {
        "inherited": -(
            (slope + 1) * (s + 4 * (1 - slope) * parameter)
        )
        / (s * (slope - 1)),
        "specialization": (
            (slope + 1) * (s + 4 * (slope - 1) * parameter)
        )
        / (s * (slope - 1)),
    }
    for name, line in branches.items():
        marking = tuple(sp.factor(-value.subs(line)) for value in singletons)
        branch_markings[name] = marking
        assert all(
            sp.factor(sp.cancel(left - right)) == 0
            for left, right in zip(marking, expected_markings[name], strict=True)
        )

        alpha_23, beta_23, _ = tensor(
            alpha, beta, tuple(line[z] for z in extensions), "D23", slope
        )
        beta_23_marked = marked(alpha_23, beta_23, marking)
        marked_23 = {
            word: sp.factor(
                permanent(
                    tuple(
                        beta_23_marked[i] if word[i] else alpha_23[i]
                        for i in range(4)
                    )
                )
            )
            for word in WORDS
        }
        assert marked_23[WORDS[0]] == 1
        assert all(marked_23[word] == 0 for word in MIXED)
        assert sp.factor(
            sp.cancel(marked_23[WORDS[-1]] - expected_opposites[name])
        ) == 0

        alpha_01, beta_01, _ = tensor(
            alpha, beta, tuple(line[z] for z in extensions), "D01", slope
        )
        beta_01_marked = marked(alpha_01, beta_01, marking)
        branch_maps[name] = tuple(
            sp.Matrix(one_marked_map(i, alpha_01, beta_01_marked))
            for i in range(4)
        )

    # Classify every paired-D01 rank on the inherited line.
    maps = branch_maps["inherited"]
    y = s + 4 * (1 - slope) * parameter
    zeta = s + 8 * (1 - slope) * parameter
    p = s * (slope - 2) - 3 * (slope - 1) ** 2 * parameter

    # Mode zero: X and Y cannot vanish together because 2X-Y=s.
    mode0_x = determinant(maps[0], (1, 2, 4, 5))
    mode0_y = determinant(maps[0], (1, 3, 4, 5))
    assert sp.factor(sp.cancel(mode0_x - x / s**3)) == 0
    assert sp.factor(
        sp.cancel(mode0_y + 2 * (slope + 1) * y / (s**3 * (slope - 1)))
    ) == 0
    assert sp.expand(2 * x - y) == s

    # Mode one: X and Zeta cannot vanish together because 4X-Zeta=3s.
    mode1_x = determinant(maps[1], (0, 1, 2, 5))
    mode1_zeta = determinant(maps[1], (0, 1, 3, 5))
    assert sp.factor(
        sp.cancel(mode1_x - (slope + 1) * x / (s**3 * (slope - 1)))
    ) == 0
    assert sp.factor(
        sp.cancel(
            mode1_zeta
            + (slope + 1) ** 2 * zeta / (s**3 * (slope - 1) ** 2)
        )
    ) == 0
    assert sp.expand(4 * x - zeta) == 3 * s

    # Mode two has rank four exactly off X=0 and drops exactly to rank two there.
    mode2_x = determinant(maps[2], (2, 3, 6, 7))
    assert sp.factor(
        sp.cancel(mode2_x + (slope + 1) * x**2 / (s**4 * (slope - 1)))
    ) == 0
    x_zero = {parameter: s / (2 * (slope - 1))}
    mode2_zero = maps[2].subs(x_zero)
    mode2_kernel = (
        sp.Matrix((0, -1, 1, 0)),
        sp.Matrix((2 * (slope - 1) ** 2, -4 * (slope - 1) / s, 0, 1)),
    )
    assert all(
        all(sp.factor(sp.cancel(value)) == 0 for value in mode2_zero * vector)
        for vector in mode2_kernel
    )
    assert sp.Matrix.hstack(*mode2_kernel).rank() == 2
    mode2_two = determinant(mode2_zero, (1, 3), (1, 3))
    assert sp.factor(sp.cancel(mode2_two + (slope + 1) / s)) == 0

    # Mode three has no maximal minor.  Two 3-minors cover the parameter line:
    # 2P-3(lambda-1)X=-s(lambda+1), a unit on the ordinary-weight chart.
    assert all(
        sp.factor(sp.cancel(value)) == 0
        for value in maps[3] * sp.Matrix((0, -1, 1, 0))
    )
    mode3_p = determinant(maps[3], (0, 1, 2), (0, 1, 3))
    mode3_x = determinant(maps[3], (0, 2, 3), (0, 1, 3))
    assert sp.factor(
        sp.cancel(
            mode3_p
            - 2 * (slope + 1) * p / (s**6 * (slope - 1) ** 2)
        )
    ) == 0
    assert sp.factor(
        sp.cancel(
            mode3_x
            - 3 * (slope + 1) * x / (s**6 * (slope - 1))
        )
    ) == 0
    assert sp.expand(2 * p - 3 * (slope - 1) * x + s * (slope + 1)) == 0

    # On the new specialization line, modes zero and three have rank three
    # everywhere, while modes one and two have rank four everywhere.
    maps = branch_maps["specialization"]
    w = s + 2 * (slope - 1) * parameter

    new_mode0_kernel = sp.Matrix(
        (
            0,
            s - 4 * parameter,
            -(s + 4 * slope * parameter),
            4 * parameter**2 * (slope + 1),
        )
    )
    assert all(
        sp.factor(sp.cancel(value)) == 0 for value in maps[0] * new_mode0_kernel
    )
    new_mode0_t = determinant(maps[0], (0, 1, 3), (0, 1, 2))
    new_mode0_w = determinant(maps[0], (2, 6, 7), (0, 2, 3))
    assert sp.factor(
        sp.cancel(new_mode0_t - 24 * parameter**3 * (slope - 1) ** 2 / s**4)
    ) == 0
    assert sp.factor(
        sp.cancel(new_mode0_w + (s - 4 * parameter) * w / s**4)
    ) == 0

    new_mode1_t = determinant(maps[1], (0, 1, 3, 5))
    new_mode1_w = determinant(maps[1], (1, 4, 5, 6))
    assert sp.factor(
        sp.cancel(new_mode1_t + 12 * parameter**2 * (slope - 1) ** 2 / s**4)
    ) == 0
    assert sp.factor(
        sp.cancel(
            new_mode1_w - (slope - 1) * w**2 / (s**4 * (slope + 1))
        )
    ) == 0

    new_mode2_w = determinant(maps[2], (0, 1, 2, 4))
    new_mode2_t = determinant(maps[2], (1, 2, 3, 5))
    assert sp.factor(
        sp.cancel(new_mode2_w - 4 * w**2 / (s**4 * (slope - 1)))
    ) == 0
    assert sp.factor(
        sp.cancel(
            new_mode2_t
            - 12 * parameter**2 * (slope + 1) ** 3 / (s**4 * (slope - 1))
        )
    ) == 0

    assert all(
        sp.factor(sp.cancel(value)) == 0
        for value in maps[3] * sp.Matrix((0, -1, 1, 0))
    )
    new_mode3_t = determinant(maps[3], (0, 1, 7), (0, 1, 3))
    new_mode3_six = determinant(maps[3], (0, 4, 5), (0, 1, 3))
    six = s + 6 * (slope - 1) * parameter
    assert sp.factor(
        sp.cancel(new_mode3_t - 6 * parameter * (slope + 1) / s**6)
    ) == 0
    assert sp.factor(sp.cancel(new_mode3_six + six / s**6)) == 0

    print(
        json.dumps(
            {
                "status": "pass_with_k_zero_generic_projective_D23_closure",
                "component": 25,
                "projective_leaf_sheets": ["a=1,g=0,es=1", "a=1,g=0,es=-1"],
                "component_divisor": "k=0,s!=0",
                "field": "Q(s,lambda)",
                "p4_pair_profile": list(pair_profile),
                "component23_transport": "excluded by pair-profile multiset",
                "normalized_binary_incidence_ideal": "two reduced affine lines",
                "forced_markings": {
                    name: [str(value) for value in marking]
                    for name, marking in branch_markings.items()
                },
                "paired_D01_rank_profiles": {
                    "inherited_X_nonzero": [4, 4, 4, 3],
                    "inherited_X_zero": [4, 4, 2, 3],
                    "specialization_all_t": [3, 4, 4, 3],
                },
                "global_obstruction": (
                    "inherited line: mode 0 rank 4; "
                    "specialization line: modes 1 and 2 rank 4"
                ),
                "generic_finite_D23_closed": True,
                "special_finite_weights_closed": False,
                "D23_weight_infinity_closed": False,
                "other_projective_charts_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
