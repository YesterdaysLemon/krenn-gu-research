#!/usr/bin/env python3
"""Verify the one-double-endpoint star-(1,1,1) classification."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess

import sympy as sp

BITS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def coefficients(planes):
    return {
        bits: sp.factor(permanent([planes[index][bits[index]] for index in range(4)]))
        for bits in BITS
    }


def product(left, right):
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def pair_matrix(left, right):
    return sp.Matrix.hstack(*(product(u, v) for u in left for v in right))


def maximal_minors(matrix, size=4):
    return [
        sp.factor(matrix.extract(rows, columns).det())
        for rows in itertools.combinations(range(matrix.rows), size)
        for columns in itertools.combinations(range(matrix.cols), size)
    ]


def common_center(A, C, B, D):
    a0, b0, d0, a1, b1, d1, a2, b2, d2, a3, b3, d3 = sp.symbols(
        "a0 b0 d0 a1 b1 d1 a2 b2 d2 a3 b3 d3"
    )
    x0 = a0 * C + b0 * B + d0 * D
    x1 = a1 * A + b1 * B + d1 * D
    y2 = a2 * A + b2 * B + d2 * D
    y3 = a3 * A + b3 * B + d3 * D
    planes = ((A, x0), (C, x1), (y2, C), (y3, C))
    values = coefficients(planes)
    e02 = b0 * b2 - d0 * d2
    e03 = b0 * b3 - d0 * d3
    assert sp.factor(values[(1, 0, 0, 1)] + 4 * e02) == 0
    assert sp.factor(values[(1, 0, 1, 0)] + 4 * e03) == 0
    wedge = b2 * d3 - d2 * b3
    assert sp.factor(e02 * d3 - e03 * d2 - b0 * wedge) == 0
    assert sp.factor(e02 * b3 - e03 * b2 - d0 * wedge) == 0
    minors = maximal_minors(pair_matrix(planes[2], planes[3]))
    assert all(sp.rem(minor, wedge) == 0 for minor in minors)
    return "singleton zero; binary forces r23<=3"


def mixed_cases(X, A, C, B, D):
    # Singleton double support: both leaf planes contain e and e^2=0.
    e = X[0]
    u = sp.Matrix(sp.symbols("u0:4"))
    v = sp.Matrix(sp.symbols("v0:4"))
    singleton_pair = pair_matrix((e, u), (v, e))
    assert all(minor == 0 for minor in maximal_minors(singleton_pair))

    # Binary, disjoint second support.
    a1, b1, d1, a2, b2, d2, a3, c3, b3 = sp.symbols(
        "ma1 mb1 md1 ma2 mb2 md2 ma3 mc3 mb3"
    )
    planes = (
        (A, B),
        (C, a1 * A + b1 * B + d1 * D),
        (a2 * A + b2 * B + d2 * D, C),
        (D, a3 * A + c3 * C + b3 * B),
    )
    values = coefficients(planes)
    assert values[(1, 1, 1, 1)] == -4 * b1 * c3
    assert values[(1, 0, 1, 1)] == -4 * b3
    assert values[(1, 0, 0, 1)] == -4 * b2 * c3

    # Binary, overlapping second support.
    y0 = X[0] + X[1]
    polar = X[0] - X[1]
    w = X[0] + X[2]
    y3 = X[0] - X[2]
    oa1, ob1, od1, oa2, ob2, od2, oa3, oc3, od3 = sp.symbols(
        "oa1 ob1 od1 oa2 ob2 od2 oa3 oc3 od3"
    )
    overlap = (
        (y0, w),
        (polar, oa1 * y0 + ob1 * X[2] + od1 * X[3]),
        (oa2 * y0 + ob2 * X[2] + od2 * X[3], polar),
        (y3, oa3 * w + oc3 * X[1] + od3 * X[3]),
    )
    values = coefficients(overlap)
    assert values[(1, 0, 1, 1)] == -2 * od3
    assert sp.factor(values[(1, 1, 1, 1)] - od1 * (oc3 - 2 * oa3) + ob1 * od3) == 0
    assert sp.factor(values[(1, 0, 0, 1)] - od2 * (oc3 - 2 * oa3) + ob2 * od3) == 0
    overlap_transverse = str(values[(1, 0, 1, 1)])

    # Binary, same second support.  The two polar equations either make the
    # middle plane equal to U0 or make the exterior 13 projections dependent.
    ca1, cb1, cd1, ca2, cb2, cd2, ca3, cb3, cd3 = sp.symbols(
        "ca1 cb1 cd1 ca2 cb2 cd2 ca3 cb3 cd3"
    )
    same_support = (
        (A, C),
        (C, ca1 * A + cb1 * B + cd1 * D),
        (ca2 * A + cb2 * B + cd2 * D, C),
        (A, ca3 * C + cb3 * B + cd3 * D),
    )
    values = coefficients(same_support)
    assert sp.factor(values[(1, 1, 1, 1)] + 4 * (cb1 * cb3 - cd1 * cd3)) == 0
    assert sp.factor(values[(0, 1, 0, 0)] - 4 * (cb1 * cb2 - cd1 * cd2)) == 0
    assert sp.factor(values[(1, 0, 0, 1)] + 4 * (cb2 * cb3 - cd2 * cd3)) == 0

    # Singleton inside the binary double support has the analogous ternary
    # polar system.
    ia1, ib1, id1, ia2, ib2, id2, ia3, ib3, id3 = sp.symbols(
        "ia1 ib1 id1 ia2 ib2 id2 ia3 ib3 id3"
    )
    singleton_inside = (
        (A, X[0]),
        (C, ia1 * A + ib1 * X[2] + id1 * X[3]),
        (ia2 * A + ib2 * X[2] + id2 * X[3], C),
        (X[0], ia3 * X[1] + ib3 * X[2] + id3 * X[3]),
    )
    values = coefficients(singleton_inside)
    assert sp.factor(values[(1, 1, 1, 1)] + ib1 * id3 + ib3 * id1) == 0
    assert sp.factor(values[(0, 1, 0, 0)] - ib1 * id2 - ib2 * id1) == 0
    assert sp.factor(values[(1, 0, 0, 1)] + ib2 * id3 + ib3 * id2) == 0

    # Binary, singleton outside the double support.
    sa1, sb1, sd1, sa2, sb2, sd2, sa3, sc3, sd3 = sp.symbols(
        "sa1 sb1 sd1 sa2 sb2 sd2 sa3 sc3 sd3"
    )
    singleton_outside = (
        (A, X[2]),
        (C, sa1 * A + sb1 * X[2] + sd1 * X[3]),
        (sa2 * A + sb2 * X[2] + sd2 * X[3], C),
        (X[2], sa3 * A + sc3 * C + sd3 * X[3]),
    )
    values = coefficients(singleton_outside)
    assert values[(1, 0, 1, 1)] == -2 * sd3
    assert values[(1, 1, 1, 1)] == -2 * sc3 * sd1
    assert values[(1, 0, 0, 1)] == -2 * sc3 * sd2

    return {
        "singleton_double": "r12<=3",
        "binary_second_supports": ["singleton", "same", "overlap", "disjoint"],
        "overlap_transverse_forcing": [overlap_transverse],
    }


def common_leaf_easy_cases(X, A, C, B, D):
    # Singleton double support, complete coordinate-pencil chart.
    c2, c3 = sp.symbols("lc2 lc3")
    a1, b1, d1, a2, b2, d2, a3, b3, d3 = sp.symbols(
        "la1 lb1 ld1 la2 lb2 ld2 la3 lb3 ld3"
    )
    w2 = X[1] + c2 * X[0]
    y2 = c2 * X[0] - X[1]
    w3 = X[1] + c3 * X[0]
    y3 = c3 * X[0] - X[1]
    pencil = (
        (X[0], X[1]),
        (X[0], a1 * X[1] + b1 * X[2] + d1 * X[3]),
        (y2, a2 * w2 + b2 * X[2] + d2 * X[3]),
        (y3, a3 * w3 + b3 * X[2] + d3 * X[3]),
    )
    values = coefficients(pencil)
    q13 = b1 * d3 + b3 * d1
    q12 = b1 * d2 + b2 * d1
    assert values[(0, 1, 0, 1)] == -q13
    assert values[(0, 1, 1, 0)] == -q12
    assert sp.factor(values[(1, 1, 1, 1)] - a2 * c2 * q13 - a3 * c3 * q12) == 0

    # Singleton double support with an equal disjoint-binary center factor.
    da1, db1, dd1, da2, dc2, dd2, da3, dc3, dd3 = sp.symbols(
        "da1 db1 dd1 da2 dc2 dd2 da3 dc3 dd3"
    )
    dw = X[1] + X[2]
    dz = X[1] - X[2]
    disjoint_from_singleton = (
        (X[0], dw),
        (X[0], da1 * dw + db1 * dz + dd1 * X[3]),
        (dz, da2 * dw + dc2 * X[0] + dd2 * X[3]),
        (dz, da3 * dw + dc3 * X[0] + dd3 * X[3]),
    )
    values = coefficients(disjoint_from_singleton)
    assert values[(0, 1, 0, 0)] == -2 * dd1
    assert (
        sp.factor(
            values[(1, 1, 1, 1)]
            - 2
            * (da1 * dc2 * dd3 + da1 * dc3 * dd2 + da2 * dc3 * dd1 + da3 * dc2 * dd1)
        )
        == 0
    )

    # Binary double support, all center factors in the same binary plane.
    ell, mu = sp.symbols("ell mu")
    sa1, sb1, sd1, sa2, sb2, sd2, sa3, sb3, sd3 = sp.symbols(
        "qa1 qb1 qd1 qa2 qb2 qd2 qa3 qb3 qd3"
    )
    same = (
        (A, C),
        (C, sa1 * A + sb1 * B + sd1 * D),
        (A + ell * C, sa2 * (C + ell * A) + sb2 * B + sd2 * D),
        (A + mu * C, sa3 * (C + mu * A) + sb3 * B + sd3 * D),
    )
    values = coefficients(same)
    q13 = sb1 * sb3 - sd1 * sd3
    q12 = sb1 * sb2 - sd1 * sd2
    assert sp.factor(values[(0, 1, 0, 1)] - 4 * q13) == 0
    assert sp.factor(values[(0, 1, 1, 0)] - 4 * q12) == 0
    assert sp.factor(values[(1, 1, 1, 1)] + 4 * (sa2 * q13 + sa3 * q12)) == 0

    # Equal overlapping binary factor: the full purity ideal contains active.
    u = X[0] + X[1]
    v = X[0] - X[1]
    w = X[0] + X[2]
    z = X[0] - X[2]
    ea1, eb1, ed1, ea2, ec2, ed2, ea3, ec3, ed3 = sp.symbols(
        "ea1 eb1 ed1 ea2 ec2 ed2 ea3 ec3 ed3"
    )
    equal_overlap = (
        (u, w),
        (v, ea1 * u + eb1 * X[2] + ed1 * X[3]),
        (z, ea2 * w + ec2 * X[1] + ed2 * X[3]),
        (z, ea3 * w + ec3 * X[1] + ed3 * X[3]),
    )
    values = coefficients(equal_overlap)
    forbidden = [
        value for bits, value in values.items() if bits != (1, 1, 1, 1) and value != 0
    ]
    variables = (ea1, eb1, ed1, ea2, ec2, ed2, ea3, ec3, ed3)
    basis = sp.groebner(forbidden, *variables, order="grevlex")
    assert basis.reduce(values[(1, 1, 1, 1)])[1] == 0

    # Equal disjoint binary factor.  These five equations are the complete
    # nonzero list after a1=0; their two-dimensional polar split forces an
    # exterior rank-three edge.
    ra1, rb1, rd1, ra2, rc2, rb2, ra3, rc3, rb3 = sp.symbols(
        "ra1 rb1 rd1 ra2 rc2 rb2 ra3 rc3 rb3"
    )
    equal_disjoint = (
        (A, B),
        (C, ra1 * A + rb1 * B + rd1 * D),
        (D, ra2 * A + rc2 * C + rb2 * B),
        (D, ra3 * A + rc3 * C + rb3 * B),
    )
    values = coefficients(equal_disjoint)
    assert values[(0, 1, 0, 0)] == -4 * ra1
    assert values[(0, 1, 0, 1)] == -4 * ra3 * rd1
    assert values[(0, 1, 1, 0)] == -4 * ra2 * rd1
    assert sp.factor(values[(1, 0, 1, 1)] + 4 * (rb2 * rc3 + rb3 * rc2)) == 0
    assert (
        sp.factor(
            values[(1, 1, 1, 1)]
            - 4
            * (ra1 * ra2 * rb3 + ra1 * ra3 * rb2 + ra2 * ra3 * rb1 - rb1 * rc2 * rc3)
        )
        == 0
    )

    # Equal singleton factor is an exterior rank-three boundary because the
    # shared kernel square is the zero column.
    su = sp.Matrix(sp.symbols("su0:4"))
    sv = sp.Matrix(sp.symbols("sv0:4"))
    singleton_leaf_pair = pair_matrix((X[2], su), (X[2], sv))
    assert all(minor == 0 for minor in maximal_minors(singleton_leaf_pair))
    return "singleton and same/overlap binary projective sheets closed"


def unequal_overlap_data(X):
    u = X[0] + X[1]
    v = X[0] - X[1]
    w = X[0] + X[2]
    z = X[0] - X[2]
    h = X[2] - X[1]
    k = X[2] + X[1]
    variables = sp.symbols("a1 b1 d1 a2 c2 d2 a3 c3 d3")
    a1, b1, d1, a2, c2, d2, a3, c3, d3 = variables
    planes = (
        (u, w),
        (v, a1 * u + b1 * X[2] + d1 * X[3]),
        (z, a2 * w + c2 * X[1] + d2 * X[3]),
        (k, a3 * h + c3 * X[0] + d3 * X[3]),
    )
    values = coefficients(planes)
    generators = [
        values[(0, 1, 0, 1)],
        values[(0, 1, 1, 0)],
        values[(0, 1, 1, 1)],
        values[(1, 0, 1, 1)],
    ]
    active = values[(1, 1, 1, 1)]
    primes = [
        [2 * d1 * a2 + d1 * c2 + 2 * a1 * d2 + b1 * d2, d3, c3, a3],
        [d3, 2 * a3 - c3, d2, 2 * a2 + c2],
        [d3, d2, d1],
        [-2 * d1 * a3 + d1 * c3 + 2 * a1 * d3 - b1 * d3, d2, c2, a2],
        [
            -2 * d2 * a3 + c2 * d3,
            d2 * c3 + 2 * a2 * d3,
            4 * a2 * a3 + c2 * c3,
            2 * d1 * a3 - d1 * c3 + b1 * d3,
            2 * d1 * a2 + d1 * c2 + b1 * d2,
            a1,
        ],
        [
            -d2 * c3 + c2 * d3,
            d2 * a3 + a2 * d3,
            c2 * a3 + a2 * c3,
            -2 * d1 * a3 + d1 * c3 + 2 * a1 * d3,
            2 * d1 * a2 + d1 * c2 + 2 * a1 * d2,
            b1,
        ],
        [2 * d2 * a3 + d2 * c3 + 2 * a2 * d3 - c2 * d3, d1, b1, a1],
    ]
    return variables, planes, generators, active, primes


def singular_command():
    native = shutil.which("Singular")
    if native:
        return [native, "-q"]
    wsl = shutil.which("wsl.exe")
    if wsl:
        return [wsl, "--exec", "/usr/bin/Singular", "-q"]
    raise RuntimeError("Singular is required for the exact radical replay")


def singular_expression(expression):
    return str(sp.expand(expression)).replace("**", "^")


def verify_radical_decomposition(variables, generators, primes):
    names = ",".join(str(variable) for variable in variables)
    source = [f'LIB "primdec.lib"; ring r=0,({names}),dp;']
    source.append("ideal I=" + ",".join(map(singular_expression, generators)) + ";")
    for index, prime in enumerate(primes, 1):
        source.append(
            f"ideal P{index}=" + ",".join(map(singular_expression, prime)) + ";"
        )
    source.append("ideal J=P1;")
    for index in range(2, len(primes) + 1):
        source.append(f"J=intersect(J,P{index});")
    source.append("ideal R=radical(I);")
    source.append("list L=minAssGTZ(I);")
    source.append('if(size(L)==7){"MINASS_SEVEN";}else{"MINASS_COUNT_FAIL";}')
    source.append(
        'if(size(simplify(reduce(R,std(J)),2))==0 && size(simplify(reduce(J,std(R)),2))==0){"RADICAL_EQUAL";}else{"RADICAL_FAIL";}'
    )
    completed = subprocess.run(
        singular_command(),
        input="\n".join(source),
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "RADICAL_EQUAL" in completed.stdout, completed.stdout
    assert "MINASS_SEVEN" in completed.stdout, completed.stdout


def unequal_overlap_classification(X):
    variables, planes, generators, active, primes = unequal_overlap_data(X)
    verify_radical_decomposition(variables, generators, primes)
    zero_primes = {1, 3, 4, 7}
    statuses = []
    for index, prime in enumerate(primes, 1):
        basis = sp.groebner(prime, *variables, order="grevlex")
        active_remainder = sp.factor(basis.reduce(active)[1])
        if index in zero_primes:
            assert active_remainder == 0
            statuses.append("zero")
            continue
        if index == 2:
            minors = maximal_minors(pair_matrix(planes[0], planes[2]), size=3)
            assert all(basis.reduce(minor)[1] == 0 for minor in minors)
            statuses.append("lower-pair")
            continue
        boundary_basis = sp.groebner(
            [*prime, variables[5], variables[8]], *variables, order="grevlex"
        )
        minors = maximal_minors(pair_matrix(planes[2], planes[3]))
        assert all(boundary_basis.reduce(minor)[1] == 0 for minor in minors)
        inverse = sp.Symbol(f"inverse_{index}")
        d2_zero_open = sp.groebner(
            [*prime, variables[5], inverse * active - 1],
            inverse,
            *variables,
            order="grevlex",
        )
        d3_zero_open = sp.groebner(
            [*prime, variables[8], inverse * active - 1],
            inverse,
            *variables,
            order="grevlex",
        )
        assert d2_zero_open.reduce(variables[8])[1] == 0
        assert d3_zero_open.reduce(variables[5])[1] == 0
        assert active_remainder != 0
        statuses.append("radical-star interior; r23 boundary")
    return statuses


def main():
    X = tuple(sp.eye(4).col(index) for index in range(4))
    A = X[0] + X[1]
    C = X[0] - X[1]
    B = X[2] + X[3]
    D = X[2] - X[3]
    common_center_result = common_center(A, C, B, D)
    mixed_result = mixed_cases(X, A, C, B, D)
    common_leaf_result = common_leaf_easy_cases(X, A, C, B, D)
    unequal_statuses = unequal_overlap_classification(X)
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "orientation_count": 3,
                "common_center": common_center_result,
                "mixed_support_ledger": mixed_result,
                "common_leaf_easy_cases": common_leaf_result,
                "unequal_overlap_minimal_primes": unequal_statuses,
                "surviving_dense_primes": [5, 6],
                "surviving_dense_placement": "overlapping radical star -> L1/L2/L3",
                "new_component_orbit": False,
                "two_double_stratum_classified_by_this_verifier": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
