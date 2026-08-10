#!/usr/bin/env python3
"""Verify component 21's lambda=-1 zero-base second normals."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])

import verify_p5_component21_finite_base_extension_infinity_partial_closure as V

ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_COMPONENT21_FINITE_H22_EXTENSION_ZERO_BASE_LAMBDA_MINUS_ONE_SECOND_NORMAL_OBSTRUCTION.md"
)
DIAGONAL_ROWS = (0, 15, 16, 31)


def determinant(matrix, rows, columns):
    return sp.factor(matrix.extract(rows, columns).det())


def assert_equal(left, right):
    assert sp.expand(left - right) == 0


def is_zero(vector):
    return all(sp.expand(value) == 0 for value in vector)


def unit(length, index):
    return sp.eye(length).col(index)


def independent(vectors):
    return sp.Matrix.hstack(*vectors).rank() == len(vectors)


def main() -> None:
    p, q, kappa, ell, slope = sp.symbols("p q kappa ell slope")
    x, y, zeta = sp.symbols("X Y Z")
    tangent = sp.symbols("t")
    cap_p, cap_q = sp.symbols("P Q")
    cap_a, cap_b, cap_c, cap_e = sp.symbols("A B C E")
    extension = sp.symbols("z0:8")
    alpha, beta = V.finite_bases(p, q, kappa, ell)
    matrix = V.stacked_contraction_matrix(
        alpha, beta, extension, "finite", slope
    )
    identity = sp.eye(8)
    u = identity.col(3)
    w = identity.col(7)
    v = -identity.col(1) + identity.col(4)
    parameters = (p, q, kappa, ell, slope)

    def normal(leading, substitution):
        output = matrix.subs(substitution)
        for parameter in parameters:
            output = output.row_join(
                (sp.diff(matrix, parameter) * leading).subs(substitution)
            )
        return output

    # kappa!=0 kernel P1, open direction Y!=0.
    h_plane = x * u + y * w
    n_plane = normal(h_plane, {p: 0, q: 0, slope: -1})
    plane_kernel = (
        u.col_join(sp.zeros(5, 1)),
        w.col_join(sp.zeros(5, 1)),
        unit(13, 10),
        unit(13, 11),
    )
    assert independent(plane_kernel)
    assert all(is_zero(n_plane * vector) for vector in plane_kernel)
    assert n_plane.row(0) == sp.zeros(1, 13)
    assert n_plane.row(15) == sp.zeros(1, 13)
    assert_equal(
        determinant(
            n_plane,
            (3, 11, 18, 20, 22, 23, 24, 26, 28),
            (0, 1, 2, 4, 5, 6, 8, 9, 12),
        ),
        -131072 * y**3 * kappa**2,
    )

    # Its Y=0 intersection with the ordinary-weight kernel line.
    n_u_nonzero_kappa = n_plane.subs({x: 1, y: 0})
    weight_lift = sp.Rational(1, 2) * unit(13, 6) + unit(13, 12)
    u_nonzero_kernel = plane_kernel + (weight_lift,)
    assert independent(u_nonzero_kernel)
    assert all(is_zero(n_u_nonzero_kappa * vector) for vector in u_nonzero_kernel)
    assert_equal(
        determinant(
            n_u_nonzero_kappa,
            (2, 10, 18, 20, 22, 24, 26, 28),
            (0, 1, 2, 4, 5, 6, 8, 9),
        ),
        65536 * kappa**2,
    )
    force_lambda_w = (sp.diff(matrix, slope) * w).subs(
        {p: 0, q: 0, slope: -1}
    )
    assert all(force_lambda_w[row] == 0 for row in DIAGONAL_ROWS)
    augmented_u_nonzero = n_u_nonzero_kappa.row_join(force_lambda_w)
    augmented_columns = (0, 1, 2, 4, 5, 6, 8, 9, 13)
    assert_equal(
        determinant(
            augmented_u_nonzero,
            (2, 10, 16, 18, 20, 22, 23, 24, 26),
            augmented_columns,
        ),
        -131072 * kappa**2 * (ell**2 - 1),
    )
    assert_equal(
        determinant(
            augmented_u_nonzero,
            (2, 10, 16, 18, 19, 20, 22, 24, 28),
            augmented_columns,
        ),
        -131072 * ell * kappa,
    )

    # kappa=0 kernel P2 and its open rank-nine locus.
    h_p2 = x * u + y * v + zeta * w
    p2_substitution = {p: 0, q: 0, kappa: 0, slope: -1}
    n_p2 = normal(h_p2, p2_substitution)
    p2_kernel = (
        u.col_join(sp.zeros(5, 1)),
        v.col_join(sp.zeros(5, 1)),
        w.col_join(sp.zeros(5, 1)),
        unit(13, 11),
    )
    assert independent(p2_kernel)
    assert all(is_zero(n_p2 * vector) for vector in p2_kernel)
    assert n_p2.row(0) == sp.zeros(1, 13)
    assert n_p2.row(15) == sp.zeros(1, 13)
    p2_columns = (0, 1, 2, 5, 6, 8, 9, 10, 12)
    p2_minors = (
        determinant(
            n_p2,
            (2, 10, 16, 18, 19, 20, 22, 24, 28),
            p2_columns,
        ),
        determinant(
            n_p2,
            (2, 10, 16, 18, 20, 22, 23, 24, 28),
            p2_columns,
        ),
        determinant(
            n_p2,
            (3, 11, 16, 18, 19, 20, 22, 24, 28),
            p2_columns,
        ),
        determinant(
            n_p2,
            (3, 11, 16, 18, 20, 22, 23, 24, 28),
            p2_columns,
        ),
    )
    expected_p2_minors = (
        -131072 * x**2 * y * (-y + zeta * ell),
        -131072 * x**2 * y * zeta,
        -131072 * y * (-y + zeta * ell) * (y * ell - zeta) ** 2,
        -131072 * y * zeta * (y * ell - zeta) ** 2,
    )
    assert all(
        sp.expand(value - expected) == 0
        for value, expected in zip(p2_minors, expected_p2_minors, strict=True)
    )

    # Exceptional projective line H=v+ell*w, where dp,dq join the kernel.
    h_special = v + ell * w
    n_special = normal(h_special, p2_substitution)
    special_kernel = (
        u.col_join(sp.zeros(5, 1)),
        v.col_join(sp.zeros(5, 1)),
        w.col_join(sp.zeros(5, 1)),
        unit(13, 8),
        unit(13, 9),
        unit(13, 11),
    )
    assert independent(special_kernel)
    assert all(is_zero(n_special * vector) for vector in special_kernel)
    assert n_special.extract(range(16), range(13)) == sp.zeros(16, 13)
    special_columns = (0, 1, 2, 5, 6, 10, 12)
    assert_equal(
        determinant(
            n_special,
            (16, 18, 19, 20, 22, 24, 28),
            special_columns,
        ),
        -8192 * (ell**2 - 1),
    )
    assert_equal(
        determinant(
            n_special,
            (16, 18, 20, 22, 23, 24, 28),
            special_columns,
        ),
        -8192 * ell,
    )
    first_extension = cap_a * u + cap_b * v + cap_c * w
    expansion = matrix.subs(
        {
            p: tangent * cap_p,
            q: tangent * cap_q,
            kappa: 0,
            ell: ell + tangent * cap_e,
            slope: -1,
        }
    ) * (h_special + tangent * first_extension)
    first_coefficient = sp.Matrix(
        [sp.expand(value).coeff(tangent, 1) for value in expansion]
    )
    second_force = sp.Matrix(
        [sp.factor(sp.expand(value).coeff(tangent, 2)) for value in expansion]
    )
    assert is_zero(first_coefficient)
    expected_force = sp.zeros(32, 1)
    expected_force[2] = -4 * cap_a * cap_p
    expected_force[3] = 4 * cap_p * (cap_b * ell - cap_c + cap_e)
    expected_force[10] = -4 * cap_a * cap_q
    expected_force[11] = 4 * cap_q * (cap_b * ell - cap_c + cap_e)
    assert is_zero(second_force - expected_force)

    # Y=0,Z!=0 crossing of the P2 with the kappa-moving P1.
    h_kappa_crossing = x * u + zeta * w
    n_kappa_crossing = normal(h_kappa_crossing, p2_substitution)
    kappa_crossing_kernel = (
        u.col_join(sp.zeros(5, 1)),
        v.col_join(sp.zeros(5, 1)),
        w.col_join(sp.zeros(5, 1)),
        unit(13, 10),
        unit(13, 11),
    )
    assert independent(kappa_crossing_kernel)
    assert all(
        is_zero(n_kappa_crossing * vector)
        for vector in kappa_crossing_kernel
    )
    crossing_columns = (0, 1, 2, 5, 6, 8, 9, 12)
    assert_equal(
        determinant(
            n_kappa_crossing,
            (3, 11, 16, 20, 22, 23, 24, 28),
            crossing_columns,
        ),
        -32768 * zeta**3,
    )
    force_kappa_v = (sp.diff(matrix, kappa) * v).subs(p2_substitution)
    assert all(force_kappa_v[row] == 0 for row in DIAGONAL_ROWS)
    augmented_kappa = n_kappa_crossing.row_join(force_kappa_v)
    assert_equal(
        determinant(
            augmented_kappa,
            (3, 11, 16, 18, 20, 22, 23, 24, 28),
            crossing_columns + (13,),
        ),
        131072 * zeta**3,
    )

    # Triple crossing H=u at kappa=0.
    n_triple = n_kappa_crossing.subs({x: 1, zeta: 0})
    triple_kernel = kappa_crossing_kernel + (weight_lift,)
    assert independent(triple_kernel)
    assert all(is_zero(n_triple * vector) for vector in triple_kernel)
    assert_equal(
        determinant(
            n_triple,
            (2, 10, 16, 20, 22, 24, 28),
            (0, 1, 2, 5, 6, 8, 9),
        ),
        -16384,
    )
    force_lambda_v = (sp.diff(matrix, slope) * v).subs(p2_substitution)
    force_lambda_w_zero = force_lambda_w.subs(kappa, 0)
    for force in (force_kappa_v, force_lambda_v, force_lambda_w_zero):
        assert force[0] == 0 and force[15] == 0
    augmented_triple = (
        n_triple.row_join(force_kappa_v)
        .row_join(force_lambda_v)
        .row_join(force_lambda_w_zero)
    )
    assert_equal(
        determinant(
            augmented_triple,
            (2, 10, 16, 18, 19, 20, 22, 23, 24, 28),
            (0, 1, 2, 5, 6, 8, 9, 13, 14, 15),
        ),
        262144,
    )

    theorem = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for phrase in (
        "Exact characteristic-zero theorem in the displayed raw finite chart",
        "The exceptional line `H=v+ell w`",
        "complete second-order branch decomposition",
        "lambda=1",
        "remain **UNKNOWN**",
        "global Krenn--Gu conjecture remains **UNRESOLVED**",
        "No finite-field",
    ):
        assert phrase in theorem

    print(
        json.dumps(
            {
                "status": "PASS",
                "field": "exact characteristic zero",
                "component": 21,
                "stratum": "p=q=0, lambda=-1",
                "kappa_nonzero": {
                    "kernel_projective_dimension": 1,
                    "open_first_normal_rank": 9,
                    "u_first_normal_rank": 8,
                    "u_augmented_second_rank": 9,
                    "zero_second_product": "B*R=0",
                },
                "kappa_zero": {
                    "kernel_projective_dimension": 2,
                    "open_first_normal_rank": 9,
                    "exceptional_line": "H=v+ell*w",
                    "exceptional_line_first_normal_rank": 7,
                    "kappa_crossing_first_normal_rank": 8,
                    "kappa_crossing_augmented_rank": 9,
                    "triple_first_normal_rank": 7,
                    "triple_augmented_rank": 10,
                },
                "second_normal_H22_incidence_empty": True,
                "higher_zero_normals_closed": False,
                "lambda_plus_one_closed": False,
                "arbitrary_order_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(THEOREM.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
