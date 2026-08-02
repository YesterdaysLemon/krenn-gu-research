#!/usr/bin/env python3
"""No-import audit of the no-double star-(1,1,1) classification."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
BITS = tuple(itertools.product((0, 1), repeat=4))
QWORDS = tuple(itertools.combinations(range(4), 2))
MODE_PAIRS = tuple(itertools.combinations(range(4), 2))


def subset_dp_permanent(rows):
    states = {0: sp.Integer(1)}
    for row in rows:
        next_states = {}
        for mask, value in states.items():
            for coordinate, entry in enumerate(row):
                if mask & (1 << coordinate):
                    continue
                new_mask = mask | (1 << coordinate)
                next_states[new_mask] = sp.expand(
                    next_states.get(new_mask, 0) + value * entry
                )
        states = next_states
    return sp.factor(states.get(15, 0))


def tensor(planes):
    return {
        bits: subset_dp_permanent(tuple(planes[i][bits[i]] for i in range(4)))
        for bits in BITS
    }


def quadratic_product(left, right):
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in QWORDS])


def product_matrix(left, right):
    return sp.Matrix.hstack(*(quadratic_product(u, v) for u in left for v in right))


def profile(planes):
    return tuple(product_matrix(planes[i], planes[j]).rank() for i, j in MODE_PAIRS)


def flattening_ranks(values):
    result = []
    for mode in range(4):
        other = tuple(index for index in range(4) if index != mode)
        matrix = sp.zeros(2, 8)
        for bits, value in values.items():
            column = sum(bits[index] << place for place, index in enumerate(other))
            matrix[bits[mode], column] = value
        result.append(matrix.rank())
    return tuple(result)


def pure_active(values):
    assert values[(1, 1, 1, 1)] != 0
    assert all(value == 0 for bits, value in values.items() if bits != (1, 1, 1, 1))


def singular_command():
    if shutil.which("Singular"):
        return [shutil.which("Singular"), "-q"]
    if shutil.which("wsl.exe"):
        return ["wsl.exe", "--exec", "/usr/bin/Singular", "-q"]
    raise RuntimeError("Singular unavailable")


def sx(expression):
    return str(sp.expand(expression)).replace("**", "^")


def minass_count(label, variables, generators, open_factor, expected, dense=None):
    source = [
        'LIB "primdec.lib";',
        f"ring r=0,({','.join(map(str, variables))}),dp;",
        "ideal I=" + ",".join(map(sx, generators)) + ";",
        f"ideal J=sat(I,ideal({sx(open_factor)}));",
        "list L=minAssGTZ(J);",
        f'if(size(L)=={expected}){{"COUNT_OK";}}else{{"COUNT_FAIL";}}',
    ]
    if dense is not None:
        source.append(
            f'if(reduce({sx(dense)},std(L[1]))!=0){{"DENSE_OK";}}else{{"DENSE_FAIL";}}'
        )
    completed = subprocess.run(
        singular_command(),
        input="\n".join(source),
        text=True,
        capture_output=True,
        timeout=300,
        check=False,
    )
    assert completed.returncode == 0, (label, completed.stderr)
    assert "COUNT_OK" in completed.stdout, (label, completed.stdout)
    if dense is not None:
        assert "DENSE_OK" in completed.stdout, (label, completed.stdout)


def source_triangle_audit(X):
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
    values = tensor(planes)
    forbidden = [
        value for bits, value in values.items() if bits != (1, 1, 1, 1) and value != 0
    ]
    active = values[(1, 1, 1, 1)]
    variables = (a1, b1, d1, a2, c2, d2, a3, c3, d3, t)
    minass_count(
        "source_triangle", variables, forbidden, t * (t + 1) * active, 1, d1 * d2 * d3
    )

    failed = {
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
    failed_values = {
        bits: sp.factor(value.subs(failed)) for bits, value in values.items()
    }
    assert [
        failed_values[bits]
        for bits in ((0, 0, 1, 1), (0, 1, 1, 0), (1, 1, 1, 0), (1, 1, 1, 1))
    ] == [2, sp.Rational(22, 5), 2, 10]
    assert flattening_ranks(failed_values) == (2, 2, 1, 2)

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
    corrected_planes = tuple(
        tuple(row.subs(corrected) for row in plane) for plane in planes
    )
    corrected_values = tensor(corrected_planes)
    pure_active(corrected_values)
    assert corrected_values[(1, 1, 1, 1)] == 40
    assert flattening_ranks(corrected_values) == (1, 1, 1, 1)

    # Independently reconstruct the old->new source map and L3 row spans.
    source_map = lambda row: sp.Matrix([row[3], row[0], row[1], row[2]])
    transformed = tuple(
        tuple(source_map(row) for row in corrected_planes[index])
        for index in (3, 1, 2, 0)
    )
    S, D, G, T = 2, -10, 4, 4
    P, Q = G - T, D - S
    l3 = (
        (sp.Matrix([2, P + Q, Q - P, 0]), sp.Matrix([0, 0, 1, 1])),
        (sp.Matrix([0, 1, -1, 0]), sp.Matrix([1, 0, S, D])),
        (sp.Matrix([1, 0, G, T]), sp.Matrix([0, 1, 0, -1])),
        (sp.Matrix([0, 1, 1, 0]), sp.Matrix([0, 1, 0, 1])),
    )
    for actual, expected in zip(transformed, l3, strict=True):
        assert (
            sp.Matrix.hstack(*actual).T.rref()[0]
            == sp.Matrix.hstack(*expected).T.rref()[0]
        )
    assert T == -D - G - S
    return flattening_ranks(failed_values), flattening_ranks(corrected_values)


def component21_singleton_arc(X):
    s, t = sp.symbols("s t")
    y = sp.Matrix([0, 0, 1, 1])
    x = sp.Matrix([0, 1, 1, -1])
    q = sp.Matrix([0, 1, 2, -2])
    planes = (
        (X[0] + s * X[1], X[0] + X[1]),
        (y, X[0] - s * X[1]),
        (X[0] - X[1], x),
        (X[0] - t * X[1], q),
    )
    values = {
        bits: sp.factor(value.subs(t, 2)) for bits, value in tensor(planes).items()
    }
    assert all(value == 0 for bits, value in values.items() if bits != (1, 1, 1, 1))
    assert sp.expand(values[(1, 1, 1, 1)] - 4 * (s - 1)) == 0
    singleton = tuple(
        tuple(row.subs({s: 0, t: 2}) for row in plane) for plane in planes
    )
    genuine = tuple(
        tuple(row.subs({s: sp.Rational(1, 3), t: 2}) for row in plane)
        for plane in planes
    )
    pure_active(tensor(singleton))
    pure_active(tensor(genuine))
    assert profile(singleton) == (3, 3, 3, 4, 4, 4)
    assert profile(genuine) == (3, 3, 3, 4, 4, 4)

    # Fresh symbolic census of the genuine pencil: degenerate plus one
    # parameter-independent nondegenerate prime.
    yy = sp.Matrix(sp.symbols("yy0:4"))
    xx = sp.Matrix(sp.symbols("xx0:4"))
    qq = sp.Matrix(sp.symbols("qq0:4"))
    symbolic = (
        (X[0] + s * X[1], X[0] + X[1]),
        (yy, X[0] - s * X[1]),
        (X[0] - X[1], xx),
        (X[0] - t * X[1], qq),
    )
    substitutions = {yy[0]: 0, xx[0]: 0, qq[0]: 0}
    symbolic_values = {
        bits: sp.factor(value.subs(substitutions))
        for bits, value in tensor(symbolic).items()
    }
    forbidden = [
        value
        for bits, value in symbolic_values.items()
        if bits != (1, 1, 1, 1) and value != 0
    ]
    active = symbolic_values[(1, 1, 1, 1)]
    variables = (xx[1], xx[2], xx[3], qq[1], qq[2], qq[3], yy[1], yy[2], yy[3], s, t)
    minass_count(
        "component21_arc",
        variables,
        forbidden,
        s * t * (s - 1) * (s - t) * (t - 1) * active,
        2,
    )
    return profile(singleton)


def collision_samples(X):
    A, C = X[0] + X[1], X[0] - X[1]
    equal = (
        (sp.Matrix([0, 0, 1, 1]), A),
        (C, sp.Matrix([0, 1, 1, -1])),
        (C, sp.Matrix([0, 1, 2, -2])),
        (C, sp.Matrix([0, 1, 3, -3])),
    )
    overlap = (
        ((X[0] + X[2]) - A, A),
        (C, sp.Matrix([0, 1, 2, 1])),
        (C, sp.Matrix([0, 2, 1, 1])),
        (X[0] - X[2], sp.Matrix([0, 1, 1, 0])),
    )
    disjoint = (
        ((X[2] + X[3]) - 2 * A, A),
        (C, sp.Matrix([0, 1, 1, 1])),
        (C, sp.Matrix([0, 3, 1, 1])),
        (X[2] - X[3], sp.Matrix([1, 1, 0, 0])),
    )
    for planes in (equal, overlap, disjoint):
        pure_active(tensor(planes))
    assert profile(equal) == (3, 3, 3, 3, 3, 3)
    assert profile(overlap) == (3, 3, 2, 4, 3, 3)
    assert profile(disjoint) == (3, 3, 3, 3, 3, 3)
    return {
        "equal": profile(equal),
        "overlap": profile(overlap),
        "disjoint": profile(disjoint),
    }


def dependent_disjoint_census(X):
    y = sp.Matrix(sp.symbols("dy0:4"))
    x = sp.Matrix(sp.symbols("dx0:4"))
    q = sp.Matrix(sp.symbols("dq0:4"))
    A, C = X[0] + X[1], X[0] - X[1]
    E, F = X[2] + X[3], X[2] - X[3]
    planes = ((A, E), (y, C), (F, x), (F, q))
    substitutions = {y[0]: 0, x[2]: 0, q[2]: 0}
    values = {
        bits: sp.factor(value.subs(substitutions))
        for bits, value in tensor(planes).items()
    }
    forbidden = [
        value for bits, value in values.items() if bits != (1, 1, 1, 1) and value != 0
    ]
    active = values[(1, 1, 1, 1)]
    variables = (x[0], x[1], x[3], q[0], q[1], q[3], y[1], y[2], y[3])
    minass_count("dependent_disjoint", variables, forbidden, active, 5)


def main():
    theorem = (
        ROOT / "P4_NO_DOUBLE_ENDPOINT_STAR_1110_COLLISION_CLASSIFICATION.md"
    ).read_text(encoding="utf-8")
    assert "component 21 parameter closure" in theorem
    assert "previously considered values" in theorem
    assert "UNRESOLVED" in theorem
    X = tuple(sp.eye(4).col(index) for index in range(4))
    failed, corrected = source_triangle_audit(X)
    singleton_profile = component21_singleton_arc(X)
    samples = collision_samples(X)
    dependent_disjoint_census(X)
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent subset-DP permanent and fresh Singular censuses",
                "failed_sample_flattenings": failed,
                "corrected_sample_flattenings": corrected,
                "component21_singleton_arc_profile": singleton_profile,
                "collision_sample_profiles": samples,
                "source_triangle_minimal_primes": 1,
                "dependent_disjoint_minimal_primes": 5,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
