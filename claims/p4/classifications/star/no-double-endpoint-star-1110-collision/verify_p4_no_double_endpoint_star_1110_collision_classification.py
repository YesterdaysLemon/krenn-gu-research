#!/usr/bin/env python3
"""Exact verification of the no-double star-(1,1,1) collision ledger."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess
from pathlib import Path

import sys

import sympy as sp

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
THEOREM = HERE / "P4_NO_DOUBLE_ENDPOINT_STAR_1110_COLLISION_CLASSIFICATION.md"
BITS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))


def permanent(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def coefficients(planes: tuple[tuple[sp.Matrix, sp.Matrix], ...]):
    return {
        bits: sp.factor(permanent(tuple(planes[i][bits[i]] for i in range(4))))
        for bits in BITS
    }


def product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def pair_matrix(left, right) -> sp.Matrix:
    return sp.Matrix.hstack(*(product(u, v) for u in left for v in right))


def four_minors(matrix: sp.Matrix) -> list[sp.Expr]:
    return [
        sp.factor(matrix.extract(rows, range(4)).det())
        for rows in itertools.combinations(range(6), 4)
    ]


def pair_profile(planes) -> tuple[int, ...]:
    return tuple(pair_matrix(planes[i], planes[j]).rank() for i, j in PAIRS)


def forbidden_and_active(planes, substitutions=None):
    values = coefficients(planes)
    if substitutions:
        values = {
            bits: sp.factor(value.subs(substitutions)) for bits, value in values.items()
        }
    forbidden = [
        value for bits, value in values.items() if bits != (1, 1, 1, 1) and value != 0
    ]
    return forbidden, values[(1, 1, 1, 1)], values


def singular_command() -> list[str]:
    native = shutil.which("Singular")
    if native:
        return [native, "-q"]
    if shutil.which("wsl.exe"):
        return ["wsl.exe", "--exec", "/usr/bin/Singular", "-q"]
    raise RuntimeError("Singular is required for exact radical replay")


def singular_expr(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def radical_check(
    label: str,
    variables: tuple[sp.Symbol, ...],
    ideal: list[sp.Expr],
    open_factor: sp.Expr,
    primes: list[list[sp.Expr]],
) -> None:
    names = ",".join(map(str, variables))
    source = [f'LIB "primdec.lib"; ring r=0,({names}),dp;']
    source.append("ideal I=" + ",".join(map(singular_expr, ideal)) + ";")
    source.append(f"ideal J=sat(I,ideal({singular_expr(open_factor)}));")
    source.append("ideal R=radical(J); list L=minAssGTZ(J);")
    if not primes:
        source.append('if(reduce(1,std(J))==0){"UNIT_OK";}else{"UNIT_FAIL";}')
    else:
        for index, prime in enumerate(primes, 1):
            source.append(
                f"ideal P{index}=" + ",".join(map(singular_expr, prime)) + ";"
            )
        source.append("ideal K=P1;")
        for index in range(2, len(primes) + 1):
            source.append(f"K=intersect(K,P{index});")
        source.append(
            "if(size(simplify(reduce(R,std(K)),2))==0 "
            '&& size(simplify(reduce(K,std(R)),2))==0){"RADICAL_OK";}else{"RADICAL_FAIL";}'
        )
        source.append(f'if(size(L)=={len(primes)}){{"COUNT_OK";}}else{{"COUNT_FAIL";}}')
    completed = subprocess.run(
        singular_command(),
        input="\n".join(source),
        text=True,
        capture_output=True,
        timeout=300,
        check=False,
    )
    assert completed.returncode == 0, (label, completed.stderr)
    if primes:
        assert "RADICAL_OK" in completed.stdout, (label, completed.stdout)
        assert "COUNT_OK" in completed.stdout, (label, completed.stdout)
    else:
        assert "UNIT_OK" in completed.stdout, (label, completed.stdout)


def prime_kills_pair(planes, substitutions, prime, variables, pair) -> None:
    basis = sp.groebner(prime, *variables, order="grevlex")
    matrix = pair_matrix(planes[pair[0]], planes[pair[1]]).subs(substitutions)
    assert all(basis.reduce(sp.expand(minor))[1] == 0 for minor in four_minors(matrix))


def flattening_ranks(values) -> tuple[int, ...]:
    ranks = []
    for mode in range(4):
        other = tuple(index for index in range(4) if index != mode)
        matrix = sp.zeros(2, 8)
        for bits, value in values.items():
            column = sum(bits[index] << place for place, index in enumerate(other))
            matrix[bits[mode], column] = value
        ranks.append(matrix.rank())
    return tuple(ranks)


def source_triangle(X):
    a1, b1, d1, a2, c2, d2, a3, c3, d3, t = sp.symbols("a1 b1 d1 a2 c2 d2 a3 c3 d3 t")
    f1, g1 = X[0] + X[1], X[0] - X[1]
    f2, g2 = X[0] + X[2], X[0] - X[2]
    f3, g3 = X[2] - X[1], X[2] + X[1]
    planes = (
        (f2 + t * f1, f1),
        (g1, a1 * f1 + b1 * X[2] + d1 * X[3]),
        (g2, a2 * f2 + c2 * X[1] + d2 * X[3]),
        (g3, a3 * f3 + c3 * X[0] + d3 * X[3]),
    )
    forbidden, active, values = forbidden_and_active(planes)
    variables = (a1, b1, d1, a2, c2, d2, a3, c3, d3, t)

    # The full complementary-row projective sheet has one saturated prime,
    # and its d1*d2*d3 chart is dense.
    names = ",".join(map(str, variables))
    source = [f'LIB "primdec.lib"; ring r=0,({names}),dp;']
    source.append("ideal I=" + ",".join(map(singular_expr, forbidden)) + ";")
    source.append(f"ideal J=sat(I,ideal(t*(t+1)*({singular_expr(active)})));")
    source.append("list L=minAssGTZ(J);")
    source.append('if(size(L)==1){"ONE_PRIME";}else{"PRIME_COUNT_FAIL";}')
    source.append(
        'if(reduce(d1*d2*d3,std(L[1]))!=0){"DENSE_D_OPEN";}else{"D_OPEN_FAIL";}'
    )
    completed = subprocess.run(
        singular_command(),
        input="\n".join(source),
        text=True,
        capture_output=True,
        timeout=300,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "ONE_PRIME" in completed.stdout
    assert "DENSE_D_OPEN" in completed.stdout

    normalized = {d1: 1, d2: 1, d3: 1}
    b_solution = -2 * (a2 + a3)
    c2_solution = -2 * a1 + 2 * a3
    c3_solution = -2 * (a1 + a2)
    t_solution = a2 * (-a1 + a3) / (a1 * (a2 + a3))
    solved = {
        **normalized,
        b1: b_solution,
        c2: c2_solution,
        c3: c3_solution,
        t: t_solution,
    }
    solved_values = {
        bits: sp.factor(value.subs(solved)) for bits, value in values.items()
    }
    assert solved_values[(1, 1, 1, 1)] == 8 * a1 * (a2 + a3)
    assert all(
        value == 0 for bits, value in solved_values.items() if bits != (1, 1, 1, 1)
    )

    S, D, G, T = 2 * a1, b_solution, c2_solution, 2 * a2
    assert sp.expand(T - (-D - G - S)) == 0
    P, Q = G - T, D - S
    assert sp.expand(P - (c3_solution + 2 * a3)) == 0
    assert sp.expand(Q - (c3_solution - 2 * a3)) == 0

    # Explicit source transformation old -> new is (x3,x0,x1,x2).
    transform = lambda row: sp.Matrix([row[3], row[0], row[1], row[2]])
    transformed_u0 = 2 * (transform(planes[3][1].subs(solved)) - a3 * transform(g3))
    assert transformed_u0 == sp.Matrix([2, P + Q, Q - P, 0])
    assert transform(g3) == sp.Matrix([0, 0, 1, 1])
    transformed_x1 = transform(planes[1][1].subs(solved)) - a1 * transform(g1)
    transformed_x2 = transform(planes[2][1].subs(solved)) - a2 * transform(g2)
    assert transformed_x1 == sp.Matrix([1, 0, S, D])
    assert transformed_x2 == sp.Matrix([1, 0, G, T])
    assert transform(f1) == sp.Matrix([0, 1, 1, 0])
    assert transform(f2) == sp.Matrix([0, 1, 0, 1])

    # Replay the failed old sample and a corrected non-double rational sample.
    old = {
        a1: 1,
        a2: 1,
        a3: 1,
        b1: -4,
        c2: 2,
        c3: -4,
        d1: 1,
        d2: 1,
        d3: 1,
        t: sp.Rational(6, 5),
    }
    old_values = {bits: sp.factor(value.subs(old)) for bits, value in values.items()}
    assert [
        old_values[bits]
        for bits in ((0, 0, 1, 1), (0, 1, 1, 0), (1, 1, 1, 0), (1, 1, 1, 1))
    ] == [2, sp.Rational(22, 5), 2, 10]
    assert flattening_ranks(old_values) == (2, 2, 1, 2)

    corrected = {
        a1: 1,
        a2: 2,
        a3: 3,
        b1: -10,
        c2: 4,
        c3: -6,
        d1: 1,
        d2: 1,
        d3: 1,
        t: sp.Rational(4, 5),
    }
    corrected_values = {
        bits: sp.factor(value.subs(corrected)) for bits, value in values.items()
    }
    assert corrected_values[(1, 1, 1, 1)] == 40
    assert all(
        value == 0 for bits, value in corrected_values.items() if bits != (1, 1, 1, 1)
    )
    assert flattening_ranks(corrected_values) == (1, 1, 1, 1)
    return old_values, corrected_values


def all_outward_collisions(X):
    A, C = X[0] + X[1], X[0] - X[1]
    y = sp.Matrix(sp.symbols("y0:4"))
    x = sp.Matrix(sp.symbols("x0:4"))
    q = sp.Matrix(sp.symbols("q0:4"))
    r = sp.Matrix(sp.symbols("r0:4"))

    # All center factors equal and genuinely binary.
    equal = ((y, A), (C, x), (C, q), (C, r))
    equal_subs = {y[0]: 0, x[0]: 0, q[0]: 0, r[0]: 0}
    ideal, active, _ = forbidden_and_active(equal, equal_subs)
    variables = (x[1], x[2], x[3], q[1], q[2], q[3], r[1], r[2], r[3], y[1], y[2], y[3])
    deg = [y[1], y[2], y[3]]
    low = [
        x[3] * y[2] + x[2] * y[3],
        r[3] * y[2] + r[2] * y[3],
        -r[3] * x[2] + r[2] * x[3],
        q[3] * y[2] + q[2] * y[3],
        -q[3] * x[2] + q[2] * x[3],
        -q[3] * r[2] + q[2] * r[3],
        y[1],
    ]
    radical_check("all_equal", variables, ideal, active, [deg, low])
    for pair in ((1, 2), (1, 3), (2, 3)):
        prime_kills_pair(equal, equal_subs, low, variables, pair)

    # Repeated genuine factor, second support overlap/disjoint/outside singleton.
    t = sp.Symbol("t")
    h_overlap, v_overlap = X[0] + X[2], X[0] - X[2]
    overlap = ((h_overlap - t * A, A), (C, x), (C, q), (v_overlap, r))
    overlap_subs = {x[0]: 0, q[0]: 0, r[0]: 0}
    ideal, active, _ = forbidden_and_active(overlap, overlap_subs)
    variables = (x[1], x[2], x[3], q[1], q[2], q[3], r[1], r[2], r[3], t)
    prime = [
        q[3] * x[1] - q[3] * x[2] + q[1] * x[3] - q[2] * x[3],
        t - 1,
        r[3],
        r[1] - r[2],
    ]
    radical_check("repeated_overlap", variables, ideal, t * active, [prime])
    for pair in ((1, 3), (2, 3)):
        prime_kills_pair(overlap, overlap_subs, prime, variables, pair)

    h_disjoint, v_disjoint = X[2] + X[3], X[2] - X[3]
    disjoint = ((h_disjoint - t * A, A), (C, x), (C, q), (v_disjoint, r))
    disjoint_subs = {x[0]: 0, q[0]: 0, r[2]: 0}
    ideal, active, _ = forbidden_and_active(disjoint, disjoint_subs)
    variables = (x[1], x[2], x[3], q[1], q[2], q[3], r[0], r[1], r[3], t)
    prime = [
        q[3] * t * x[2] ** 2
        + q[2] * t * x[2] * x[3]
        - q[3] * t * x[2] * x[3]
        - q[2] * t * x[3] ** 2
        - q[3] * x[1] * x[2]
        + q[2] * x[1] * x[3],
        -q[3] * t * x[2] - q[2] * t * x[3] + q[3] * x[1] + q[1] * x[3],
        q[2] * x[1] - q[3] * x[1] + q[1] * x[2] - q[1] * x[3],
        r[3],
        r[0] - r[1],
    ]
    radical_check("repeated_disjoint", variables, ideal, t * active, [prime])
    for pair in ((1, 3), (2, 3)):
        prime_kills_pair(disjoint, disjoint_subs, prime, variables, pair)

    outside = ((X[2] - t * A, A), (C, x), (C, q), (X[2], r))
    outside_subs = {x[0]: 0, q[0]: 0, r[2]: 0}
    ideal, active, _ = forbidden_and_active(outside, outside_subs)
    variables = (x[1], x[2], x[3], q[1], q[2], q[3], r[0], r[1], r[3], t)
    radical_check("repeated_outside_singleton", variables, ideal, t * active, [])


def independent_singleton_binary_line(X):
    y = sp.Matrix(sp.symbols("y0:4"))
    x = sp.Matrix(sp.symbols("x0:4"))
    q = sp.Matrix(sp.symbols("q0:4"))
    s, t = sp.symbols("s t")
    # Three distinct factors on the 01 pencil have ratios s,1,t.  The
    # nondegenerate saturated prime is independent of s,t, so s=0 is the
    # literal polynomial singleton limit of the genuine component-21 chart.
    planes = (
        (X[0] + s * X[1], X[0] + X[1]),
        (y, X[0] - s * X[1]),
        (X[0] - X[1], x),
        (X[0] - t * X[1], q),
    )
    substitutions = {y[0]: 0, x[0]: 0, q[0]: 0}
    ideal, active, _ = forbidden_and_active(planes, substitutions)
    variables = (x[1], x[2], x[3], q[1], q[2], q[3], y[1], y[2], y[3], s, t)
    deg = [y[1], y[2], y[3]]
    placed = [
        x[3] * y[2] + x[2] * y[3],
        q[3] * y[2] + q[2] * y[3],
        -q[3] * x[2] + q[2] * x[3],
        y[1],
    ]
    open_factor = s * t * (s - 1) * (s - t) * (t - 1) * active
    radical_check(
        "independent_singleton_limit", variables, ideal, open_factor, [deg, placed]
    )

    fixed = {
        y[1]: 0,
        y[2]: 1,
        y[3]: 1,
        x[1]: 1,
        x[2]: 1,
        x[3]: -1,
        q[1]: 1,
        q[2]: 2,
        q[3]: -2,
        t: 2,
    }
    family_values = {
        bits: sp.factor(value.subs(substitutions).subs(fixed))
        for bits, value in coefficients(planes).items()
    }
    assert all(
        value == 0 for bits, value in family_values.items() if bits != (1, 1, 1, 1)
    )
    assert sp.expand(family_values[(1, 1, 1, 1)] - 4 * (s - 1)) == 0
    singleton = tuple(
        tuple(row.subs(fixed).subs(s, 0) for row in plane) for plane in planes
    )
    genuine = tuple(
        tuple(row.subs(fixed).subs(s, sp.Rational(1, 3)) for row in plane)
        for plane in planes
    )
    assert pair_profile(singleton) == (3, 3, 3, 4, 4, 4)
    assert pair_profile(genuine) == (3, 3, 3, 4, 4, 4)


def dependent_center_ledger(X):
    y = sp.Matrix(sp.symbols("y0:4"))
    x = sp.Matrix(sp.symbols("x0:4"))
    q = sp.Matrix(sp.symbols("q0:4"))

    def family(u, v, w, z):
        return ((u, w), (y, v), (z, x), (z, q))

    # Singleton inward support, binary repeated support containing it.
    A, C = X[0] + X[1], X[0] - X[1]
    inside = family(X[0], X[0], A, C)
    subs = {y[0]: 0, x[0]: 0, q[0]: 0}
    ideal, active, _ = forbidden_and_active(inside, subs)
    variables = (x[1], x[2], x[3], q[1], q[2], q[3], y[1], y[2], y[3])
    deg = [y[1], y[2], y[3]]
    low = [
        x[3] * y[2] + x[2] * y[3],
        q[3] * y[2] + q[2] * y[3],
        -q[3] * x[2] + q[2] * x[3],
        y[1],
    ]
    radical_check("dependent_singleton_inside", variables, ideal, active, [deg, low])
    prime_kills_pair(inside, subs, low, variables, (2, 3))

    E, F = X[2] + X[3], X[2] - X[3]
    outside = family(X[0], X[0], E, F)
    subs = {y[0]: 0, x[2]: 0, q[2]: 0}
    ideal, active, _ = forbidden_and_active(outside, subs)
    variables = (x[0], x[1], x[3], q[0], q[1], q[3], y[1], y[2], y[3])
    deg = [y[1], y[2], y[3]]
    radical_check("dependent_singleton_outside", variables, ideal, active, [deg])

    B, D = X[1] + X[2], X[1] - X[2]
    overlap = family(A, C, B, D)
    subs = {y[0]: 0, x[1]: 0, q[1]: 0}
    ideal, active, _ = forbidden_and_active(overlap, subs)
    variables = (x[0], x[2], x[3], q[0], q[2], q[3], y[1], y[2], y[3])
    radical_check(
        "dependent_binary_overlap", variables, ideal, active, [[y[1], y[2], y[3]]]
    )

    disjoint = family(A, C, E, F)
    subs = {y[0]: 0, x[2]: 0, q[2]: 0}
    ideal, active, _ = forbidden_and_active(disjoint, subs)
    variables = (x[0], x[1], x[3], q[0], q[1], q[3], y[1], y[2], y[3])
    primes = [
        [y[1], y[2], y[3]],
        [
            -q[3] * x[0] * x[1]
            - q[3] * x[1] ** 2
            + q[1] * x[0] * x[3]
            - q[1] * x[1] * x[3],
            q[3] * x[0] + q[3] * x[1] + q[0] * x[3] + q[1] * x[3],
            q[1] * x[0] + q[0] * x[1],
            y[2] - y[3],
            y[1],
        ],
        [y[2] + y[3], y[1], x[0] + x[1], q[0] + q[1]],
        [y[1], x[1], x[0], q[0] + q[1]],
        [y[1], x[0] + x[1], q[1], q[0]],
    ]
    radical_check("dependent_binary_disjoint", variables, ideal, active, primes)
    for prime, pairs in zip(
        primes[1:],
        (
            ((1, 2), (1, 3)),
            ((1, 2), (1, 3), (2, 3)),
            ((1, 2), (2, 3)),
            ((1, 3), (2, 3)),
        ),
        strict=True,
    ):
        for pair in pairs:
            prime_kills_pair(disjoint, subs, prime, variables, pair)


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    assert "c_2=-2a_1+2a_3" in theorem
    assert "T=-D-G-S" in theorem
    assert "UNRESOLVED" in theorem
    for dependency in (
        REPO_ROOT / "claims" / "p4" / "classifications" / "star"
        / "coincident-support-star-reverse"
        / "P4_COINCIDENT_SUPPORT_STAR_REVERSE_CLASSIFICATION.md",
        REPO_ROOT / "claims" / "p4" / "classifications" / "star"
        / "radical-star" / "P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md",
        REPO_ROOT / "claims/p4/classifications/pair-geometry/lower-pair-rank-exhaustion/P4_LOWER_PAIR_RANK_COMPONENT_EXHAUSTION.md",
    ):
        assert dependency.exists()

    X = tuple(sp.eye(4).col(index) for index in range(4))
    old, corrected = source_triangle(X)
    all_outward_collisions(X)
    independent_singleton_binary_line(X)
    dependent_center_ledger(X)

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "orientation_orbits": 2,
                "source_triangle_saturated_minimal_primes": 1,
                "source_triangle_placement": "L3",
                "failed_old_sample_flattening_ranks": flattening_ranks(old),
                "corrected_sample_flattening_ranks": flattening_ranks(corrected),
                "dependent_disjoint_nontrivial_primes": 4,
                "no_double_star_1110_complete": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
