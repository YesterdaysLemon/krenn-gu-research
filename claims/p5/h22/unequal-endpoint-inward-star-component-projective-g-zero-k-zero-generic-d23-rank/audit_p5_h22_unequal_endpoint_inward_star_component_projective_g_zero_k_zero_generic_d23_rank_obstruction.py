#!/usr/bin/env python3
"""No-import audit of component 25's k=0 generic projective-D23 closure."""

from __future__ import annotations

import itertools
import json
import time

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))


def permanent_dp(rows):
    """Permanent by subset DP, independent of the repository implementation."""
    n = len(rows)
    state = {0: sp.Integer(1)}
    for row in rows:
        next_state = {}
        for mask, coefficient in state.items():
            for column in range(n):
                bit = 1 << column
                if mask & bit:
                    continue
                target = mask | bit
                next_state[target] = next_state.get(target, 0) + coefficient * row[column]
        state = next_state
    return sp.expand(state[(1 << n) - 1])


def plus(*rows):
    return tuple(sp.expand(sum(row[j] for row in rows)) for j in range(4))


def times(c, row):
    return tuple(sp.expand(c * value) for value in row)


def basis(s, sign):
    a = (1, 1, 0, 0)
    c = (1, -1, 0, 0)
    b = (0, 0, 1, 1)
    d = (0, 0, 1, -1)
    e = sp.Rational(sign, 1) / s
    alpha = (
        plus(a, times(-e, b)),
        plus(a, times(-e, b), times(-sign, c)),
        c,
        d,
    )
    beta = (a, a, plus(a, times(e, b)), plus(b, times(-s, c)))
    return alpha, beta


def shift_rows(alpha, beta, shifts):
    return tuple(plus(beta[i], times(shifts[i], alpha[i])) for i in range(4))


def projection(row, extension, direction, slope):
    if direction == "D23":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    raise AssertionError(direction)


def coefficients(alpha, beta, extensions, direction, slope):
    a = tuple(projection(alpha[i], extensions[i], direction, slope) for i in range(4))
    b = tuple(
        projection(beta[i], extensions[4 + i], direction, slope) for i in range(4)
    )
    values = {
        word: sp.factor(
            permanent_dp(tuple(b[i] if word[i] else a[i] for i in range(4)))
        )
        for word in WORDS
    }
    return a, b, values


def incidence(values):
    zero = values[(0, 0, 0, 0)]
    singles = tuple(
        values[tuple(int(i == mode) for i in range(4))] for mode in range(4)
    )
    equations = [zero - 1]
    for word in WORDS:
        degree = sum(word)
        if 2 <= degree <= 3:
            equations.append(
                values[word] * zero ** (degree - 1)
                - sp.prod(singles[i] for i in range(4) if word[i])
            )
    return tuple(equations), singles


def one_row_map(mode, alpha, beta):
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = []
        cursor = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if bits[cursor] else alpha[other])
                cursor += 1
        coefficient_row = []
        for coordinate in range(4):
            unit = tuple(int(j == coordinate) for j in range(4))
            coefficient_row.append(
                permanent_dp(
                    tuple(unit if other == mode else selected[other] for other in range(4))
                )
            )
        rows.append(coefficient_row)
    return sp.Matrix(rows)


def minor(matrix, rows, columns=None):
    if columns is None:
        columns = range(matrix.cols)
    return sp.factor(matrix[list(rows), list(columns)].det(method="domain-ge"))


