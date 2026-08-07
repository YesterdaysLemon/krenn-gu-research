#!/usr/bin/env python3
"""Independent no-import audit of the one-double star classification."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess
from fractions import Fraction

import sympy as sp


def permanent_dp(rows):
    states = {0: sp.Integer(1)}
    for row in rows:
        updated = {}
        for mask, value in states.items():
            for column in range(4):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                updated[new_mask] = updated.get(new_mask, 0) + value * row[column]
        states = updated
    return sp.expand(states[15])


def squarefree_product(left, right):
    return sp.Matrix(
        [
            left[i] * right[j] + left[j] * right[i]
            for i, j in itertools.combinations(range(4), 2)
        ]
    )


def rational_rank(columns):
    return sp.Matrix.hstack(*columns).rank()


def pair_rank(left, right):
    return rational_rank([squarefree_product(u, v) for u in left for v in right])


def singular_command():
    native = shutil.which("Singular")
    if native:
        return [native, "-q"]
    wsl = shutil.which("wsl.exe")
    if wsl:
        return [wsl, "--exec", "/usr/bin/Singular", "-q"]
    raise RuntimeError("Singular is required for the independent Q audit")


def audit_radical_intersection():
    # Independently ordered reconstruction of the seven primes.
    source = r"""
LIB "primdec.lib";
ring r=0,(a1,b1,d1,a2,c2,d2,a3,c3,d3),dp;
ideal I=
-2*a1*d3+2*a3*d1+b1*d3-c3*d1,
2*a1*d2+2*a2*d1+b1*d2+c2*d1,
2*a1*a2*d3+2*a1*a3*d2+a2*b1*d3+a2*c3*d1-a3*b1*d2+a3*c2*d1+b1*c2*d3+b1*c3*d2,
-2*a2*d3-2*a3*d2+c2*d3-c3*d2;
ideal Q7=2*d2*a3+d2*c3+2*a2*d3-c2*d3,d1,b1,a1;
ideal Q6=-d2*c3+c2*d3,d2*a3+a2*d3,c2*a3+a2*c3,-2*d1*a3+d1*c3+2*a1*d3,2*d1*a2+d1*c2+2*a1*d2,b1;
ideal Q5=-2*d2*a3+c2*d3,d2*c3+2*a2*d3,4*a2*a3+c2*c3,2*d1*a3-d1*c3+b1*d3,2*d1*a2+d1*c2+b1*d2,a1;
ideal Q4=-2*d1*a3+d1*c3+2*a1*d3-b1*d3,d2,c2,a2;
ideal Q3=d3,d2,d1;
ideal Q2=d3,2*a3-c3,d2,2*a2+c2;
ideal Q1=2*d1*a2+d1*c2+2*a1*d2+b1*d2,d3,c3,a3;
ideal J=intersect(Q7,Q6); J=intersect(J,Q5); J=intersect(J,Q4);
J=intersect(J,Q3); J=intersect(J,Q2); J=intersect(J,Q1);
ideal R=radical(I);
if(size(simplify(reduce(R,std(J)),2))==0 && size(simplify(reduce(J,std(R)),2))==0){"AUDIT_RADICAL_EQUAL";}else{"AUDIT_FAIL";}
"""
    completed = subprocess.run(
        singular_command(),
        input=source,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "AUDIT_RADICAL_EQUAL" in completed.stdout, completed.stdout


def dense_tuple(parameters):
    X = tuple(sp.eye(4).col(index) for index in range(4))
    u = X[0] + X[1]
    v = X[0] - X[1]
    w = X[0] + X[2]
    z = X[0] - X[2]
    h = X[2] - X[1]
    k = X[2] + X[1]
    a1, b1, d1, a2, c2, d2, a3, c3, d3 = map(sp.Rational, parameters)
    x1 = a1 * u + b1 * X[2] + d1 * X[3]
    x2 = a2 * w + c2 * X[1] + d2 * X[3]
    x3 = a3 * h + c3 * X[0] + d3 * X[3]
    return ((u, w), (v, x1), (z, x2), (k, x3))


def audit_dense_primes():
    samples = (
        (0, Fraction(1, 2), 1, Fraction(-3, 4), 1, 1, 1, 3, 2),
        (-3, 0, 2, 1, 1, 1, -2, 2, 2),
    )
    records = []
    for sample in samples:
        planes = dense_tuple(sample)
        values = {
            bits: sp.factor(
                permanent_dp([planes[index][bits[index]] for index in range(4)])
            )
            for bits in itertools.product((0, 1), repeat=4)
        }
        active = values[(1, 1, 1, 1)]
        assert active != 0
        assert all(value == 0 for bits, value in values.items() if bits != (1, 1, 1, 1))
        profile = tuple(
            pair_rank(planes[left], planes[right])
            for left, right in itertools.combinations(range(4), 2)
        )
        assert profile == (3, 3, 3, 4, 4, 4)
        # The two leaf-facing exact pairs have overlapping genuine supports
        # 02 and 12 and independent center factors.
        assert squarefree_product(planes[0][1], planes[2][0]) == sp.zeros(6, 1)
        assert squarefree_product(
            planes[0][1] - planes[0][0], planes[3][0]
        ) == sp.zeros(6, 1)
        records.append({"active": str(active), "pair_profile": profile})
    return records


def audit_singleton_boundaries():
    # Source permutation and unequal scales retain the zero square column.
    e = sp.Matrix((0, 0, 5, 0))
    u = sp.Matrix((2, 3, 0, 7))
    v = sp.Matrix((11, 13, 0, 17))
    matrix = sp.Matrix.hstack(
        squarefree_product(e, v),
        squarefree_product(e, e),
        squarefree_product(u, v),
        squarefree_product(u, e),
    )
    assert matrix.rank() <= 3
    return True


def main():
    audit_radical_intersection()
    dense_records = audit_dense_primes()
    audit_singleton_boundaries()
    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import characteristic-zero audit",
                "field": "Q",
                "radical_intersection_reconstructed": True,
                "dense_prime_samples": dense_records,
                "singleton_projective_boundary_checked": True,
                "finite_field_proof_used": False,
                "new_component_orbit": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