def main():
    started = time.perf_counter()
    s, lam, u = sp.symbols("s lambda u")
    h = sp.symbols("h0:4")
    yvars = sp.symbols("y0:8")
    alpha, beta = basis(s, 1)

    # Independent P4-location check.
    pure = {
        word: sp.factor(
            permanent_dp(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))
        )
        for word in WORDS
    }
    assert pure[(1, 1, 1, 1)] == 4 / s
    assert all(value == 0 for word, value in pure.items() if word != (1, 1, 1, 1))
    profile = tuple(
        sp.Matrix([alpha[i], beta[i], alpha[j], beta[j]]).rank()
        for i, j in itertools.combinations(range(4), 2)
    )
    assert profile == (3, 3, 4, 3, 4, 4)

    # Independently audit all sixteen coefficients in the sign-sheet transfer.
    alpha_m, beta_m = basis(s, -1)
    alpha_t, beta_t = basis(-s, 1)
    signs = (1, 1, -1, -1)
    h_t = tuple(signs[i] * h[i] for i in range(4))
    y_t = tuple(signs[i] * yvars[i] for i in range(4)) + yvars[4:]
    _, _, minus = coefficients(
        alpha_m, shift_rows(alpha_m, beta_m, h), yvars, "D23", lam
    )
    _, _, transferred = coefficients(
        alpha_t, shift_rows(alpha_t, beta_t, h_t), y_t, "D23", 1 / lam
    )
    for word in WORDS:
        factor = sp.prod(signs[i] for i in range(4) if not word[i])
        assert sp.factor(sp.cancel(factor * minus[word] - lam * transferred[word])) == 0

    # Reverse-variable grevlex comparison of the full normalized incidence ideal.
    _, _, raw = coefficients(alpha, beta, yvars, "D23", lam)
    equations, singles = incidence(raw)
    field = sp.QQ.frac_field(s, lam)
    reverse = tuple(reversed(yvars))
    actual = sp.groebner(
        tuple(sp.together(value).as_numer_denom()[0] for value in equations),
        *reverse,
        domain=field,
        order="grevlex",
    )
    x = s + 2 * (1 - lam) * u
    q = yvars[4]
    union_equations = (
        q * (2 * (lam - 1) * q - 1),
        2 * s * (lam - 1) * (yvars[0] + q)
        + 2 * (lam - 1) * yvars[7]
        - s,
        2 * s * (lam - 1) * (yvars[1] + q)
        + 2 * (lam - 1) * yvars[7]
        - s,
        2 * (lam - 1) * (yvars[2] + q) - 1,
        2 * (lam + 1) * yvars[3]
        + 4 * s * (lam - 1) * q
        + 2 * (lam - 1) * yvars[7]
        - s,
        yvars[5],
        s * yvars[6] - yvars[7],
    )
    expected = sp.groebner(
        union_equations, *reverse, domain=field, order="grevlex"
    )
    assert len(actual) == len(expected) == 7
    assert all(actual.reduce(value)[1] == 0 for value in union_equations)
    assert all(
        expected.reduce(polynomial.as_expr())[1] == 0 for polynomial in actual.polys
    )

    branches = {}
    for name, q_value in (
        ("inherited", sp.Integer(0)),
        ("specialization", 1 / (2 * (lam - 1))),
    ):
        branches[name] = {
            yvars[0]: x / (2 * s * (lam - 1)) - q_value,
            yvars[1]: x / (2 * s * (lam - 1)) - q_value,
            yvars[2]: 1 / (2 * (lam - 1)) - q_value,
            yvars[3]: x / (2 * (lam + 1))
            - 2 * s * (lam - 1) * q_value / (lam + 1),
            yvars[4]: q_value,
            yvars[5]: 0,
            yvars[6]: u / s,
            yvars[7]: u,
        }
    assert all(
        sp.factor(sp.cancel(value.subs(line))) == 0
        for line in branches.values()
        for value in equations
    )

    target_markings = {
        "inherited": (-1, -1, -1, -(lam + 1) / (lam - 1)),
        "specialization": (-1, 0, -1, 0),
    }
    opposites = {
        "inherited": -((lam + 1) * (s + 4 * (1 - lam) * u))
        / (s * (lam - 1)),
        "specialization": ((lam + 1) * (s + 4 * (lam - 1) * u))
        / (s * (lam - 1)),
    }
    markings = {}
    branch_maps = {}
    for name, line in branches.items():
        marking = tuple(sp.factor(-value.subs(line)) for value in singles)
        markings[name] = marking
        assert all(
            sp.factor(sp.cancel(left - right)) == 0
            for left, right in zip(marking, target_markings[name], strict=True)
        )
        a23, b23, _ = coefficients(
            alpha, beta, tuple(line[y] for y in yvars), "D23", lam
        )
        bm23 = shift_rows(a23, b23, marking)
        marked23 = {
            word: sp.factor(
                permanent_dp(
                    tuple(bm23[i] if word[i] else a23[i] for i in range(4))
                )
            )
            for word in WORDS
        }
        assert marked23[(0, 0, 0, 0)] == 1
        assert all(marked23[word] == 0 for word in WORDS[1:-1])
        assert sp.factor(
            sp.cancel(marked23[(1, 1, 1, 1)] - opposites[name])
        ) == 0

        a01, b01, _ = coefficients(
            alpha, beta, tuple(line[y] for y in yvars), "D01", lam
        )
        bm01 = shift_rows(a01, b01, marking)
        branch_maps[name] = tuple(one_row_map(i, a01, bm01) for i in range(4))

    # Alternate minors audit the inherited line's complete paired-D01 ranks.
    maps = branch_maps["inherited"]
    y = s + 4 * (1 - lam) * u
    p = s * (lam - 2) - 3 * (lam - 1) ** 2 * u

    m0x = minor(maps[0], (0, 1, 2, 5))
    m0y = minor(maps[0], (0, 1, 3, 5))
    assert sp.factor(sp.cancel(m0x - 2 * x / (s**3 * (lam - 1)))) == 0
    assert sp.factor(
        sp.cancel(m0y + 4 * (lam + 1) * y / (s**3 * (lam - 1) ** 2))
    ) == 0
    assert sp.expand(2 * x - y) == s

    m1x = minor(maps[1], (0, 1, 2, 6))
    m1y = minor(maps[1], (1, 3, 5, 7))
    assert sp.factor(sp.cancel(m1x - x**2 / s**4)) == 0
    assert sp.factor(
        sp.cancel(m1y - 2 * (lam + 1) ** 3 * y / (s**3 * (lam - 1) ** 3))
    ) == 0
    assert sp.expand(2 * x - y) == s

    m2x = minor(maps[2], (0, 1, 2, 3))
    assert sp.factor(
        sp.cancel(m2x + (lam + 1) * x**2 / (s**4 * (lam - 1)))
    ) == 0
    at_x_zero = {u: s / (2 * (lam - 1))}
    m2zero = maps[2].subs(at_x_zero)
    m2kernel = (
        sp.Matrix((0, -1, 1, 0)),
        sp.Matrix((2 * (lam - 1) ** 2, -4 * (lam - 1) / s, 0, 1)),
    )
    assert all(
        all(sp.factor(sp.cancel(value)) == 0 for value in m2zero * vector)
        for vector in m2kernel
    )
    assert sp.Matrix.hstack(*m2kernel).rank() == 2
    m2two = minor(m2zero, (1, 7), (2, 3))
    assert sp.factor(sp.cancel(m2two - 2 * (lam + 1) / s)) == 0

    assert all(
        sp.factor(sp.cancel(value)) == 0
        for value in maps[3] * sp.Matrix((0, -1, 1, 0))
    )
    m3p = minor(maps[3], (0, 1, 2), (0, 2, 3))
    m3x = minor(maps[3], (0, 2, 5), (0, 1, 3))
    assert sp.factor(
        sp.cancel(m3p - 2 * (lam + 1) * p / (s**6 * (lam - 1) ** 2))
    ) == 0
    assert sp.factor(
        sp.cancel(m3x - 3 * (lam + 1) * x / (s**6 * (lam - 1)))
    ) == 0
    assert sp.expand(2 * p - 3 * (lam - 1) * x + s * (lam + 1)) == 0

    # Independent alternate minors on the specialization-only line.
    maps = branch_maps["specialization"]
    w = s + 2 * (lam - 1) * u

    mode0kernel = sp.Matrix(
        (0, s - 4 * u, -(s + 4 * lam * u), 4 * u**2 * (lam + 1))
    )
    assert all(
        sp.factor(sp.cancel(value)) == 0 for value in maps[0] * mode0kernel
    )
    m0t = minor(maps[0], (3, 6, 7), (0, 1, 2))
    m0w = minor(maps[0], (2, 6, 7), (0, 1, 3))
    assert sp.factor(sp.cancel(m0t - 24 * u**3 * (lam + 1) ** 2 / s**4)) == 0
    assert sp.factor(sp.cancel(m0w + (s + 4 * lam * u) * w / s**4)) == 0

    m1w = minor(maps[1], (0, 1, 2, 4))
    m1t = minor(maps[1], (1, 2, 3, 5))
    assert sp.factor(
        sp.cancel(m1w - (lam - 1) ** 2 * w**2 / (s**4 * (lam + 1) ** 2))
    ) == 0
    assert sp.factor(sp.cancel(m1t + 12 * u**2 * (lam - 1) ** 2 / s**4)) == 0

    m2w = minor(maps[2], (0, 2, 3, 4))
    m2t = minor(maps[2], (1, 2, 3, 7))
    assert sp.factor(sp.cancel(m2w + 2 * w**2 / (s**4 * (lam - 1)))) == 0
    assert sp.factor(
        sp.cancel(m2t - 12 * u**2 * (lam + 1) ** 3 / (s**4 * (lam - 1)))
    ) == 0

    assert all(
        sp.factor(sp.cancel(value)) == 0
        for value in maps[3] * sp.Matrix((0, -1, 1, 0))
    )
    m3t = minor(maps[3], (0, 1, 4), (0, 1, 3))
    m3six = minor(maps[3], (1, 4, 5), (0, 1, 3))
    six = s + 6 * (lam - 1) * u
    assert sp.factor(sp.cancel(m3t + 6 * u * (lam - 1) / s**6)) == 0
    assert sp.factor(
        sp.cancel(m3six - (lam + 1) * six / (s**6 * (lam - 1)))
    ) == 0

    print(
        json.dumps(
            {
                "status": "pass",
                "role": "no-import subset-DP, reverse-grevlex, alternate-minor audit",
                "component": 25,
                "divisor": "a=1,g=0,k=0,s!=0; both es sign sheets",
                "field": "Q(s,lambda)",
                "p4_pair_profile": list(profile),
                "normalized_incidence_ideal": "two reduced affine lines",
                "forced_markings": {
                    name: [str(value) for value in marking]
                    for name, marking in markings.items()
                },
                "paired_D01_rank_profiles": {
                    "inherited_X_nonzero": [4, 4, 4, 3],
                    "inherited_X_zero": [4, 4, 2, 3],
                    "specialization_all_u": [3, 4, 4, 3],
                },
                "both_lines_empty": True,
                "special_finite_weights_closed": False,
                "weight_infinity_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
